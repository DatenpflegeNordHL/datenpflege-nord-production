"""Isolated signed-tag, CI and production-gate matrix; no network/secrets."""
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ops/deploy'))
import release_gate as gate

class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='dpn-release-gate-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.repo=self.root/'repo';self.repo.mkdir();self.records=self.root/'records';self.records.mkdir()
        self.git('init','-q');self.git('config','user.name','Release Fixture');self.git('config','user.email','fixture@example.invalid')
        (self.repo/'index.html').write_text('valid package\n');self.git('add','.');self.git('commit','-qm','target')
        self.target=self.git('rev-parse','HEAD');self.git('update-ref','refs/remotes/origin/main',self.target)
        self.key=self.root/'approved';self.other=self.root/'wrong'
        for key,comment in [(self.key,'approved'),(self.other,'wrong')]:subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-C',comment,'-f',str(key)],check=True)
        self.allowed=self.root/'allowed';self.allowed.write_text('dpn-release namespaces="git" '+(self.key.with_suffix('.pub')).read_text())
        self.tag='dpn-release-20260915-120000Z';self.sign(self.tag,self.target,self.key)
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.repo),*args],text=True).strip()
    def sign(self,tag,target,key):
        subprocess.run(['git','-C',str(self.repo),'-c','gpg.format=ssh','-c',f'user.signingkey={key}','tag','-s','-a','-m','explicit human release approval',tag,target],check=True,capture_output=True)
    def verify(self,tag=None,target=None,allowed=None):return gate.verify_tag(self.repo/'.git',tag or self.tag,target or self.target,allowed or self.allowed,self.records,False)
    def good_ci(self,**changes):
        run={'id':42,'run_number':7,'head_sha':self.target,'head_branch':'main','path':'.github/workflows/site-audit.yml','status':'completed','conclusion':'success','event':'push'}
        run.update(changes);return {'workflow_runs':[run]}
    def test_valid_signed_release_tag_and_ci_pass(self):
        identity=self.verify();ci=gate.select_ci_run(self.good_ci(),self.target)
        self.assertEqual(identity['target'],self.target);self.assertEqual(ci['ci_run_id'],42)
    def test_unsigned_tag_fails(self):
        self.git('tag','unsigned',self.target)
        with self.assertRaisesRegex(gate.GateError,'match|annotated'):self.verify('unsigned')
        self.git('tag','unsigned-release',self.target)
        self.git('tag','dpn-release-20260915-120001Z',self.target)
        with self.assertRaisesRegex(gate.GateError,'annotated'):self.verify('dpn-release-20260915-120001Z')
    def test_wrong_signer_fails(self):
        allowed=self.root/'wrong-allowed';allowed.write_text('wrong namespaces="git" '+self.other.with_suffix('.pub').read_text())
        with self.assertRaisesRegex(gate.GateError,'signature'):self.verify(allowed=allowed)
    def test_tag_points_to_wrong_sha_fails(self):
        (self.repo/'next').write_text('next');self.git('add','.');self.git('commit','-qm','next');other=self.git('rev-parse','HEAD')
        with self.assertRaisesRegex(gate.GateError,'resolve'):self.verify(target=other)
    def test_sha_not_on_origin_main_fails(self):
        (self.repo/'next').write_text('next');self.git('add','.');self.git('commit','-qm','next');other=self.git('rev-parse','HEAD')
        tag='dpn-release-20260915-120001Z';self.sign(tag,other,self.key)
        with self.assertRaisesRegex(gate.GateError,'origin/main'):self.verify(tag,other)
    def test_malformed_sha_fails(self):
        for sha in ['abc',self.target.upper(),self.target+'0']:
            with self.subTest(sha=sha),self.assertRaisesRegex(gate.GateError,'full lowercase'):self.verify(target=sha)
    def test_missing_and_failed_ci_fail(self):
        for payload in [{'workflow_runs':[]},self.good_ci(conclusion='failure'),self.good_ci(head_sha='0'*40),self.good_ci(head_branch='feature')]:
            with self.subTest(payload=payload),self.assertRaisesRegex(gate.GateError,'no successful'):gate.select_ci_run(payload,self.target)
    def test_valid_ci_and_invalid_signature_fails(self):
        self.assertEqual(gate.select_ci_run(self.good_ci(),self.target)['ci_conclusion'],'success')
        with self.assertRaises(gate.GateError):self.verify(allowed=self.root/'missing')
    def test_valid_signature_and_invalid_package_fails_closed(self):
        self.verify();(self.repo/'index.html').write_text('tampered package\n')
        expected=self.git('rev-parse',self.target+':index.html')
        actual=subprocess.check_output(['git','hash-object',str(self.repo/'index.html')],text=True).strip()
        self.assertNotEqual(expected,actual)
    def test_record_rejects_moved_tag_and_nonmonotonic_new_tag(self):
        identity={**self.verify(),**gate.select_ci_run(self.good_ci(),self.target)};gate.record_identity(identity,self.records,False)
        self.git('tag','-d',self.tag);(self.repo/'next').write_text('next');self.git('add','.');self.git('commit','-qm','next');other=self.git('rev-parse','HEAD');self.git('update-ref','refs/remotes/origin/main',other);self.sign(self.tag,other,self.key)
        with self.assertRaisesRegex(gate.GateError,'moved'):self.verify(target=other)
        older={'tag':'dpn-release-20260915-115959Z','tag_object':'a'*40,'target':'b'*40}
        with self.assertRaisesRegex(gate.GateError,'older'):gate.record_identity(older,self.records,False)
    def test_ci_fetch_uses_token_without_printing_it(self):
        token=self.root/'token';token.write_text('private-fixture-token')
        class Response(io.BytesIO):
            def __enter__(self):return self
            def __exit__(self,*args):pass
        captured={}
        def opener(request,timeout):captured['authorization']=request.headers['Authorization'];return Response(json.dumps(self.good_ci()).encode())
        result=gate.fetch_ci(token,'owner/repo',self.target,'.github/workflows/site-audit.yml',False,opener)
        self.assertEqual(result['ci_run_id'],42);self.assertEqual(captured['authorization'],'Bearer private-fixture-token');self.assertNotIn('private-fixture-token',str(result))
    def test_trust_permissions_fail_closed(self):
        with self.assertRaises(gate.GateError):
            gate.verify_tag(self.repo/'.git',self.tag,self.target,self.allowed,self.records,True)

class DeployGateContractTests(unittest.TestCase):
    def test_untagged_deploy_rejected_and_authorization_precedes_package_activation(self):
        script=(ROOT/'ops/deploy/dpn-deploy').read_text()
        result=subprocess.run(['bash',str(ROOT/'ops/deploy/dpn-deploy'),'deploy','--target','0'*40],capture_output=True,text=True)
        self.assertEqual(result.returncode,64)
        self.assertLess(script.index('fetch_and_verify_release_authorization\nfi'),script.index('create_release\n'))
        self.assertLess(script.rindex('validate_release "$NEW"'),script.index('record_release_authorization\ncheck_services'))
        self.assertLess(script.index('record_release_authorization\ncheck_services'),script.index('ln -s "$NEW" "$CURRENT.new"'))
    def test_no_push_workflow_can_deploy(self):
        workflows='\n'.join(p.read_text() for p in (ROOT/'.github/workflows').glob('*'))
        self.assertNotRegex(workflows,r'(?m)^\s*(?:sudo\s+)?(?:/usr/local/sbin/)?dpn-deploy\s+deploy\b')
        self.assertNotIn('/srv/datenpflege-nord/current',workflows)

if __name__=='__main__':unittest.main()
