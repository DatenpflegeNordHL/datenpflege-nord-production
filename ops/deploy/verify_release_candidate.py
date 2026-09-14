"""Verify an exact local Git archive with canonical validators; no deployment.

Generation must already be committed. Reject an archive that would change on
regeneration. The manifest is created only after all package gates pass.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import tempfile
import check_asset_versions as assets


def verify(repo, commit):
    repo=Path(repo).resolve()
    commit=subprocess.check_output(['git','-C',str(repo),'rev-parse',commit+'^{commit}'],text=True).strip()
    with tempfile.TemporaryDirectory(prefix='dpn-rc-') as d:
        root=Path(d)
        source=root/'source';source.mkdir()
        archive=subprocess.check_output(['git','-C',str(repo),'archive',commit])
        subprocess.run(['tar','-x','-C',str(source)],input=archive,check=True)
        pinned=source/'ops/deploy/check_asset_versions.py'
        result=subprocess.run(['python3',str(pinned),'--root',str(source),'--generate'],capture_output=True,text=True,check=True)
        report=json.loads(result.stdout)
        if report['changed_files']:raise ValueError('Archive is not finalized: '+str(report['changed_files']))
        for audit in ['site_audit.py','golden_audit.py']:
            subprocess.run(['python3',str(source/'scripts'/audit)],check=True,capture_output=True,text=True)
        public=assets.public_files(source)
        package=root/'package';package.mkdir()
        for p in public:
            dest=package/p.relative_to(source);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        script=(source/'ops/deploy/dpn-deploy').read_text()
        definitions=root/'definitions.sh'
        definitions.write_text(script.split('install -d -m 700 "$RELEASE_STATE_DIR"\n')[0])
        gitdir=subprocess.check_output(['git','-C',str(repo),'rev-parse','--absolute-git-dir'],text=True).strip()
        code='source "$1" check --target "$2"\nCACHE="$3"\nSELECTED_PUBLIC_FILES=('+ ' '.join(shlex.quote(p.relative_to(source).as_posix()) for p in public)+')\nvalidate_release "$4"\n'
        subprocess.run(['bash','-c',code,'candidate',str(definitions),commit,gitdir,str(package)],check=True,capture_output=True,text=True)
        # Final byte manifest; nothing mutates the package after this point.
        manifest={p.relative_to(package).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.rglob('*')) if p.is_file()}
        assert all(hashlib.sha256((package/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
        return {'result':'PASS','commit':commit,'reference_count':report['reference_count'],'manifest':manifest,'post_manifest_mutations':0}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',default='.');p.add_argument('--commit',required=True);a=p.parse_args()
    print(json.dumps(verify(a.repo,a.commit),indent=2))
