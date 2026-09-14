"""Privileged installation/rollback proof, restricted to temporary fixtures."""
import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('deploy_manager', ROOT / 'ops/deploy/manage_dpn_deploy.py')
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)


@unittest.skipUnless(os.geteuid() == 0, 'root metadata proof requires isolated privileged test run')
class DeployInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='dpn-install-test-', dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'source'
        self.repo.mkdir()
        self.source = self.repo / 'dpn-deploy'
        self.previous = b'#!/bin/bash\necho previous-fixture\n'
        self.updated = b'#!/bin/bash\necho reviewed-fixture\n'
        self.source.write_bytes(self.updated)
        for args in [('init', '-q'), ('add', '.'),
                     ('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'review fixture')]:
            self.git(*args)
        self.commit = self.git('rev-parse', 'HEAD').stdout.strip()
        (self.root / 'runtime').mkdir()
        self.target = self.root / 'runtime/dpn-deploy'
        self.target.write_bytes(self.previous)
        self.target.chmod(0o750)
        (self.root / 'deploy.lock').touch(mode=0o600)

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args],
                              capture_output=True, text=True, check=True)

    def args(self, action, **changes):
        values = dict(action=action, source=str(self.source), repo=str(self.repo), commit=self.commit,
                      expected_sha=manager.digest(self.updated), expected_current_sha=manager.digest(self.previous),
                      backup=None, fixture_root=str(self.root))
        values.update(changes)
        return argparse.Namespace(**values)

    def test_validate_has_no_runtime_or_backup_writes(self):
        before = self.target.stat()
        result = manager.manage(self.args('validate'))
        self.assertEqual(result['result'], 'VALIDATED')
        self.assertEqual(self.target.stat().st_ino, before.st_ino)
        self.assertEqual(self.target.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertFalse((self.root / 'backups').exists())

    def test_matching_install_is_noop(self):
        self.target.write_bytes(self.updated)
        before = self.target.stat()
        result = manager.manage(self.args('install', expected_current_sha=manager.digest(self.updated)))
        self.assertEqual(result['result'], 'MATCH_NOOP')
        self.assertEqual(self.target.stat().st_ino, before.st_ino)
        self.assertFalse((self.root / 'backups').exists())

    def test_install_and_rollback_exact_bytes_root_mode_syntax(self):
        result = manager.manage(self.args('install'))
        backup = Path(result['backup'])
        self.assertEqual(backup.read_bytes(), self.previous)
        self.assertTrue(manager.expected_metadata(backup))
        self.assertEqual(self.target.read_bytes(), self.updated)
        self.assertTrue(manager.expected_metadata(self.target))
        result = manager.manage(self.args('rollback', backup=str(backup),
                                         expected_sha=manager.digest(self.previous),
                                         expected_current_sha=manager.digest(self.updated)))
        self.assertEqual(result['result'], 'ROLLBACK_VERIFIED')
        self.assertEqual(self.target.read_bytes(), self.previous)
        self.assertTrue(manager.expected_metadata(self.target))
        manager.syntax(self.target.read_bytes())

    def test_working_tree_change_is_rejected_even_with_its_expected_hash(self):
        self.source.write_bytes(self.previous)
        with self.assertRaises(manager.Rejected):
            manager.manage(self.args('install', expected_sha=manager.digest(self.previous)))
        self.assertEqual(self.target.read_bytes(), self.previous)

    def test_wrong_expected_source_or_current_hash_rejected(self):
        for values in [dict(expected_sha='0' * 64), dict(expected_current_sha='0' * 64)]:
            with self.assertRaises(manager.Rejected):
                manager.manage(self.args('install', **values))
        self.assertFalse((self.root / 'backups').exists())

    def test_pinned_invalid_shell_is_rejected(self):
        bad = b'#!/bin/bash\nif then\n'
        self.source.write_bytes(bad)
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'invalid fixture')
        commit = self.git('rev-parse', 'HEAD').stdout.strip()
        with self.assertRaises(manager.Rejected):
            manager.manage(self.args('install', commit=commit, expected_sha=manager.digest(bad)))

    def test_held_deployment_lock_prevents_install(self):
        with open(self.root / 'deploy.lock', 'r+b') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):
                manager.manage(self.args('install'))
        self.assertEqual(self.target.read_bytes(), self.previous)

    def test_backup_tampering_rejected_before_restoration(self):
        result = manager.manage(self.args('backup'))
        backup = Path(result['backup'])
        backup.write_bytes(b'#!/bin/bash\necho tampered-fixture\n')
        with self.assertRaises(manager.Rejected):
            manager.manage(self.args('rollback', backup=str(backup), expected_sha=manager.digest(self.previous)))
        self.assertEqual(self.target.read_bytes(), self.previous)

    def test_post_install_failure_restores_original(self):
        original = manager.replace_runtime
        count = 0

        def fail_once(*args, **kwargs):
            nonlocal count
            count += 1
            original(*args, **kwargs)
            if count == 1:
                raise manager.Rejected('Simulated post-install verification failure')

        with mock.patch.object(manager, 'replace_runtime', side_effect=fail_once):
            with self.assertRaises(manager.Rejected):
                manager.manage(self.args('install'))
        self.assertEqual(self.target.read_bytes(), self.previous)
        self.assertTrue(manager.expected_metadata(self.target))

    def test_runtime_symlink_rejected(self):
        self.target.unlink()
        self.target.symlink_to(self.source)
        with self.assertRaises(OSError):
            manager.manage(self.args('install'))

    def test_cli_never_outputs_source_contents(self):
        result = subprocess.run(['bash', str(ROOT / 'ops/deploy/install-dpn-deploy.sh'),
                                 'validate', '--fixture-root', str(self.root),
                                 '--source', str(self.source), '--repo', str(self.repo), '--commit', self.commit,
                                 '--expected-sha', manager.digest(self.updated),
                                 '--expected-current-sha', manager.digest(self.previous)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('reviewed-fixture', result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['result'], 'VALIDATED')


if __name__ == '__main__':
    unittest.main()
