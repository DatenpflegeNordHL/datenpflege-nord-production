#!/usr/bin/env bash
set -euo pipefail
[ "${EUID:-$(id -u)}" -eq 0 ] || { echo 'Root required.' >&2; exit 77; }
[ "$#" -eq 7 ] || [ "$#" -eq 9 ] || { echo 'Usage: install-release-gate.sh install <release_gate.py> <allowed-signers> <repo> <commit> <expected-code-sha256> <expected-signers-sha256> [--fixture-root /tmp/dpn-release-gate-test-*]' >&2; exit 64; }
[ "$1" = install ] || exit 64
SOURCE="$2"; SIGNERS="$3"; REPO="$4"; COMMIT="$5"; EXPECTED_CODE="$6"; EXPECTED_SIGNERS="$7"; PREFIX=""
if [ "$#" -eq 9 ]; then
    [ "$8" = --fixture-root ] || exit 64
    PREFIX="$(realpath -e "$9")"
    case "$PREFIX" in /tmp/dpn-release-gate-test-*) ;; *) echo 'Invalid isolated fixture root.' >&2; exit 64 ;; esac
    [ -d "$PREFIX" ] && [ ! -L "$PREFIX" ] && [ "$(stat -c '%U:%a' "$PREFIX")" = root:700 ] || { echo 'Unsafe fixture root.' >&2; exit 1; }
fi
[[ "$COMMIT" =~ ^[0-9a-f]{40}$ ]] || exit 64
[ -d "$REPO" ] && [ "$(git --no-replace-objects -C "$REPO" cat-file -t "$COMMIT" 2>/dev/null)" = commit ] || { echo 'Unreviewed commit.' >&2; exit 1; }
REPO="$(realpath -e "$REPO")"; SOURCE="$(realpath -e "$SOURCE")"; SIGNERS="$(realpath -e "$SIGNERS")"
case "$SOURCE" in "$REPO"/*) CODE_REL="${SOURCE#"$REPO"/}" ;; *) echo 'Code source outside reviewed repository.' >&2; exit 1 ;; esac
case "$SIGNERS" in "$REPO"/*) SIGNERS_REL="${SIGNERS#"$REPO"/}" ;; *) echo 'Signer source outside reviewed repository.' >&2; exit 1 ;; esac
[ "$(git --no-replace-objects -C "$REPO" rev-parse "$COMMIT:$CODE_REL" 2>/dev/null)" = "$(git hash-object "$SOURCE")" ] || { echo 'Code does not match reviewed commit.' >&2; exit 1; }
[ "$(git --no-replace-objects -C "$REPO" rev-parse "$COMMIT:$SIGNERS_REL" 2>/dev/null)" = "$(git hash-object "$SIGNERS")" ] || { echo 'Signer list does not match reviewed commit.' >&2; exit 1; }
[[ "$EXPECTED_CODE" =~ ^[0-9a-f]{64}$ && "$EXPECTED_SIGNERS" =~ ^[0-9a-f]{64}$ ]] || exit 64
[ -f "$SOURCE" ] && [ ! -L "$SOURCE" ] && [ -f "$SIGNERS" ] && [ ! -L "$SIGNERS" ] || { echo 'Invalid source.' >&2; exit 1; }
[ "$(sha256sum "$SOURCE" | cut -d' ' -f1)" = "$EXPECTED_CODE" ] || { echo 'Code hash mismatch.' >&2; exit 1; }
[ "$(sha256sum "$SIGNERS" | cut -d' ' -f1)" = "$EXPECTED_SIGNERS" ] || { echo 'Signer hash mismatch.' >&2; exit 1; }
PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/dpn-release-gate-pycache" python3 -m py_compile "$SOURCE"
[ "$(grep -Ec '^dpn-release namespaces="git" ssh-ed25519 [A-Za-z0-9+/=]+([[:space:]].*)?$' "$SIGNERS")" -ge 1 ] || { echo 'Invalid allowed-signers format.' >&2; exit 1; }
[ "$(grep -Evc '^(dpn-release namespaces="git" ssh-ed25519 [A-Za-z0-9+/=]+([[:space:]].*)?|[[:space:]]*)$' "$SIGNERS")" -eq 0 ] || { echo 'Unexpected allowed-signers entry.' >&2; exit 1; }
LIB="$PREFIX/usr/local/lib/dpn-deploy"; ETC="$PREFIX/etc/dpn-deploy"; STATE="$PREFIX/var/lib/dpn-deploy/release-tags"
install -d -o root -g root -m 755 "$LIB"
install -d -o root -g root -m 700 "$ETC" "$STATE"
CODE_TMP="$(mktemp "$LIB/.release_gate.py.XXXXXX")"; SIGNER_TMP="$(mktemp "$ETC/.release-signers.XXXXXX")"
trap 'rm -f "$CODE_TMP" "$SIGNER_TMP"' EXIT
install -o root -g root -m 755 "$SOURCE" "$CODE_TMP"
install -o root -g root -m 644 "$SIGNERS" "$SIGNER_TMP"
mv -fT "$CODE_TMP" "$LIB/release_gate.py"; mv -fT "$SIGNER_TMP" "$ETC/release-signers.allowed"
trap - EXIT
[ "$(stat -c '%U:%G:%a' "$LIB/release_gate.py")" = root:root:755 ]
[ "$(stat -c '%U:%G:%a' "$ETC/release-signers.allowed")" = root:root:644 ]
[ "$(find "$ETC" -type f | wc -l)" -eq 1 ] # The private key/token are never installed from repository sources.
