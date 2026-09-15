"""Read-only verifier behavior, using isolated fixture files only."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


VERIFIER = Path(__file__).resolve().parents[1] / 'ops/deploy/verify-dpn-deploy.sh'


class DeployIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.verifier = self.root / VERIFIER.name
        shutil.copyfile(VERIFIER, self.verifier)
        self.canonical = self.root / 'dpn-deploy'
        self.canonical.write_bytes(b'fixture deployment logic\n')
        self.installed = self.root / 'installed'
        self.installed.write_bytes(self.canonical.read_bytes())

    def run_verifier(self, *args):
        return subprocess.run(['bash', str(self.verifier), *args],
                              capture_output=True, text=True)

    def test_match_does_not_modify_files(self):
        before = self.installed.stat()
        result = self.run_verifier('--installed', str(self.installed))
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.endswith('MATCH\n'))
        self.assertEqual(self.installed.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(self.installed.read_bytes(), self.canonical.read_bytes())

    def test_mismatch_never_prints_contents_or_overwrites(self):
        content = b'sensitive-fixture-value-not-for-output\n'
        self.installed.write_bytes(content)
        result = self.run_verifier('--installed', str(self.installed))
        self.assertEqual(result.returncode, 1)
        self.assertTrue(result.stdout.endswith('MISMATCH\n'))
        self.assertNotIn(content.decode().strip(), result.stdout + result.stderr)
        self.assertEqual(self.installed.read_bytes(), content)

    def test_missing_installed_is_unknown(self):
        result = self.run_verifier('--installed', str(self.root / 'missing'))
        self.assertEqual(result.returncode, 3)
        self.assertIn('UNKNOWN: installed', result.stdout)

    def test_missing_canonical_is_unknown(self):
        self.canonical.unlink()
        result = self.run_verifier('--installed', str(self.installed))
        self.assertEqual(result.returncode, 3)
        self.assertIn('UNKNOWN: canonical', result.stdout)

    @unittest.skipIf(os.geteuid() == 0, 'root bypasses file read permission')
    def test_permission_denied_is_distinct(self):
        self.installed.chmod(0)
        result = self.run_verifier('--installed', str(self.installed))
        self.assertEqual(result.returncode, 2)
        self.assertIn('PERMISSION_DENIED: installed; identity UNKNOWN', result.stdout)

    def test_invalid_arguments(self):
        result = self.run_verifier('--install', str(self.installed))
        self.assertEqual(result.returncode, 64)


if __name__ == '__main__':
    unittest.main()
