import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'ops/deploy/check_asset_versions.py'
spec = importlib.util.spec_from_file_location('asset_versions', SCRIPT)
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
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

    def test_missing_wrong_malformed_duplicate_versions_fail(self):
        for value in ['/style.css', '/style.css?v=random','/style.css?v='+ '0'*64,
                      '/style.css?v='+self.sha+'&v='+self.sha]:
            with self.subTest(value=value):
                self.html(value)
                row=checker.inspect(self.root)[0]
                self.assertEqual(row['result'],'BLOCKER')
                self.assertEqual(row['expected_sha256'],self.sha)
                self.assertIn('observed_version',row)

    def test_full_query_required_even_for_hashed_filename(self):
        name='style.'+self.sha[:16]+'.css'
        self.css.rename(self.root/name)
        self.html('/'+name)
        self.assertEqual(checker.inspect(self.root)[0]['result'],'BLOCKER')
        checker.generate(self.root)
        self.assertEqual(checker.inspect(self.root)[0]['result'],'PASS')

    def test_dependency_order_changed_leaf_and_unchanged_url(self):
        (self.root/'leaf.png').write_bytes(b'first-image')
        (self.root/'fixed.png').write_bytes(b'unchanged-image')
        (self.root/'child.css').write_text('body{background:url("leaf.png")}')
        self.css.write_text('@import "child.css";body{background:url(fixed.png)}')
        (self.root/'app.js').write_text('import "./module.mjs";fetch("./data.json");')
        (self.root/'module.mjs').write_text('export const image=new URL("./leaf.png",import.meta.url);')
        (self.root/'data.json').write_text('{"image":"/leaf.png"}')
        self.html('/style.css')
        (self.root/'index.html').write_text((self.root/'index.html').read_text()+'<script src="app.js"></script>')
        checker.generate(self.root)
        self.assertTrue(all(r['result']=='PASS' for r in checker.inspect(self.root)))
        original=(self.root/'index.html').read_text()
        fixed=hashlib.sha256((self.root/'fixed.png').read_bytes()).hexdigest()
        (self.root/'leaf.png').write_bytes(b'new-image')
        checker.generate(self.root)
        self.assertNotEqual(original,(self.root/'index.html').read_text())
        self.assertIn('fixed.png?v='+fixed,self.css.read_text())
        self.assertTrue(all(r['result']=='PASS' for r in checker.inspect(self.root)))

    def test_idempotence_including_bytes_and_mtime(self):
        self.html('/style.css?theme=light#section')
        checker.generate(self.root)
        before={p:(p.read_bytes(),p.stat().st_mtime_ns) for p in self.root.iterdir()}
        self.assertEqual(checker.generate(self.root),[])
        self.assertEqual(before,{p:(p.read_bytes(),p.stat().st_mtime_ns) for p in self.root.iterdir()})
        self.assertIn('theme=light&amp;v='+self.sha+'#section',(self.root/'index.html').read_text())

    def test_cycle_fails_before_writes(self):
        self.html('/style.css')
        self.css.write_text('@import "other.css";')
        (self.root/'other.css').write_text('@import "style.css";')
        before={p:p.read_bytes() for p in self.root.iterdir()}
        with self.assertRaisesRegex(ValueError,'cycle'):checker.generate(self.root)
        self.assertEqual(before,{p:p.read_bytes() for p in self.root.iterdir()})
        self.assertTrue(any(r['source']=='dependency graph' for r in checker.inspect(self.root)))

    def test_missing_asset_fails_before_writes(self):
        self.html('/style.css')
        self.css.write_text('body{background:url(missing.png)}')
        before=self.css.read_bytes()
        with self.assertRaisesRegex(ValueError,'missing'):checker.generate(self.root)
        self.assertEqual(before,self.css.read_bytes())
        self.assertTrue(any(r['result']=='BLOCKER' for r in checker.inspect(self.root)))

    def test_navigation_api_canonical_hreflang_fragments_external_excluded(self):
        html_path=self.root/'index.html'
        html_path.write_text('<a href="/en/">EN</a><form action="/api/contact"></form>'
          '<link rel="canonical" href="https://datenpflege-nord.de/">'
          '<link rel="alternate" hreflang="en" href="/en/">'
          '<img src="data:image/png;base64,AA"><img src="https://external.invalid/a.png">'
          '<a href="#top">top</a>')
        before=html_path.read_bytes()
        checker.generate(self.root)
        self.assertEqual(before,html_path.read_bytes())
        self.assertEqual(checker.inspect(self.root),[])
        for url in ['/en/?v='+self.sha,'/api/contact?v='+self.sha,'#top?v='+self.sha]:
            if url.startswith('#'):continue
            html_path.write_text('<a href="'+url+'">test</a>')
            self.assertEqual(checker.inspect(self.root)[0]['result'],'BLOCKER')
        html_path.write_text('<link rel="canonical" href="/style.css?v='+self.sha+'">')
        self.assertEqual(checker.inspect(self.root)[0]['result'],'BLOCKER')

    def test_social_icons_schema_srcset_inline_css_and_svg(self):
        (self.root/'image.png').write_bytes(b'img')
        (self.root/'logo.svg').write_text('<svg><image href="image.png"/></svg>')
        (self.root/'index.html').write_text('<link rel="icon" href="logo.svg">'
         '<meta property="og:image" content="https://datenpflege-nord.de/image.png">'
         '<img srcset="image.png 1x, image.png 2x" data-src="image.png" poster="image.png">'
         '<style>p{background:url("image.png")}</style>'
         '<script type="application/ld+json">{"image":"/image.png","url":"https://datenpflege-nord.de/"}</script>')
        checker.generate(self.root)
        rows=checker.inspect(self.root)
        self.assertEqual(len(rows),9)
        self.assertTrue(all(r['result']=='PASS' for r in rows))

    def test_og_requires_byte_hash_but_its_cache_policy_is_separate(self):
        (self.root/'og-datenpflege-nord.png').write_bytes(b'og')
        self.html('/og-datenpflege-nord.png?v=20260908-3')
        self.assertEqual(checker.inspect(self.root)[0]['result'],'BLOCKER')
        checker.generate(self.root)
        self.assertEqual(checker.inspect(self.root)[0]['result'],'PASS')

    def test_dynamic_local_resource_fails_and_sitemap_is_never_versioned(self):
        (self.root/'app.js').write_text('fetch(`/assets/${name}`)')
        with self.assertRaisesRegex(ValueError,'dynamic'):checker.generate(self.root)
        (self.root/'app.js').unlink()
        (self.root/'sitemap.xml').write_text('<urlset><url><loc>https://datenpflege-nord.de/?v='+self.sha+'</loc></url></urlset>')
        self.assertEqual(checker.inspect(self.root)[0]['result'],'BLOCKER')

    def test_comments_and_empty_js_literals_are_not_dependencies(self):
        (self.root/'app.js').write_text('/* "missing.png" */const empty=""; // "missing.js"\n')
        self.html('/style.css')
        checker.generate(self.root)
        self.assertEqual(checker.generate(self.root),[])

if __name__=='__main__':unittest.main()
