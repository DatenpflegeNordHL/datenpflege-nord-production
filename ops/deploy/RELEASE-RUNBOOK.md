# Golden deployment script and release runbook

This runbook separates script installation, release validation and website activation. None authorizes another implicitly. Never edit `/usr/local/sbin/dpn-deploy` ad hoc. `ops/deploy/dpn-deploy` is the version-controlled source; the installed executable is its runtime copy. Current canonical/runtime SHA-256: `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01`.

## Verify and update the script

1. Review a Git-source change and its exact full commit; test it and scan for secrets. Preserve the current installed hash. Any change to the canonical deployment script needs this same process. Do not install from an unreviewed working tree.
2. Supply an explicit source file, repository, full source commit, expected source SHA-256 and expected installed SHA-256 to `install-dpn-deploy.sh validate`. The helper compares source bytes with the pinned Git blob using `--no-replace-objects`, checks expected hash, and runs `bash -n` without printing contents. It rejects symlink/non-regular files. Validation does not install, acquire production locks or create backups.
3. For an explicitly authorized future update, use the same arguments with action `install`. Root privileges are required for writes. The helper validates protected root-owned target/backup directories, takes the script-management lock and existing deployment kernel lock without truncating deployment metadata, rechecks current bytes and retains a timestamped root-owned backup with a hash/metadata record.
4. It stages verified snapshot bytes in the target directory as `root:root 750`, fsyncs and validates the stage, atomically renames it onto the fixed runtime path, fsyncs the directory and rechecks installed bytes/metadata. A failed bounded installation attempts to restore the verified previous bytes and returns non-zero. Stop and inspect any failure.
5. Run `verify-dpn-deploy.sh` against the reviewed canonical source, then separately check runtime owner/group/mode. Do not invoke deployment from the installation helper. `MATCH_NOOP` avoids installation and backup/lock writes when current bytes already match; the live runtime was not replaced in this task.
6. Run the authorized `check` entrypoint against an explicitly known fetched-main target before separately authorizing activation. Preserve the script backup and previous release target/SHA for rollback. `--fixture-root` is only for protected root-owned `/tmp/dpn-install-test-*` fixtures and cannot redirect writes to the real release pointer.

Current validated source example, read-only with respect to runtime:

```bash
sudo bash ops/deploy/install-dpn-deploy.sh validate \
  --source /home/adminzander/projekte/dpn-golden-phase-1-3/ops/deploy/dpn-deploy \
  --repo /home/adminzander/projekte/dpn-golden-phase-1-3 \
  --commit 9ef0f433bfc3f988a02e97f5baa5d271cbf29a7d \
  --expected-sha d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01 \
  --expected-current-sha d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01
```

For a future approved installation, action `install` must use that update's reviewed commit and expected hashes, not blindly reuse this example. Source bytes must exactly match the specified commit even when an altered working tree has its own supplied hash.

## Script backup and rollback

A backup-only operation is explicit and never installs:

```bash
sudo bash ops/deploy/install-dpn-deploy.sh backup \
  --expected-current-sha d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01
```

Actual retained backup: `/var/backups/dpn-deploy/dpn-deploy.20260914T095215.730995Z.backup`, `root:root 750`, SHA-256 equal to the current canonical hash. Its `.json` record is root-owned mode `600`; the backup directory is mode `700`. This source contains deployment logic/path references, not secret values.

For a separately authorized real rollback, invoke action `rollback` with `--backup <retained-backup>`, `--expected-sha <previous-sha>` and `--expected-current-sha <erroneous-installed-sha>`. The helper checks backup path, protected directory, regular file, expected/recorded bytes, owner/mode and shell syntax before changing runtime. It retains the replaced runtime bytes, stages the selected backup as `root:root 750`, atomically restores it and verifies installed identity. Then run the identity verifier against the corresponding reviewed source and `bash -n` again. Stop on failure. This restores the script only; it never restores or deploys website content.

Proof on 2026-09-14: an isolated privileged fixture received a copy of the actual retained runtime backup/record; rollback restored its original SHA, `root:root 750` and valid shell syntax. All temporary fixture artifacts were cleaned. The live installed script inode, mtime, bytes, metadata and current release pointer remained unchanged. Eleven privileged fixture tests also cover install/rollback, no-op, wrong hashes, unreviewed working-tree edits, syntax failure, locks, symlinks, tampered backups and post-install failure recovery.

## Controlled deployment entrypoint validation

The actual installed mode is `check --target`, not `--check` or an invented `--dry-run`. It writes lock/fetch/cache state and a temporary archive, but never activates a release. Use a private per-run TMPDIR and a timeout. Do not restore stale lock metadata afterward or remove the production lock file; the next kernel-lock owner handles stale metadata.

On 2026-09-14 the known live target `65468e875fa0f4318cc07d7e4cbe843cacb24569` was rejected with exit 1 because fetched main had advanced to `e72e01be18a3c8ad1ed43660ef8cb88f0a981bfa`. This is correct fail-closed behavior, not a release-parity failure. The later known fetched-main target passed content/manifest/resource/exclusion validation and returned documented exit **10**, meaning deployment would be required. It was not deployed. The main change consists of four excluded research files; current public release remains tied to its original commit.

Successful validation command (recorded historical TMPDIR was created specifically for this invocation and then removed):

```bash
sudo -n env TMPDIR=/tmp/dpn-issue15-check-n3hm_q9y \
  timeout --signal=TERM --kill-after=10s 120s \
  /usr/local/sbin/dpn-deploy check \
  --target e72e01be18a3c8ad1ed43660ef8cb88f0a981bfa
```

