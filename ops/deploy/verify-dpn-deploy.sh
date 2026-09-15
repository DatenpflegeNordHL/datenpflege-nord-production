#!/usr/bin/env bash
# Read-only identity check. Never installs or executes the deployment script.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INSTALLED=/usr/local/sbin/dpn-deploy
if [[ $# -ne 0 ]]; then
    if [[ $# -ne 2 || $1 != --installed ]]; then
        echo 'Usage: verify-dpn-deploy.sh [--installed PATH]' >&2
        exit 64
    fi
    INSTALLED=$2
fi

python3 - "$SCRIPT_DIR/dpn-deploy" "$INSTALLED" <<'PY'
import hashlib
import sys

hashes = []
for role, name in zip(('canonical', 'installed'), sys.argv[1:]):
    try:
        digest = hashlib.sha256()
        with open(name, 'rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
    except PermissionError:
        print(f'PERMISSION_DENIED: {role}; identity UNKNOWN')
        sys.exit(2)
    except OSError:
        print(f'UNKNOWN: {role} unavailable or unreadable')
        sys.exit(3)
    hashes.append(digest.hexdigest())
    print(f'{role}_sha256={hashes[-1]}')
if hashes[0] != hashes[1]:
    print('MISMATCH')
    sys.exit(1)
print('MATCH')
PY
