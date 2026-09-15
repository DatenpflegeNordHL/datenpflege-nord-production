"""Root metadata tests for the release trust root, only under protected /tmp fixtures."""
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'ops/deploy/install-release-gate.sh';CODE=ROOT/'ops/deploy/release_gate.py';SIGNERS=ROOT/'ops/deploy/release-signers.allowed';COMMIT=subprocess.check_output(['git','-C',ROOT,'rev-parse','HEAD'],text=True).strip()
@unittest.skipUnless(os.geteuid()==0,'root metadata proof requires isolated privileged test run')
class ReleaseGateInstallTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='dpn-release-gate-test-',dir='/tmp');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.root.chmod(0o700)
 def digest(self,p):return hashlib.sha256(p.read_bytes()).hexdigest()
 def install(self,code=CODE,signers=SIGNERS,code_hash=None,signers_hash=None):
  return subprocess.run(['bash',str(SCRIPT),'install',str(code),str(signers),str(ROOT),COMMIT,code_hash or self.digest(code),signers_hash or self.digest(signers),'--fixture-root',str(self.root)],capture_output=True,text=True)
 def test_root_owned_trust_install_contains_only_public_material(self):
  result=self.install();self.assertEqual(result.returncode,0,result.stderr)
  expected={self.root/'usr/local/lib/dpn-deploy/release_gate.py':'root:root:755',self.root/'etc/dpn-deploy/release-signers.allowed':'root:root:644'}
  for path,mode in expected.items():self.assertEqual(subprocess.check_output(['stat','-c','%U:%G:%a',path],text=True).strip(),mode)
  self.assertFalse(any(self.root.rglob('*PRIVATE*')));self.assertFalse((self.root/'etc/dpn-deploy/github-ci-token').exists())
  self.assertEqual(subprocess.check_output(['stat','-c','%U:%G:%a',self.root/'var/lib/dpn-deploy/release-tags'],text=True).strip(),'root:root:700')
 def test_wrong_hashes_fail_before_install(self):
  self.assertNotEqual(self.install(code_hash='0'*64).returncode,0);self.assertFalse((self.root/'etc').exists())
  self.assertNotEqual(self.install(signers_hash='0'*64).returncode,0);self.assertFalse((self.root/'etc').exists())
 def test_unreviewed_private_or_unexpected_signer_input_rejected(self):
  bad=self.root/'bad';bad.write_text('-----BEGIN OPENSSH '+'PRIVATE KEY-----\n')
  self.assertNotEqual(self.install(signers=bad).returncode,0);self.assertFalse((self.root/'etc').exists())
 def test_fixture_escape_rejected(self):
  result=subprocess.run(['bash',str(SCRIPT),'install',str(CODE),str(SIGNERS),str(ROOT),COMMIT,self.digest(CODE),self.digest(SIGNERS),'--fixture-root','/tmp'],capture_output=True,text=True)
  self.assertEqual(result.returncode,64)
