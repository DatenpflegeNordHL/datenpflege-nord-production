"""Pinned Git-source installation and backup restoration; no website activation."""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile


class Rejected(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_regular(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'Not a regular file')
        return stream.read()


def syntax(data):
    result = subprocess.run(['bash', '-n'], input=data, capture_output=True)
    require(result.returncode == 0, 'Shell syntax rejected (contents suppressed)')


def trusted_directory(path):
    require(path.is_absolute() and path.resolve() == path, 'Directory symlink rejected')
    for directory in [path, *path.parents]:
        info = directory.stat()
        # /tmp is a legitimate sticky ancestor for isolated fixtures.
        writable = info.st_mode & 0o022
        require(info.st_uid == 0 and (not writable or info.st_mode & stat.S_ISVTX),
                'Directory must be root-owned and protected from other writers')


def expected_metadata(path):
    info = path.stat()
    return info.st_uid == info.st_gid == 0 and stat.S_IMODE(info.st_mode) == 0o750


def pinned_source(args):
    require(args.source and args.repo and args.commit and args.expected_sha,
            'Explicit source, repository, full commit and expected SHA are required')
    require(re.fullmatch(r'[0-9a-f]{40}', args.commit), 'Full Git commit required')
    source = Path(args.source).absolute()
    repo = Path(args.repo).resolve(strict=True)
    require(source.resolve() == source, 'Source symlink rejected')
    relative = source.relative_to(repo).as_posix()
    command = ['git', '--no-replace-objects', '-c', 'safe.directory=' + str(repo), '-C', str(repo),
               'show', args.commit + ':' + relative]
    result = subprocess.run(command, capture_output=True)
    require(result.returncode == 0, 'Source unavailable in the specified Git commit')
    data = read_regular(source)
    require(data == result.stdout, 'Working-tree source differs from pinned Git source')
    require(digest(data) == args.expected_sha, 'Expected source SHA mismatch')
    syntax(data)
    return data


def durable_file(path, data, mode):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as stream:
        os.fchown(stream.fileno(), 0, 0)
        os.fchmod(stream.fileno(), mode)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save_backup(directory, data):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    path = directory / ('dpn-deploy.' + stamp + '.backup')
    durable_file(path, data, 0o750)
    record = {'sha256': digest(data), 'uid': 0, 'gid': 0, 'mode': '750'}
    durable_file(Path(str(path) + '.json'), (json.dumps(record) + '\n').encode(), 0o600)
    sync_directory(directory)
    require(read_regular(path) == data and expected_metadata(path), 'Backup validation failed')
    return path


def replace_runtime(target, data, validate_syntax=True):
    fd, name = tempfile.mkstemp(prefix='.dpn-deploy-stage-', dir=target.parent)
    stage = Path(name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchown(stream.fileno(), 0, 0)
            os.fchmod(stream.fileno(), 0o750)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        require(read_regular(stage) == data and expected_metadata(stage), 'Stage validation failed')
        if validate_syntax:
            syntax(read_regular(stage))
        os.replace(stage, target)
        sync_directory(target.parent)
        require(read_regular(target) == data and expected_metadata(target),
                'Installed hash or owner/mode validation failed')
    finally:
        if stage.exists():
            stage.unlink()


@contextlib.contextmanager
def locks(backups, deployment_lock):
    # Serialize script management and exclude a running deployment. Neither lock
    # is truncated or written with process metadata.
    install_fd = os.open(backups / '.install.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(install_fd, 'r+b') as install_lock:
        require(stat.S_ISREG(os.fstat(install_fd).st_mode), 'Invalid installation lock')
        os.fchmod(install_lock.fileno(), 0o600)
        fd = os.open(deployment_lock, os.O_RDWR | os.O_NOFOLLOW)
        with os.fdopen(fd, 'r+b') as deploy_lock:
            for stream in [install_lock, deploy_lock]:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield


def manage(args):
    for value in [args.expected_current_sha, args.expected_sha]:
        if value is not None:
            require(re.fullmatch(r'[0-9a-f]{64}', value), 'Full SHA-256 required')
    require(args.expected_current_sha, 'Expected current SHA is required')
    target = Path('/usr/local/sbin/dpn-deploy')
    backups = Path('/var/backups/dpn-deploy')
    deployment_lock = Path('/var/lib/dpn-deploy/deploy.lock')
    if args.fixture_root:
        root = Path(args.fixture_root).absolute()
        require(root.parent == Path('/tmp') and root.name.startswith('dpn-install-test-')
                and root.resolve() == root, 'Invalid isolated fixture root')
        target, backups, deployment_lock = root / 'runtime/dpn-deploy', root / 'backups', root / 'deploy.lock'
    trusted_directory(target.parent)
    current = read_regular(target)
    require(digest(current) == args.expected_current_sha, 'Current runtime SHA mismatch')
    source = None
    if args.action in ('validate', 'install'):
        source = pinned_source(args)
        require(expected_metadata(target), 'Runtime owner/mode differs from root:root 750')
    if args.action == 'validate':
        return {'result': 'VALIDATED', 'source_sha256': digest(source),
                'installed_sha256': digest(current), 'identity': 'MATCH' if source == current else 'MISMATCH',
                'runtime_changed': False, 'installation_performed': False}
    if args.action == 'install' and source == current:
        return {'result': 'MATCH_NOOP', 'installed_sha256': digest(current),
                'runtime_changed': False, 'installation_performed': False}
    require(os.geteuid() == 0, 'Root privileges required for backup/install/rollback')
    if not backups.exists():
        trusted_directory(backups.parent)
        backups.mkdir(mode=0o700)
    trusted_directory(backups)
    require(stat.S_IMODE(backups.stat().st_mode) == 0o700, 'Backup directory must be mode 700')
    with locks(backups, deployment_lock):
        require(read_regular(target) == current, 'Runtime changed while acquiring locks')
        if args.action == 'rollback':
            require(args.backup and args.expected_sha, 'Explicit backup and expected SHA required')
            path = Path(args.backup).absolute()
            require(path.parent == backups and path.resolve() == path, 'Backup outside trusted directory')
            source = read_regular(path)
            record = json.loads(read_regular(Path(str(path) + '.json')))
            require(digest(source) == args.expected_sha == record['sha256']
                    and expected_metadata(path) and record == {'sha256': args.expected_sha, 'uid': 0, 'gid': 0, 'mode': '750'},
                    'Backup identity/metadata mismatch')
            syntax(source)
        elif args.action == 'backup':
            require(expected_metadata(target), 'Runtime owner/mode differs from root:root 750')
            syntax(current)
        backup = save_backup(backups, current)
        if args.action != 'backup':
            try:
                replace_runtime(target, source)
            except Exception:
                # A failed bounded install is restored from its verified prior bytes.
                replace_runtime(target, current, validate_syntax=False)
                raise
        return {'result': 'BACKUP_CREATED' if args.action == 'backup' else args.action.upper() + '_VERIFIED',
                'backup': str(backup), 'previous_sha256': digest(current),
                'installed_sha256': digest(read_regular(target)), 'owner': 'root:root', 'mode': '750',
                'runtime_changed': args.action != 'backup' and source != current,
                'installation_performed': args.action != 'backup'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'backup', 'install', 'rollback'])
    for option in ['source', 'repo', 'commit', 'expected-sha', 'expected-current-sha', 'backup', 'fixture-root']:
        parser.add_argument('--' + option)
    args = parser.parse_args()
    try:
        print(json.dumps(manage(args), sort_keys=True))
    except (Rejected, OSError, ValueError, KeyError):
        # Do not print subprocess stderr, file contents or arbitrary exception values.
        print('REJECTED: identity, permissions, syntax, pinned source, backup or lock validation failed')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
