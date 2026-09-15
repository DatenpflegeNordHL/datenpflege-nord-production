from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ops/deploy'))
import scan_secrets

class SecretScanTests(unittest.TestCase):
    def test_pending_credentials_detected_without_values_in_findings(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);subprocess.run(['git','init','-q',d],check=True)
            token='gh'+'p_'+'A'*36
            (root/'pending.txt').write_text('fixture\n'+token)
            rows=scan_secrets.scan(root)
            self.assertEqual(rows,[{'file':'pending.txt','line':2,'signature':'github-token'}])
            self.assertNotIn(token,str(rows))
    def test_public_contact_address_is_not_a_secret(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(['git','init','-q',d],check=True)
            (Path(d)/'index.html').write_text('kontakt@datenpflege-nord.de')
            self.assertEqual(scan_secrets.scan(d),[])
