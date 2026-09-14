"""Exercise canonical release validators in a temporary Git repository.

The deployment entrypoint is never run: only definitions preceding its first
state-directory write are loaded, with all paths replaced by test fixtures.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'ops/deploy/dpn-deploy'


class DeployContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.release = self.root / 'release'
        self.repo.mkdir()
        self.release.mkdir()
        content = {'index.html': '<html><title>Fixture</title><h1>Fixture</h1>'
                   '<link href="/style.css"><script src="/app.js"></script></html>\n',
                   'style.css': 'body { color: black; }\n', 'app.js': 'void 0;\n'}
        for name, text in content.items():
            (self.repo / name).write_text(text)
            (self.release / name).write_text(text)
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'fixture')
        self.target = self.git('rev-parse', 'HEAD').stdout.strip()
        script = SCRIPT.read_text()
        boundary = 'install -d -m 700 "$RELEASE_STATE_DIR"\n'
        self.assertEqual(script.count(boundary), 1)
        self.definitions = self.root / 'definitions.sh'
        self.definitions.write_text(script.split(boundary)[0])

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args],
                              capture_output=True, text=True, check=True)

    def validate(self, command):
        code = ('source "$1" check --target "$2"\n'
                'CACHE="$3/.git"; TARGET="$2"\n'
                'SELECTED_PUBLIC_FILES=(index.html style.css app.js)\n' + command)
        return subprocess.run(['bash', '-c', code, 'fixture', str(self.definitions),
                               self.target, str(self.repo), str(self.release)],
                              capture_output=True, text=True)

    def test_exact_manifest_and_local_references(self):
        result = self.validate('check_release_manifest "$4"; check_local_references "$4"')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tampered_blob_rejected(self):
        (self.release / 'app.js').write_text('tampered;\n')
        result = self.validate('check_release_manifest "$4"')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('entspricht nicht TARGET', result.stderr)

    def test_extra_file_rejected(self):
        (self.release / 'private.txt').write_text('fixture\n')
        result = self.validate('check_release_manifest "$4"')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Allowlist', result.stderr)

    def test_symlink_and_secret_filename_rejected(self):
        link = self.release / 'link'
        link.symlink_to('app.js')
        self.assertNotEqual(self.validate('check_forbidden_files "$4"').returncode, 0)
        link.unlink()
        (self.release / '.env').write_text('fixture\n')
        self.assertNotEqual(self.validate('check_forbidden_files "$4"').returncode, 0)

    def test_manifest_order_does_not_affect_validation(self):
        result = self.validate('SELECTED_PUBLIC_FILES=(app.js index.html style.css); '
                               'check_release_manifest "$4"; check_local_references "$4"')
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
