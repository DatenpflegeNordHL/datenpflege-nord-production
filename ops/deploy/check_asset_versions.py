"""Read-only release gate for content-hash filenames or ?v=<asset SHA-256>."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urljoin, urlsplit


ASSET_SUFFIXES = {'.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif',
                  '.ico', '.woff', '.woff2', '.mp4'}
NO_STORE_PATHS = {'og-datenpflege-nord.png'}


def inspect(root):
    root = Path(root).resolve(strict=True)
    rows = []

    def reference(source, value):
        base = 'https://datenpflege-nord.de/' + source.relative_to(root).as_posix()
        url = urlsplit(urljoin(base, value.strip()))
        if url.scheme not in ('http', 'https') or url.hostname != 'datenpflege-nord.de':
            return
        relative = unquote(url.path).lstrip('/')
        candidate = (root / relative).resolve()
        if not candidate.is_relative_to(root):
            raise ValueError('Reference leaves source root')
        if candidate.suffix.lower() not in ASSET_SUFFIXES or relative in NO_STORE_PATHS:
            return
        if not candidate.is_file():
            rows.append({'source': source.relative_to(root).as_posix(), 'asset': relative,
                         'classification': 'C', 'result': 'BLOCKER', 'reason': 'missing asset'})
            return
        digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        token = re.search(r'\.([0-9a-f]{16,64})\.', candidate.name)
        query = parse_qs(url.query).get('v', [])
        category = 'A' if token else 'B' if query else 'C'
        valid = bool(token and digest.startswith(token.group(1))) or query == [digest]
        rows.append({'source': source.relative_to(root).as_posix(), 'asset': relative,
                     'classification': category, 'expected_sha256': digest,
                     'result': 'PASS' if valid else 'BLOCKER',
                     'reason': 'content identity version verified' if valid else 'stable URL or incorrect content version'})

    class References(HTMLParser):
        def __init__(self, source):
            super().__init__()
            self.source = source

        def handle_starttag(self, tag, attrs):
            for name, value in attrs:
                if value and name in ('src', 'href', 'data-src', 'poster'):
                    reference(self.source, value)
                elif value and name == 'srcset' and not value.startswith('data:'):
                    for entry in value.split(','):
                        reference(self.source, entry.strip().split()[0])

    for source in sorted(root.rglob('*.html')):
        References(source).feed(source.read_text())
    for source in sorted(root.rglob('*.css')):
        text = source.read_text()
        for value in re.findall(r'url\(\s*[\x22\x27]?([^\x22\x27)]+)', text):
            reference(source, value)
        for value in re.findall(r'@import\s+[\x22\x27]([^\x22\x27]+)', text):
            reference(source, value)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    try:
        rows = inspect(args.root)
    except (OSError, ValueError):
        print('BLOCKER: source root or asset reference cannot be validated')
        return 2
    passed = bool(rows) and all(row['result'] == 'PASS' for row in rows)
    print(json.dumps({'result': 'PASS' if passed else 'BLOCKER', 'references': rows}, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
