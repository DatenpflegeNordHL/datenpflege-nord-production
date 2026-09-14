#!/usr/bin/env bash
# Explicit script management only; never runs dpn-deploy or nginx.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/manage_dpn_deploy.py" "$@"
