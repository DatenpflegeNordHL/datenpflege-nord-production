import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'ops/deploy/check_asset_versions.py'
spec = importlib.util.spec_from_file_location('asset_versions', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class AssetVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.css = self.root / 'style.css'
        self.css.write_text('body { color: black; }\n')
        self.sha = hashlib.sha256(self.css.read_bytes()).hexdigest()

    def html(self, reference):
        (self.root / 'index.html').write_text('<link href="' + reference + '">')

    def test_valid_version_and_changed_bytes_require_new_version(self):
        self.html('/style.css?v=' + self.sha)
        self.assertEqual(checker.inspect(self.root)[0]['result'], 'PASS')
        self.css.write_text('body { color: white; }\n')
        self.assertEqual(checker.inspect(self.root)[0]['result'], 'BLOCKER')

    def test_stable_random_and_duplicate_versions_fail(self):
        for value in ['/style.css', '/style.css?v=random', '/style.css?v=' + self.sha + '&v=' + self.sha]:
            self.html(value)
            self.assertEqual(checker.inspect(self.root)[0]['result'], 'BLOCKER')

    def test_content_addressed_filename(self):
        name = 'style.' + self.sha[:16] + '.css'
        self.css.rename(self.root / name)
        self.html('/' + name)
        self.assertEqual(checker.inspect(self.root)[0]['result'], 'PASS')

    def test_css_dependency_and_html_version_both_checked(self):
        image = self.root / 'profile.webp'
        image.write_bytes(b'fixture-image')
        image_sha = hashlib.sha256(image.read_bytes()).hexdigest()
        self.css.write_text('body { background: url("/profile.webp?v=' + image_sha + '"); }')
        css_sha = hashlib.sha256(self.css.read_bytes()).hexdigest()
        self.html('/style.css?v=' + css_sha)
        rows = checker.inspect(self.root)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row['result'] == 'PASS' for row in rows))
        image.write_bytes(b'changed-image')
        self.assertEqual(checker.inspect(self.root)[1]['result'], 'BLOCKER')

    def test_data_external_and_special_og_do_not_require_version(self):
        (self.root / 'index.html').write_text('<img src="data:image/png;base64,AA">'
                                            '<img src="https://external.invalid/a.png">'
                                            '<img src="/og-datenpflege-nord.png">')
        self.assertEqual(checker.inspect(self.root), [])

    def test_missing_asset_is_blocker_and_files_are_not_modified(self):
        self.html('/missing.js?v=' + '0' * 64)
        before = self.css.stat().st_mtime_ns
        self.assertEqual(checker.inspect(self.root)[0]['result'], 'BLOCKER')
        self.assertEqual(self.css.stat().st_mtime_ns, before)


if __name__ == '__main__':
    unittest.main()
