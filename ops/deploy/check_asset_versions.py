"""Offline final-byte SHA-256 gate and deterministic static dependency generator.

Scans the public release allowlist, never ops/evidence or documentation. For
fixtures/extracted packages without dpn-deploy, scans the supplied root instead.
Literal URL syntax is supported; dynamic local resource construction fails closed.
"""
import argparse
from dataclasses import dataclass
import hashlib
import html
import json
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urljoin, urlsplit, urlunsplit, urlencode

ASSET_SUFFIXES = {'.css', '.js', '.mjs', '.svg', '.png', '.jpg', '.jpeg', '.webp',
                  '.gif', '.avif', '.ico', '.woff', '.woff2', '.ttf', '.otf',
                  '.mp4', '.webm', '.mp3', '.wav', '.ogg', '.pdf', '.json', '.wasm',
                  '.webmanifest', '.csv', '.bin'}
ORIGIN = 'https://datenpflege-nord.de/'
STRINGS = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|(?P<q>[\x22\x27`])(?P<value>(?:\\.|(?!(?P=q))[\s\S])*?)(?P=q)')
ATTRS = re.compile(r'([\w:-]+)\s*=\s*([\x22\x27])(.*?)\2', re.S)
CSS = re.compile(r'url\(\s*(?:([\x22\x27])(.*?)\1|([^\s)]+))\s*\)|@import\s+([\x22\x27])(.*?)\4', re.S | re.I)

@dataclass
class Reference:
    source: Path
    start: int
    end: int
    value: str
    kind: str
    context: str = 'resource'
    escaped: bool = False


def public_files(root):
    script = root / 'ops/deploy/dpn-deploy'
    if script.is_file():
        block = script.read_text().split('ALLOWED_PUBLIC_FILES=(', 1)[1].split('\n)', 1)[0]
        return [root / p for p in re.findall(r'"([^"]+)"', block) if (root / p).is_file()]
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(
        part.startswith('.') or part == '__pycache__' for part in p.relative_to(root).parts))


def literals(source, text, offset, kind):
    for m in STRINGS.finditer(text):
        if m.group('value') is not None:
            yield Reference(source, offset+m.start('value'), offset+m.end('value'),
                            m.group('value'), kind)


def css_refs(source, text, offset=0):
    # Mask comments without shifting source coordinates.
    text = re.sub(r'/\*[\s\S]*?\*/', lambda m: ' ' * len(m[0]), text)
    for m in CSS.finditer(text):
        group = next(i for i in (2, 3, 5) if m.group(i) is not None)
        yield Reference(source, offset+m.start(group), offset+m.end(group), m.group(group), 'CSS')


def references(source):
    text = source.read_bytes().decode('utf-8')
    if source.suffix in {'.js', '.mjs', '.json'}:
        yield from literals(source, text, 0, 'JS' if source.suffix != '.json' else 'metadata')
    elif source.suffix == '.xml':
        for m in re.finditer(r'<loc>(.*?)</loc>',text,re.S):
            yield Reference(source,m.start(1),m.end(1),m[1],'sitemap','excluded',True)
    elif source.suffix == '.css':
        yield from css_refs(source, text)
    elif source.suffix in {'.html', '.svg'}:
        # Mask HTML comments to avoid generating dead dependencies.
        masked = re.sub(r'<!--[\s\S]*?-->', lambda m: ' '*len(m[0]), text)
        for tag in re.finditer(r'<([\w:-]+)\b[^>]*>', masked):
            attrs = {m.group(1).lower(): html.unescape(m.group(3)) for m in ATTRS.finditer(tag[0])}
            name = tag.group(1).lower()
            if name == 'base':raise ValueError(f'{source}: HTML base override requires explicit URL resolution')
            for m in ATTRS.finditer(tag[0]):
                key, value = m.group(1).lower(), m.group(3)
                start = tag.start()+m.start(3)
                if key in {'src','href','xlink:href','data-src','poster','action'}:
                    excluded = key == 'action' or (name == 'link' and
                        bool(set(attrs.get('rel','').split()) & {'canonical','alternate'}))
                    yield Reference(source,start,start+len(value),value,'HTML',
                                    'excluded' if excluded else 'resource',True)
                elif key in {'srcset','data-srcset'} and not value.startswith('data:'):
                    for item in re.finditer(r'(?:^|,)\s*([^\s,]+)',value):
                        yield Reference(source,start+item.start(1),start+item.end(1),item[1],'HTML',escaped=True)
                elif key == 'content' and name == 'meta' and attrs.get('property',attrs.get('name')) in {'og:image','og:image:url','og:image:secure_url','twitter:image','twitter:image:src'}:
                    yield Reference(source,start,start+len(value),value,'metadata',escaped=True)
                elif key == 'style':
                    yield from css_refs(source,value,start)
        for m in re.finditer(r'<(script|style)\b([^>]*)>([\s\S]*?)</\1\s*>',masked,re.I):
            if m[1].lower() == 'style':
                yield from css_refs(source,m[3],m.start(3))
            else:
                yield from literals(source,m[3],m.start(3),'metadata' if 'ld+json' in m[2] else 'JS')


def target(root, ref):
    value = html.unescape(ref.value) if ref.escaped else ref.value
    if '\\' in value:
        value = value.replace('\\/', '/')
    if not value.strip():return None,[],None
    url = urlsplit(urljoin(ORIGIN+ref.source.relative_to(root).as_posix(),value.strip()))
    query = [v for k,v in parse_qsl(url.query,keep_blank_values=True) if k == 'v']
    external = url.scheme not in {'http','https'} or url.netloc != 'datenpflege-nord.de'
    if external or value.startswith('#'):
        if any(re.fullmatch('[0-9a-f]{64}',v) for v in query):
            return None,query,'excluded URL incorrectly versioned'
        return None,query,None
    relative = unquote(url.path).lstrip('/')
    path = (root/relative).resolve()
    if not path.is_relative_to(root):
        return None,query,'reference leaves public root'
    if ref.kind == 'JS' and '${' in value and value.startswith(('/assets/','/images/','./assets/','./images/','../assets/','../images/')):
        return path,query,'dynamic local resource URL needs explicit literal resolution'
    resource = ref.context != 'excluded' and not url.path.startswith('/api/') and path.suffix.lower() in ASSET_SUFFIXES
    if not resource:
        return None,query,'excluded/navigation/API URL incorrectly versioned' if query else None
    if '${' in value or '\\' in value:
        return path,query,'dynamic or escaped resource URL needs explicit literal resolution'
    return path,query,None


def inventory(root):
    files = public_files(root)
    refs = []
    for source in files:
        if source.suffix.lower() in {'.html','.css','.js','.mjs','.json','.svg','.xml'}:
            refs.extend(references(source))
    return files,refs


def dependency_order(root, files, refs):
    graph = {p:set() for p in files}
    for ref in refs:
        path,_,error = target(root,ref)
        if error:
            raise ValueError(f'{ref.source.relative_to(root)} -> {ref.value}: {error}')
        if path:
            if not path.is_file() or path not in graph:
                raise ValueError(f'{ref.source.relative_to(root)} -> {ref.value}: missing/unpackaged asset')
            graph[ref.source].add(path)
    result,active,done = [],[],set()
    def visit(node):
        if node in active:
            raise ValueError('dependency cycle: '+' -> '.join(str(p.relative_to(root)) for p in active+[node]))
        if node in done:return
        active.append(node)
        for child in sorted(graph[node]):visit(child)
        active.pop();done.add(node);result.append(node)
    for node in sorted(graph):visit(node)
    return result,graph


def generate(root):
    root = Path(root).resolve(strict=True)
    files,refs = inventory(root)
    order,_ = dependency_order(root,files,refs) # Validate entire graph before writes.
    changes=[]
    for source in order:
        selected = [r for r in refs if r.source == source and target(root,r)[0]]
        if not selected:continue
        text = source.read_bytes().decode('utf-8')
        for ref in sorted(selected,key=lambda r:r.start,reverse=True):
            path,_,_ = target(root,ref)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            value = html.unescape(ref.value) if ref.escaped else ref.value
            value = value.replace('\\/', '/')
            url = urlsplit(value)
            query = [(k,v) for k,v in parse_qsl(url.query,keep_blank_values=True) if k != 'v']
            query.append(('v',digest))
            replacement = urlunsplit((url.scheme,url.netloc,url.path,urlencode(query),url.fragment))
            if ref.escaped:replacement=html.escape(replacement,quote=False)
            text=text[:ref.start]+replacement+text[ref.end:]
        if text != source.read_bytes().decode('utf-8'):
            source.write_bytes(text.encode('utf-8'));changes.append(source.relative_to(root).as_posix())
    return changes


def inspect(root):
    root=Path(root).resolve(strict=True)
    files,refs=inventory(root)
    rows=[]
    for ref in refs:
        path,versions,error=target(root,ref)
        if path is None and not error:continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest() if path and path.is_file() else None
        if path and path not in files:error='missing/unpackaged asset'
        valid=not error and digest is not None and versions == [digest]
        rows.append({'source':ref.source.relative_to(root).as_posix(),
            'asset':path.relative_to(root).as_posix() if path else ref.value,
            'classification':'B' if versions else 'C','kind':ref.kind,
            'expected_sha256':digest,'observed_version':versions,
            'result':'PASS' if valid else 'BLOCKER',
            'reason':error or ('verified final-byte SHA-256' if valid else 'missing asset' if digest is None else 'missing/malformed/incorrect version')})
    try:dependency_order(root,files,refs)
    except ValueError as e:
        rows.append({'source':'dependency graph','asset':str(e),'expected_sha256':None,
                     'observed_version':None,'result':'BLOCKER','reason':'inconsistent dependencies'})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    parser.add_argument('--generate',action='store_true')
    args=parser.parse_args()
    try:
        changed=generate(args.root) if args.generate else []
        rows=inspect(args.root)
        passed=bool(rows) and all(r['result']=='PASS' for r in rows)
        print(json.dumps({'result':'PASS' if passed else 'BLOCKER','changed_files':changed,'reference_count':len(rows),'references':rows},indent=2))
        return 0 if passed else 1
    except (OSError,ValueError) as e:
        print(json.dumps({'result':'BLOCKER','error':str(e)}));return 2

if __name__ == '__main__':raise SystemExit(main())
