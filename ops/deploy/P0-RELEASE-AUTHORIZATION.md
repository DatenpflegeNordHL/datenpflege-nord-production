# P0 production release authorization

## Hard invariant

There is no automatic production deployment on a push to `main`. GitHub Actions
runs validation only. Production activation is an explicit operator invocation
of the root-owned installed `dpn-deploy`. `check` remains a non-activating
package check; `authorize` is a non-activating release-authorization check.
Only `deploy` can switch `/srv/datenpflege-nord/current`, and it now requires both
`--target <full-sha>` and `--release-tag <tag>`.

GitHub-native private-repository branch protection is unavailable under the
chosen GitHub Free organization plan. The repository remains private. This
control compensates at the production boundary; it does not claim protected
Git history or prevent a direct push to `main`.

## Signing and release tags

Signing uses a dedicated Ed25519 SSH signing key, separate from GitHub/deploy SSH
authentication. Operator private key:
`~/.ssh/dpn_release_signing_ed25519` (mode 600; never committed or installed on
the server). Approved public fingerprint:
`SHA256:p1CAcez9terd2KEdDg42uAEAe3K+aEJMPhFTKH1222U`.
Only the public key is in `release-signers.allowed`.

Convention: `dpn-release-YYYYMMDD-HHMMSSZ`, UTC and lexically monotonic. Tags are
annotated, SSH-signed and created only after a human reviews successful Hosted
CI for the exact commit on `main`. Never reuse, delete/recreate, move, or force
push a release tag.

```bash
TARGET=<reviewed-full-40-character-main-sha>
TAG="dpn-release-$(date -u +%Y%m%d-%H%M%SZ)"
git tag -s -a "$TAG" "$TARGET" -m "Production release approval for $TARGET"
git verify-tag "$TAG"
git push origin "refs/tags/$TAG"
```

A tag is explicit human approval. The server checks the remote annotated object
and peeled target before fetching without force. It verifies annotation type,
full SHA, exact target, membership in fetched `origin/main`, SSH signature and
approved principal. Root-owned records bind tag name, tag-object SHA and target;
a mismatch or non-monotonic tag fails closed.

## Server trust root and CI evidence

Install only after source review and Hosted CI. `install-release-gate.sh` requires an exact reviewed Git commit, verifies both Git blobs and pinned SHA-256 values, and installs:

- `/usr/local/lib/dpn-deploy/release_gate.py`: root:root 755;
- `/etc/dpn-deploy/release-signers.allowed`: root:root 644, public keys only;
- `/var/lib/dpn-deploy/release-tags`: root:root 700, records mode 600.

The dedicated operator private key stays off the server. Rotation adds a newly
reviewed public key before first use and installs the reviewed signer-file hash.
Remove an old key only after its rollback/re-verification window ends. Existing
immutable identity records remain. Never populate allowed signers dynamically
from GitHub account keys.

CI truth is retrieved server-side from GitHub's authenticated Actions API. A
repository-scoped fine-grained token needs only Metadata read and Actions read.
Provision it interactively as `/etc/dpn-deploy/github-ci-token`, root:root 600,
outside Git and shell arguments. The gate reads it directly and never prints it.
No production credential is used in tests.

Accepted CI evidence must be `completed/success`, exact `head_sha`, branch
`main`, workflow `.github/workflows/site-audit.yml`, and event `push` or explicit
`workflow_dispatch`. Feature-branch CI alone is insufficient. API failure,
missing evidence, another SHA/branch/workflow or failed CI blocks authorization.

## Deployment chain

1. Commit finalized source; Hosted CI passes for the exact SHA on `main`.
2. Human reviews that run and creates/pushes a new signed annotated release tag.
3. `dpn-deploy authorize --target "$TARGET" --release-tag "$TAG"` performs a
   read-only authorization check.
4. Operator separately invokes `dpn-deploy deploy --target "$TARGET"
   --release-tag "$TAG"`.
5. The root deployment lock is acquired; main and the exact remote tag are
   fetched; signature/trust/CI checks pass.
6. Existing asset, package, local-reference and exact Git-blob manifest gates
   pass. Release metadata equals the target.
7. Authorization is rechecked and the immutable tag identity is recorded.
8. Existing service checks pass; only then may the release symlink change.

An untagged commit, lightweight/unsigned/wrong-signer tag, wrong target, missing
CI or invalid package cannot activate production. `verify-release-tag.sh` is a
convenience wrapper for the non-deploying installed `authorize` entrypoint.

## Acceptance status

Source implementation and isolated fixtures can establish candidate readiness.
Issue #10 becomes **ACCEPTED RISK / COMPENSATED** only after exact-commit Hosted
CI passes, the reviewed gate/deploy script and explicit trust root are installed,
the external CI token is provisioned securely, and a server-side non-deploying
acceptance proves fail-closed behavior. Until then production still runs the old
entrypoint and Issue #10 remains OPEN P0. Installing controls is not deployment,
but still requires the separate reviewed installation procedure.