Use a freshly created private TMPDIR for a future invocation; do not copy an expired directory name. Before/after evidence verifies unchanged pointer, release inventory, all 28 file hashes, release/global state SHA, installed script and nginx hash. Contact health remained 200 and all three services active. No new release directory was created. Exit 0 is validated target/live identity; exit 10 is validated target requiring activation; neither authorizes `deploy`. Other non-zero/timeout results require STOP and review.

## Golden asset and HTML freshness policy

Selected asset policy: **B — `?v=<full SHA-256 of final asset bytes>`**. Content-hashed filenames are also acceptable, but introducing them now would require changing the fixed filename allowlist. Query versions preserve existing names and Git-blob/package validation. No timestamps, randomness or documentation-only commit IDs are used as cache busters.

The freshness candidate implements this gate; it is not installed or released.

1. Finalize meaningful source content and leaf asset bytes. Run
   `python3 ops/deploy/check_asset_versions.py --root . --generate`.
   The public allowlist defines the production graph. HTML attributes/srcsets,
   inline CSS, literal JS module/resource URLs, CSS imports/URLs, SVG resources,
   social metadata and structured-data image URLs are inspected. Navigation,
   canonical, hreflang, API, external and fragment URLs are excluded. Dynamic
   local resource construction must be resolved to explicit URLs; arbitrary
   JavaScript execution is not inferred by an offline parser.
2. The graph is validated before writes. Deterministic sorted DFS detects cycles
   and missing/unpackaged dependencies. Dependencies are rewritten and hashed
   before their parents, using full SHA-256 of final bytes. Run generation again:
   `changed_files` must be empty and the working-tree byte snapshot unchanged.
3. OG image, favicon and apple-touch-icon receive final-byte query hashes. OG's
   existing nginx no-cache/no-store rule stays unchanged; canonical identity and
   sitemap lastmod are not changed for cache-busting alone.
4. Run all Golden/static/unit/browser gates and commit finalized source. Hosted
   CI checks out the exact head commit, not a synthetic PR merge, and repeats
   the generator/checker, isolated nginx and browser tests, privileged install
   fixtures, signature secret scan and exact-archive package verification.
5. `python3 ops/deploy/verify_release_candidate.py --repo . --commit <full-sha>`
   extracts a local Git archive, rejects non-finalized versions, runs Golden
   checks, builds the allowlisted package, runs canonical deploy validators,
   then computes the final-byte manifest. No mutation is permitted after it.
   The version-controlled deployment validator stages the checker from the
   pinned target Git object and checks versions BEFORE Git-blob manifest parity.
   No generated file or checker is added to the public webroot.
6. Never run the live deployment entrypoint for a candidate. Issue #10 remains
   mandatory: main protection must actually be enforced before Golden release.
   An updated deploy executable itself requires separate reviewed installation.

HTML candidate and browser acceptance instructions are in
`ops/nginx/FRESHNESS-CANDIDATE.md`. No production nginx or media configuration
has been changed. Future edge acceptance must repeat the tests through the
actual public release URL; local origin tests cannot prove CDN overrides.

Read-only edge evidence: at the sampled WAW POP, the content-version query was MISS then HIT; a distinct deterministic probe label was MISS. All bodies remained the current CSS bytes. This demonstrates sampled query-key separation, not a universal management-rule guarantee or a changed asset rollout.

Current release: all 19 static/media inventory entries use category C stable paths; 18 normal referenced assets lack content versions, while OG is deliberately no-cache and exempt. Most normal assets have seven-day public TTL; MP4 has observed public four-hour TTL and no explicit origin cache directive. Current-version checker returns expected exit 1/BLOCKER for 61 references. This known release-safety gap remains unresolved on the live site because no website source migration/deployment occurs here.

Selected HTML policy: explicit browser **revalidation before reuse**, retaining ETag/Last-Modified for efficient 304s (normally `Cache-Control: no-cache`, not mandatory `no-store`). Any server/CDN configuration implementation requires separate review and explicit approval; preserve security-header inheritance and contact/OG routing. Current DYNAMIC responses lack explicit freshness control, and Chromium default fetches reused HTML locally. Conditional origin/public HTML requests correctly returned 304, but no upper bound for ordinary browser reuse across a future deployment was proven. Do not claim absent Cache-Control itself proves a present content defect, or that DYNAMIC is equivalent to no-cache. HTML freshness acceptance remains OPEN; no nginx patch/reload was applied.

robots: the observed transformed Cloudflare response has four-hour max-age; this bounded indexing delay is accepted for ordinary public crawl-policy updates. Do not use robots caching as a secrets/publication boundary. Critical indexing policy changes require separately verified freshness before activation. No Cloudflare change is needed for today's acceptance.

sitemap: dynamic delivery, validators and origin/public 304s are accepted for ordinary indexing cadence; no multi-day explicit TTL was observed. Preserve canonical URLs and accurate source metadata. Browser-freshness improvements may include sitemap in a future reviewed revalidation change; this is not a current sitemap blocker.

OG: retain the intentional `no-cache, no-store, must-revalidate` policy and observed BYPASS. 404 and health are accepted with current correct statuses/MIME and dynamic delivery. Never send a real contact request for a smoke test.

## Current close gate

Runtime source identity, update tooling, actual entrypoint validation, script rollback proof, current release/manifest parity, secret/contact separation and sampled security/transformation handling are PASS. **Issue #15 remains OPEN only for live asset content-version migration and bounded HTML-freshness acceptance.** Current caches do not prove current content drift; they fail or leave open the required future-release freshness contract. A documentation/checker commit cannot substitute for deploying approved versioned references or approving the HTML policy.

Issue #10 remains OPEN and unchanged; hosted tests are not private-main protection. No merge, website activation, Cloudflare or contact-backend change is authorized by this runbook.
