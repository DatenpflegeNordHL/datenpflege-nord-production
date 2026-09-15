# P0 signed production release control — candidate evidence

Date: 2026-09-15. Parent freshness RC:
`f47ce765a7dca5c4679f28abfac18acd18db229b` (unchanged).

Selected signing: dedicated operator-held Ed25519 SSH signing key. Approved public
fingerprint: `SHA256:p1CAcez9terd2KEdDg42uAEAe3K+aEJMPhFTKH1222U`. The private
key is mode 600 under the operator's `~/.ssh`, outside Git and server trust files.
An actual isolated tag signed by this operator key passed Git and release-gate
verification against the committed public allowed-signers source.

Tag convention: `dpn-release-YYYYMMDD-HHMMSSZ` in UTC, annotated, signed and
monotonically recorded. Remote tag object and peeled target must match. Fetch is
non-force. Root-owned immutable records bind tag object and target. Reuse with a
moved object, malformed/non-monotonic name, unsigned/lightweight tag or an
unapproved signer fails closed.

CI is checked through GitHub's authenticated Actions API using a repository-only
fine-grained token (Metadata read + Actions read) at a fixed root-owned mode-600
path outside Git. The token is read in-process and never printed. Evidence must
be exact target SHA on `main`, completed/success, the fixed Static site audit
workflow and push/manual event. Feature-branch success does not authorize a
production release.

`dpn-deploy check` remains non-activating and needs no release tag. `authorize`
is non-activating but requires tag/SHA/signature/CI. `deploy` requires the same
and repeats authorization before immutable recording. The target must equal the
fetched origin/main tip. Existing asset/package/exact-blob manifest checks run;
identity is recorded only after final package validation and before service
checks/symlink activation. Invalid package after valid authorization fails.

Test matrix: valid signed tag PASS; unsigned, wrong signer, wrong target, target
outside origin/main, malformed SHA, missing/failed/wrong-branch CI, valid CI plus
invalid signature, valid signature plus invalid package, moved/non-monotonic tag
and untagged deploy all FAIL as required. Fixtures use temporary Git repositories,
temporary signing keys, injected CI JSON and no production secrets/network.
Root installation fixtures target only protected `/tmp/dpn-release-gate-test-*`.

No automatic deployment path was found in repository workflows, GitHub webhooks
or repository Actions secrets. The production server has a pre-existing timer
whose unit invokes `/usr/local/sbin/dpn-deploy deploy` without required arguments.
Observed runs exit 64 at usage validation before fetch/package/activation. It is
not push-driven and cannot deploy under either current or candidate CLI. It was
not stopped, restarted or edited in this task. Before accepting Issue #10, the
obsolete timer/unit should be disabled or replaced with an explicitly inert
check-only design to remove ambiguity and repeated failed units.

Candidate status: source and local isolated controls validated. Production is
NOT yet compensated because the installed deploy script/trust root were not
changed. Required before Issue #10 reclassification: exact-commit Hosted CI,
reviewed root installation of gate and updated dpn-deploy, external CI token
provisioning, obsolete timer disposition, and server-side non-deploying positive
and negative authorization acceptance. Until all complete: **Issue #10 OPEN P0**.

No production deployment performed. No merge to main performed. Repository
remains private. GitHub Team is not required by the proposed compensating-control
model, but that model is not accepted until production-boundary activation.
