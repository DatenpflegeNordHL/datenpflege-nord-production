"""Finalized Git archive/package checks without production entrypoint execution."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ops/deploy'))
import check_asset_versions as assets
import verify_release_candidate as verifier

class ReleaseCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='dpn-package-test-')
        self.addCleanup(self.temp.cleanup);self.repo=Path(self.temp.name)
        files=assets.public_files(ROOT)+[ROOT/p for p in ['ops/deploy/dpn-deploy','ops/deploy/check_asset_versions.py','scripts/site_audit.py','scripts/golden_audit.py']]
        for p in files:
            dest=self.repo/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.repo),*args],text=True).strip()
    def commit(self):self.git('add','.');self.git('commit','-qm','fixture');return self.git('rev-parse','HEAD')
    def test_finalized_archive_manifest_and_no_mutation(self):
        result=verifier.verify(self.repo,self.commit())
        self.assertEqual(result['result'],'PASS');self.assertEqual(result['reference_count'],79)
        self.assertEqual(result['post_manifest_mutations'],0);self.assertEqual(len(result['manifest']),28)
        self.assertEqual(self.git('status','--porcelain'),'')
    def test_unfinalized_archive_is_not_packaged(self):
        (self.repo/'assets/home.css').write_text('body{color:purple}')
        with self.assertRaisesRegex(ValueError,'not finalized'):verifier.verify(self.repo,self.commit())
    def test_missing_dependency_rejected(self):
        (self.repo/'favicon.svg').unlink()
        with self.assertRaises(subprocess.CalledProcessError):verifier.verify(self.repo,self.commit())

if __name__=='__main__':unittest.main()
