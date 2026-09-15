#!/usr/bin/env bash
set -euo pipefail
[ "$#" -eq 2 ] || { echo "Usage: verify-release-tag.sh <release-tag> <full-target-sha>" >&2; exit 64; }
exec /usr/local/sbin/dpn-deploy authorize --target "$2" --release-tag "$1"
