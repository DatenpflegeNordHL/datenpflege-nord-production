#!/usr/bin/env python3
"""Fail-closed signed-tag and exact-SHA Hosted CI production authorization.

The CLI has no fixture/bypass option. Tests call pure functions with isolated
Git repositories and injected CI responses. No deployment is performed here.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TAG_RE = re.compile(r'dpn-release-(\d{8})-(\d{6})Z\Z')
SHA_RE = re.compile(r'[0-9a-f]{40}\Z')
RECORD_RE = re.compile(r'dpn-release-\d{8}-\d{6}Z\.json\Z')

class GateError(RuntimeError): pass

def git(git_dir, *args, check=True):
    result=subprocess.run(['git',f'--git-dir={git_dir}',*args],capture_output=True,text=True)
    if check and result.returncode:raise GateError('git verification failed: '+' '.join(args))
    return result

def validate_tag_name(tag):
    match=TAG_RE.fullmatch(tag)
    if not match:raise GateError('release tag must match dpn-release-YYYYMMDD-HHMMSSZ')
    try:datetime.strptime(''.join(match.groups()),'%Y%m%d%H%M%S')
    except ValueError as e:raise GateError('release tag has invalid UTC date/time') from e

def secure_file(path, *, owner=0, mode_max=0o644, nonempty=True):
    path=Path(path)
    try:info=path.lstat()
    except OSError as e:raise GateError(f'required trust file unavailable: {path}') from e
    if not stat.S_ISREG(info.st_mode) or info.st_uid!=owner or stat.S_IMODE(info.st_mode)&~mode_max:
        raise GateError(f'insecure trust file owner/type/mode: {path}')
    if nonempty and info.st_size==0:raise GateError(f'empty trust file: {path}')

def secure_directory(path, *, owner=0):
    path=Path(path)
    try:info=path.lstat()
    except OSError as e:raise GateError(f'record directory unavailable: {path}') from e
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=owner or stat.S_IMODE(info.st_mode)&0o022:
        raise GateError(f'insecure record directory owner/type/mode: {path}')

def verify_tag(git_dir,tag,target,allowed_signers,records_dir,enforce_permissions=True):
    if not SHA_RE.fullmatch(target):raise GateError('target must be a full lowercase 40-character SHA')
    validate_tag_name(tag)
    git_dir=Path(git_dir);allowed_signers=Path(allowed_signers);records_dir=Path(records_dir)
    if enforce_permissions:
        secure_file(allowed_signers,mode_max=0o644);secure_directory(records_dir)
    if git(git_dir,'cat-file','-t',f'refs/tags/{tag}',check=False).stdout.strip()!='tag':
        raise GateError('release tag missing or not annotated')
    tag_object=git(git_dir,'rev-parse',f'refs/tags/{tag}').stdout.strip()
    resolved=git(git_dir,'rev-parse',f'refs/tags/{tag}^{{commit}}').stdout.strip()
    if resolved!=target:raise GateError('release tag does not resolve to expected target')
    if git(git_dir,'cat-file','-e',f'{target}^{{commit}}',check=False).returncode:
        raise GateError('target commit does not exist')
    if git(git_dir,'merge-base','--is-ancestor',target,'refs/remotes/origin/main',check=False).returncode:
        raise GateError('target is not in fetched origin/main history')
    result=git(git_dir,'-c','gpg.format=ssh','-c',f'gpg.ssh.allowedSignersFile={allowed_signers}',
               'verify-tag',f'refs/tags/{tag}',check=False)
    if result.returncode:raise GateError('tag signature is invalid or signer is not approved')
    record=records_dir/f'{tag}.json'
    if record.exists():
        if enforce_permissions:secure_file(record,mode_max=0o600)
        try:prior=json.loads(record.read_text())
        except (OSError,json.JSONDecodeError) as e:raise GateError('recorded release identity is invalid') from e
        if {key:prior.get(key) for key in ('tag','tag_object','target')}!={'tag':tag,'tag_object':tag_object,'target':target}:
            raise GateError('release tag moved from recorded identity')
    return {'tag':tag,'tag_object':tag_object,'target':target}

def select_ci_run(payload,target,workflow_path='.github/workflows/site-audit.yml'):
    runs=payload.get('workflow_runs') if isinstance(payload,dict) else None
    if not isinstance(runs,list):raise GateError('GitHub CI response is malformed')
    matches=[r for r in runs if r.get('head_sha')==target and r.get('head_branch')=='main'
             and r.get('path')==workflow_path and r.get('status')=='completed'
             and r.get('conclusion')=='success' and r.get('event') in {'push','workflow_dispatch'}]
    if not matches:raise GateError('no successful approved Hosted CI run for exact target SHA on main')
    run=max(matches,key=lambda r:(r.get('run_number',0),r.get('id',0)))
    return {'ci_run_id':run.get('id'),'ci_run_number':run.get('run_number'),
            'ci_head_sha':target,'ci_workflow':workflow_path,'ci_conclusion':'success'}

def fetch_ci(token_file,repo_slug,target,workflow_path,enforce_permissions=True,opener=urlopen):
    token_file=Path(token_file)
    if enforce_permissions:secure_file(token_file,mode_max=0o600)
    token=token_file.read_text().strip()
    if not token or '\n' in token:raise GateError('CI token file is empty or malformed')
    query=urlencode({'head_sha':target,'status':'completed','per_page':100})
    request=Request(f'https://api.github.com/repos/{repo_slug}/actions/runs?{query}',headers={
        'Accept':'application/vnd.github+json','Authorization':f'Bearer {token}',
        'X-GitHub-Api-Version':'2022-11-28','User-Agent':'dpn-release-gate/1'})
    try:
        with opener(request,timeout=15) as response:payload=json.load(response)
    except Exception as e:raise GateError('authenticated GitHub CI evidence retrieval failed') from e
    return select_ci_run(payload,target,workflow_path)

def record_identity(identity,records_dir,enforce_permissions=True):
    records_dir=Path(records_dir)
    if enforce_permissions:secure_directory(records_dir)
    validate_tag_name(identity['tag'])
    existing=sorted(p.stem for p in records_dir.iterdir() if RECORD_RE.fullmatch(p.name))
    if existing and identity['tag']<existing[-1]:raise GateError('release tag is older than the latest recorded release')
    destination=records_dir/f"{identity['tag']}.json"
    body=json.dumps(identity,sort_keys=True,separators=(',',':'))+'\n'
    if destination.exists():
        try:prior=json.loads(destination.read_text())
        except (OSError,json.JSONDecodeError) as e:raise GateError('recorded release identity is invalid') from e
        if {key:prior.get(key) for key in ('tag','tag_object','target')}!={key:identity.get(key) for key in ('tag','tag_object','target')}:raise GateError('release tag moved from recorded identity')
        return destination
    fd,temp=tempfile.mkstemp(prefix='.release-tag-',dir=records_dir)
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,'w') as stream:stream.write(body);stream.flush();os.fsync(stream.fileno())
        os.link(temp,destination);os.unlink(temp)
        directory_fd=os.open(records_dir,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(directory_fd)
        finally:os.close(directory_fd)
    except Exception:
        try:os.unlink(temp)
        except OSError:pass
        raise
    return destination

def authorize(args):
    identity=verify_tag(args.git_dir,args.tag,args.target,args.allowed_signers,args.records_dir)
    ci=fetch_ci(args.ci_token,args.repo_slug,args.target,args.workflow_path)
    result={**identity,**ci,'result':'PASS'}
    if args.record:record_identity({**identity,**ci},args.records_dir)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--git-dir',required=True);p.add_argument('--tag',required=True);p.add_argument('--target',required=True)
    p.add_argument('--allowed-signers',default='/etc/dpn-deploy/release-signers.allowed')
    p.add_argument('--records-dir',default='/var/lib/dpn-deploy/release-tags')
    p.add_argument('--ci-token',default='/etc/dpn-deploy/github-ci-token')
    p.add_argument('--repo-slug',default='DatenpflegeNordHL/datenpflege-nord-production')
    p.add_argument('--workflow-path',default='.github/workflows/site-audit.yml');p.add_argument('--record',action='store_true')
    a=p.parse_args()
    try:print(json.dumps(authorize(a),sort_keys=True))
    except GateError as e:print(f'BLOCKER: {e}');return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
