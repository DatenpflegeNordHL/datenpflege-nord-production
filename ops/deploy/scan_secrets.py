"""Offline credential-signature scan of tracked and pending repository files.

Prints paths/line numbers only, never matched values. This is a signature gate,
not a claim that arbitrary unlabeled secrets can be detected deterministically.
"""
import argparse
from pathlib import Path
import re
import subprocess

PATTERNS = {
    'private-key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    'github-token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\b'),
    'aws-access-key': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'slack-token': re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
    'stripe-live-key': re.compile(rb'\bsk_live_[A-Za-z0-9]{20,}\b'),
}

def scan(root):
    root=Path(root).resolve()
    files=subprocess.check_output(['git','-C',str(root),'ls-files','-z','--cached','--others','--exclude-standard']).split(b'\0')
    findings=[]
    for name in sorted(set(files)):
        if not name:continue
        p=root/name.decode()
        if not p.is_file():continue
        data=p.read_bytes()
        for signature,pattern in PATTERNS.items():
            for m in pattern.finditer(data):findings.append({'file':name.decode(),'line':data[:m.start()].count(b'\n')+1,'signature':signature})
    return findings

if __name__=='__main__':
    import json
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',default='.');a=p.parse_args()
    findings=scan(a.root);print(json.dumps({'result':'BLOCKER' if findings else 'PASS','scope':'tracked/pending files; credential signatures','findings':findings},indent=2))
    raise SystemExit(bool(findings))
