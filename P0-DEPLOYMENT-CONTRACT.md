# P0 Deployment Source of Truth and Release Parity

Observation date: **2026-09-14**, including final operational validation. **Issue #15: OPEN; closure is not recommended yet. Redirect P0: CLOSED. Issue #10: OPEN and unchanged.**

This evidence/tooling change is confined to `golden-p0-infra-evidence`, starting from `fde492b1a2efcc4a9b1b4ff922e36da4d619065c`. It does not change the frozen Phase 1–3 branch, runtime deployment script, release pointer, website content, nginx, Cloudflare or contact backend. The current task explicitly selects the canonical Git source as source of truth; future installations still require exact-source review and separate production authorization. Earlier deployment-contract capture is preserved in Git history.

## Canonical source decision

The canonical repository representation is **`ops/deploy/dpn-deploy`**, copied byte-identically from the installed production runtime after a complete 409-line review and literal-secret screening. No stronger existing version-controlled operations source was found in this checkout. The installed script is the current runtime truth; the repository baseline now makes that implementation reviewable and versionable in the existing private repository.

| Representation | SHA-256 | Decision |
| --- | --- | --- |
| Canonical `ops/deploy/dpn-deploy` | `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01` | Initial canonical baseline, preserving actual runtime bytes and behavior |
| Installed `/usr/local/sbin/dpn-deploy` | `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01` | Unchanged; privileged read-only identity MATCH |
| Local `/home/adminzander/projekte/datenpflege-nord-production/scripts/dpn-deploy` | `7e818ca2c76a2767a4b3887d0add25df98e66544e42e989fc16f1ee3e097e2e7` | Still untracked in its checkout; not substituted for runtime |

Installed metadata: `root:root`, mode `750`, 17000 bytes, 409 lines. The repository script is executable (`100755`); production installation must explicitly apply `root:root` / `750` rather than inheriting checkout ownership/mode.

The exact difference is only ordering of `assets/profile-card.css` and `assets/profile/dustin-zander.webp` inside `ALLOWED_PUBLIC_FILES`. Allowlist membership is identical (28 entries), and bytes outside that array are identical. No functional deployment difference has been identified from this ordering change: the allowlist is iterated to select files and the release inventory is sorted for manifest validation. The files are **not byte-identical**. Neither original was modified or overwritten. The precise diff and identities are recorded in `ops/evidence/issue15-controls-20260914.json`.

No passwords, private keys, Cloudflare tokens or environment secret values were found in the complete runtime source. Required references to `/etc/dpn-deploy/id_ed25519` and `/etc/dpn-deploy/known_hosts` are file paths, not secret contents. No secret file contents were displayed, versioned or included in reports. The authorized check-mode Git fetch uses the existing SSH key through the unchanged runtime command. `ops/`, tests, docs, backend and operational secrets remain outside the closed public-file allowlist.

## Installation identity and intentional update contract

`Repository Source of Truth → ops/deploy/dpn-deploy → reviewed commit + expected SHA-256 → installed /usr/local/sbin/dpn-deploy → runtime identity verification → explicitly approved deployment execution`

`ops/deploy/verify-dpn-deploy.sh` hashes its adjacent canonical script and the installed runtime without executing either script, installing anything or writing production files. Default installed path: `/usr/local/sbin/dpn-deploy`; `--installed PATH` supports isolated verification fixtures.

| Result | Exit code | Meaning |
| --- | ---: | --- |
| MATCH | 0 | Both readable byte identities agree |
| MISMATCH | 1 | Both readable, but SHA-256 differs; do not deploy |
| PERMISSION_DENIED / identity UNKNOWN | 2 | A script cannot be read due to permissions; not a mismatch |
| UNKNOWN | 3 | Missing file or other read failure; not a match |
| Usage error | 64 | Invalid arguments |

Only hashes/status are printed; file contents are never printed. Verification does not automatically elevate privileges. `sudo bash ops/deploy/verify-dpn-deploy.sh` was used read-only here and returned MATCH; ordinary-account permission denial is covered separately by fixture tests. Ownership/mode are verified separately because matching bytes alone do not establish installation permissions.

A future intentional update must follow all steps. The new helper was validated against the live source without installation; backup/rollback proof used a retained privileged backup and isolated fixtures, never a live replacement:

1. Change the canonical repository source in a reviewable branch. Never silently edit `/usr/local/sbin/dpn-deploy` directly.
2. Run shell syntax checks, verifier tests, canonical release-validator tests and secret review. Changes to activation/cleanup require isolated failure/rollback tests as well.
3. Obtain review and approval of the exact source commit. Evidence-branch publication is not approval for a production install or merge.
4. Record the expected script SHA-256 from that commit and the currently installed hash/metadata.
5. With explicit production authorization, preserve the existing runtime bytes/metadata as a separately dated rollback copy, stage the approved script, verify its hash, then install atomically as `root:root`, mode `750`. Do not install from an untracked checkout copy.
6. Run the privileged identity verifier against the approved source and verify owner/group/mode after installation. Stop on MISMATCH or UNKNOWN.
7. Run an explicitly authorized `dpn-deploy check --target <approved-main-sha>` and review its result before any deployment execution. Exit 0 means target/live metadata and full manifest agree; exit 10 means a deployment is required; other non-zero results are failures.
8. Preserve the old script plus expected hash and previous release metadata. If installation/dry-run validation fails, restore the saved script under the same owner/mode and reverify identity. A website release rollback is separate from a script installation rollback.

**Important:** `dpn-deploy check` writes bounded lock/fetch/cache state and a temporary archive; it never activates a release. It has now been exercised under a private TMPDIR and a 120-second timeout. The old live target was correctly rejected because fetched main advanced; the known fetched-main target `e72e01be18a3c8ad1ed43660ef8cb88f0a981bfa` passed target archive/manifest/resource/exclusion validation with documented exit 10 (deployment required), without deployment. The five actual runtime validators previously passed the unchanged live release read-only.

The canonical baseline, verifier and explicit `install-dpn-deploy.sh` helper are available on the evidence branch. The helper accepts validate/backup/install/rollback, requires explicit full source commit and expected hashes for installation, rejects source changes outside that Git snapshot, stages as root:root 750, atomically installs and validates the result, and retains a timestamped backup. Matching installations are no-op. Installation and recovery tests ran only in protected root-owned temporary fixtures. See `ops/deploy/RELEASE-RUNBOOK.md` for exact guards and commands. No runtime installation was performed.

## Runtime deployment contract preserved

The script fetches `main` from `git@github.com:DatenpflegeNordHL/datenpflege-nord-production.git` into `/var/lib/dpn-deploy/repo.git`. A supplied target must be a full 40-character commit and equal fetched `origin/main`. It does not deploy from the developer working tree. No target was deployed or merged during this task.

The 28-member closed allowlist is filtered by existence in the target commit; required HTML, robots and sitemap are separately mandatory. `git archive` packages selected files only. Validators enforce exact inventory, non-empty files, Git blob identity, local HTML/CSS references confined to that inventory, no secret-like filenames, no release symlinks and HTML/sitemap basics. An omitted optional allowlist entry is not silently treated as mandatory; the present production commit contains all 28 entries.

Activation creates `current.new` and atomically renames it over `current`. Release SHA metadata lives outside the webroot under `/var/lib/dpn-deploy/releases/`; `deployed_sha` is the final transaction marker after service and live checks. On a deployment failure after switching, cleanup attempts to restore the previous pointer and valid previous SHA, and remove a newly created inactive failed release. This is the actual preserved implementation, not a claim that a rollback was executed today.

## Independent source commit → release proof

| Artifact | Verified value |
| --- | --- |
| Git source commit | `65468e875fa0f4318cc07d7e4cbe843cacb24569` |
| Git tree | `0524b0d82110ebfed8170d3b7df39808be9fcb74` |
| Current symlink | `/srv/datenpflege-nord/current` |
| Raw and resolved target | `/srv/datenpflege-nord/releases/20260908-080736-git-65468e875fa0.DM1912` |
| Release directory | Actual directory, `root:root`, mode `755` |
| Release state | `/var/lib/dpn-deploy/releases/20260908-080736-git-65468e875fa0.DM1912.sha` contains the exact source SHA as one line |
| Global deployed state | `/var/lib/dpn-deploy/deployed_sha` contains the same exact SHA as one line |
| Selected public manifest | 28/28 expected files, no additional files, no release symlinks |
| Deployed file ownership/mode | Every selected file `root:root`, mode `664`; recorded per file |
| Independent object evidence | Local Git commit object equals server bare-cache commit object; selected blob IDs agree in both repositories |
| Deterministic content evidence | Every server-side file is byte-identical to the source Git blob; SHA-256 and blob IDs recorded per file |
| Actual runtime validators | Required files, manifest/blobs, local references, forbidden files/symlinks, HTML/sitemap basics all PASS read-only |

The release identity does **not** depend on the release directory name. The selected-file inventory and independent object comparisons prove the deployed release corresponds to the intended commit. `ops/evidence/issue15-release-20260914.json` contains the full manifest, hashes, modes and 14 Git files excluded from this source commit's public package.

Retained rollback candidate: `/srv/datenpflege-nord/releases/20260826-202520-git-49640ef4c36c.44cU28`, source `49640ef4c36cd4537228582905155d687381dde4`. Its inventory, lack of symlinks and selected file bytes also match that Git commit. This is the most recent retained preceding release by recorded timestamp, not a claim that today's runtime stores a durable previous-pointer journal. During a future deployment the runtime captures the then-current pointer/SHA before switching. No website-release rollback rehearsal or release switch occurred here. Script-update rollback is separately proven below.

## Cloudflare-aware semantic and browser parity

Server-side Git/manifest/hash proof is authoritative for package identity. CDN HTML is compared semantically, not byte-for-byte. All seven canonical pages passed origin and public comparisons of canonical, title, description, H1, schema entity types, source internal links and a source paragraph content marker. Individual values and checks are in `ops/evidence/issue15-http-20260914.json`.

Public decoded CSS (`assets/home.css`), JS (`assets/home-de.js`), profile WebP and special OG PNG hashes equal the server-side hashes; see `ops/evidence/issue15-assets-20260914.json`.

Headless Chromium desktop verified all seven canonical pages: URL/canonical, title, description, H1 after the existing typewriter animation settles, schema types, visible page body, no captured page errors and no resources with HTTP failure status. No contact interaction was performed. Initial browser-launch sandbox failure was confined to the audit process; the isolated browser was launched with `--no-sandbox` without changing host configuration, then closed. Initial transient DE/EN H1 measurements were animation timing, not deployed-content drift. This is a bounded desktop browser check, not CWV, mobile, accessibility or contact-submit acceptance. See `ops/evidence/issue15-browser-20260914.json`.

Cloudflare augments robots, can transform email markup and inject public CSP/HSTS/security headers. These observations do not invalidate server-side blob parity. No Cloudflare configuration was read through its management API or changed.

## Security-header acceptance

Every representative public endpoint below has `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: SAMEORIGIN`, enforcing CSP and HSTS `max-age=31536000`. No CSP Report-Only header was observed; this is EXPECTED with an enforcing CSP, not a missing-header P0.

Public CSP includes `default-src 'self'`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'self'`, `script-src 'self'`, `script-src-attr 'none'`, `style-src 'self'`, `style-src-attr 'none'`, `connect-src 'self' https://api.github.com` and `upgrade-insecure-requests`. Exact CSP is captured for each response. No browser page/console error was captured in this audit.

| Representative | HTTP | MIME | Public security trio / CSP / HSTS | Gzip public | Classification |
| --- | ---: | --- | --- | --- | --- |
| Homepage `/` | 200 | `text/html; charset=utf-8` | Present / enforcing / present | Yes | PASS |
| Service `/softwareentwicklung-luebeck/` | 200 | `text/html; charset=utf-8` | Present / enforcing / present | Yes | PASS |
| CSS `/assets/home.css` | 200 | `text/css` | Present / enforcing / present | Yes | PASS |
| JS `/assets/home-de.js` | 200 | `application/javascript; charset=utf-8` | Present / enforcing / present | Yes | PASS |
| Profile image | 200 | `image/webp` | Present / enforcing / present | No | EXPECTED: compressed image |
| Special OG image | 200 | `image/png` | Present / enforcing / present | No | EXPECTED: image |
| robots.txt | 200 | `text/plain; charset=utf-8` | Present / enforcing / present | Yes | PASS |
| sitemap.xml | 200 | `text/xml; charset=utf-8` | Present / enforcing / present | Yes | PASS |
| Deliberately nonexistent path | 404 | `text/html; charset=utf-8` | Present / enforcing / present | Yes | PASS: correct 404 |
| `/healthz` | 200 | `text/plain; charset=utf-8` | Present / enforcing / present | No | EXPECTED: tiny response |

Origin HTML, robots, sitemap, 404 and health have the security trio. Origin CSS/JS/images/OG lack the trio because their location-level `add_header` directives replace server-level inheritance; public responses supply it. This origin-defense gap is **IMPROVEMENT**, not a demonstrated public P0 or a reason to modify nginx here. Origin CSP/HSTS are absent; HSTS absence on a loopback plain-HTTP origin is EXPECTED. Public `Server: cloudflare`, `CF-Ray` and `CF-Cache-Status` are recorded where present. MIME and observed compression are appropriate; no security-header BLOCKER was identified in this bounded sample.

## Cache acceptance and limits

| Resource | Origin Cache-Control | Public Cache-Control / CF status | Expires / Age | Validators | Classification |
| --- | --- | --- | --- | --- | --- |
| Homepage and service HTML | Absent | Absent / DYNAMIC | Neither observed | Origin ETag + Last-Modified; public Last-Modified | IMPROVEMENT: explicit browser revalidation policy pending |
| CSS and JS | `public, max-age=604800` | Same / MISS at observation | Expires +7 days; Age absent | ETag + Last-Modified | EXPECTED for controlled assets; stable URL update policy pending |
| Profile image | `public, max-age=604800` | Same / MISS at observation | Expires +7 days; Age absent | ETag + Last-Modified | EXPECTED for controlled assets; stable URL update policy pending |
| Special OG image | `no-cache, no-store, must-revalidate` | Same / BYPASS | Expires already past; Age absent | ETag + Last-Modified | PASS: deliberate no-cache preserved |
| robots.txt | Absent | `max-age=14400` / HIT | Public Age 900 seconds; Expires absent | Origin ETag + Last-Modified; public neither | EXPECTED: observed Cloudflare-transformed four-hour cache |
| sitemap.xml | Absent | Absent / DYNAMIC | Neither observed | ETag + Last-Modified | EXPECTED: observed dynamic delivery; browser revalidation policy pending |
| 404 | Absent | Absent / DYNAMIC | Neither observed | Neither observed | EXPECTED in this sample |
| `/healthz` | Absent | Absent / DYNAMIC | Neither observed | Neither observed | EXPECTED in this sample |

Exact timestamps, headers, Age and validator strings are in the per-layer HTTP JSON. MISS is a snapshot, not a claim that assets never become HIT. Gzip responses include Vary where observed. No public HTML Age or edge HIT was observed, and current content/asset identity matches the release. This proves current parity, not a guarantee of browser freshness after a future release.

HTML lacks an explicit Cache-Control freshness/revalidation directive despite validators. DYNAMIC describes edge treatment, not browser caching. Public asset URLs in this source are stable, unversioned paths with a seven-day TTL; no automatic URL-version bump or cache invalidation exists in the runtime deploy script. Do not call them immutable or fingerprinted. Selected future policy: deterministic `?v=<full SHA-256 of final asset bytes>` for normal assets, plus explicit browser HTML revalidation retaining validators. The read-only `check_asset_versions.py` gate is implemented and tested but current live references fail it (61 references, 18 normal assets). Chromium default fetches reused both HTML and CSS locally; DYNAMIC alone does not prevent browser caching. Conditional HTML requests pass with origin/public 304s. No upper bound on browser HTML reuse across a future release is established. Live asset-version migration and bounded HTML-freshness acceptance therefore remain OPEN. No current content drift is claimed, no optional header absence is automatically treated as a P0, and no cache configuration change or website deployment was performed.

## Contact and secrets separation

Read-only inspection confirms the unchanged nginx `location = /api/contact` uses `proxy_pass http://127.0.0.1:8091;`. Direct backend health returned HTTP 200 with `{"ok": true}`. `dpn-contact`, nginx and cloudflared are active. No actual contact request was sent.

Contact environment `/etc/datenpflege-nord-contact.env`: `root:root`, mode `600`. Deploy-secret directory `/etc/dpn-deploy`: `root:root`, mode `700`. Cloudflare token file `/etc/cloudflared/token`: `root:root`, mode `600`. Only metadata was inspected. The separate backend executable/configuration and protected secrets are not public package members and are not installed by dpn-deploy. Controls and statuses are captured in `ops/evidence/issue15-controls-20260914.json`.

The nginx site SHA remains `56fb8e9b224fb6ce191e9a8911f626a48481650af64d875ea3b9873fc17444f3`. Redirect remediation remains closed; this task performs no nginx test/reload or configuration change.

## Issue #15 acceptance matrix

| Required contract item | Evidence / limitation | Status |
| --- | --- | --- |
| Canonical deployment script source | `ops/deploy/dpn-deploy`, versioned evidence-branch baseline from runtime | PASS |
| Canonical source SHA | `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01` | PASS |
| Installed script SHA | Same; `root:root`, `750`, 17000 bytes / 409 lines | PASS |
| Installation identity | Read-only verifier MATCH; mismatch/permission/unknown fixture tests | PASS |
| Canonical source/update contract | Current task selects versioned source; pinned-source helper and reviewed future installation guards documented/tested | PASS |
| Git source commit | `65468e875fa0f4318cc07d7e4cbe843cacb24569`, independent cache/local object proof | PASS |
| Release identity | Recorded release/global SHA plus content proof; not inferred from name | PASS |
| Manifest verification | 28/28 files, exact blobs/SHA-256, no extras/symlinks, runtime validators pass | PASS |
| Current symlink target | Actual link and resolved directory independently inspected | PASS |
| Website rollback target/mechanism | Retained previous release verified; runtime atomic pointer/cleanup reviewed, not executed | PASS |
| Script-update rollback proof | Actual privileged runtime backup restored only in isolated fixture; original SHA/root:root 750/syntax verified | PASS |
| Secrets separation | Complete source review + protected metadata; no secret values versioned | PASS |
| Contact backend separation | Route/backend health/service/protected env; backend outside package | PASS |
| Cloudflare transformations | Semantic HTML and server/package hashes separated; four public asset hashes match | PASS |
| Current production parity | Seven semantic/desktop-browser pages and selected static assets verified | PASS |
| Public security-header acceptance | Representative matrix PASS/EXPECTED; origin improvement documented | PASS |
| Current observed cache behavior | Deliberate OG policy, correct current content, observed resource TTLs documented | PASS |
| Normal asset freshness | Deterministic content-version policy/checker ready; actual live reference migration not applied | OPEN |
| Bounded browser HTML freshness | Default fetch cache reuse observed; 304s work, but reuse bound not proven or configured | OPEN |
| Operational check entrypoint | Fetched-main archive/resource/manifest checks passed; documented exit 10; unchanged runtime/release and cleaned temp directory | PASS |

**Issue #15 stays OPEN.** Only remaining mandatory gaps: migrate the live normal-asset references to the tested deterministic content-version policy; establish and verify bounded browser HTML freshness across releases. Update tooling, source selection, check entrypoint and script-update rollback proof are now PASS. Current runtime identity and 28/28 release parity remain PASS. Publication of this evidence does not authorize installation, deployment, nginx/Cloudflare changes or issue closure.

## Issue #10 remains separate

**Issue #10: OPEN, unchanged.** The existing evidence reports main-protection blocked by private-repository plan capability. No repository administration, visibility or protection setting was changed or revalidated here. Workflows do not replace branch protection. Do not make this repository public to obtain protection.

## Final operational proof and security/cache acceptance

Actual retained runtime backup: `/var/backups/dpn-deploy/dpn-deploy.20260914T095215.730995Z.backup`; previous SHA `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01`, root:root 750, protected root-owned metadata record. Restoration of these exact bytes was proven using the helper in an isolated privileged fixture, with shell syntax/hash/metadata validation. Live inode, mtime, bytes, metadata and release pointer remained identical. Evidence: `issue15-script-rollback-20260914.json`.

Entrypoint evidence: `issue15-entrypoint-20260914.json` records correct rejection of the old live target after fetched main advanced. `issue15-entrypoint-main-20260914.json` records successful package validation of the known new-main target with exit 10, no activation, unchanged live/global/release SHA and all 28 file hashes, no new release directory, cleaned private TMPDIR, Contact Health 200 and active services. The main advancement contains four excluded research files and does not change the current source-release identity. This task made no merge.

Complete actual asset/reference audit: `issue15-freshness-20260914.json` (19 assets, all stable URLs; OG exempt); `issue15-asset-version-gate-20260914.json` (expected current-live release gate failure, 61 references); `issue15-browser-cache-20260914.json` (same-origin browser cache/revalidation observations); `issue15-query-cache-20260914.json` (sampled distinct query keys, MISS→HIT and other key MISS; current CSS bytes unchanged). These files are under `ops/evidence/`.

| Mandatory category | Classification | Basis / acceptance |
| --- | --- | --- |
| HTML freshness | IMPROVEMENT | Current content correct and conditional origin/public 304s work; browser default cache reuse observed, mandatory cross-release freshness bound still OPEN |
| CSS freshness | BLOCKER | Stable live URLs retain seven-day freshness after same-path bytes change; content-version migration not deployed |
| JS freshness | BLOCKER | Same verified stable-URL/seven-day gap; migration not deployed |
| Normal images/media | BLOCKER | Stable image/icon URLs with seven-day caching; media uses observed four-hour edge TTL; version migration pending |
| Special OG image | PASS | Existing no-cache/no-store/must-revalidate and BYPASS preserved |
| robots freshness | EXPECTED | Accepted ordinary four-hour public crawl-policy propagation; origin validators work; not a secrets boundary |
| sitemap freshness | EXPECTED | Dynamic public delivery and origin/public conditional 304s; no explicit multi-day TTL observed |
| 404 | PASS | Correct 404, public security headers and dynamic delivery |
| Health endpoint | PASS | Correct 200/text MIME, active services and Contact Health 200; no contact submission |
| CSP | PASS | Existing sampled enforcing public policy; no captured page/console errors in seven-page parity check |
| HSTS | PASS | Existing public max-age=31536000; absence on loopback HTTP expected |
| X-Content-Type-Options | PASS | Public nosniff; separate origin asset inheritance improvement remains non-blocking |
| Referrer-Policy | PASS | Public strict-origin-when-cross-origin |
| X-Frame-Options | PASS | Public SAMEORIGIN |
| Compression | PASS | Prior sampled HTML/CSS/JS/robots/sitemap gzip appropriate; images/tiny health without gzip expected |
| MIME | PASS | Correct representative HTML/CSS/JS/image/text/XML/error/health types |

Security/compression/MIME sampling from the existing seven-page parity/representative header evidence is carried forward; no unrelated forensic audit was repeated. New cache probes and before/after nginx/runtime/manifest checks corroborate unchanged relevant state. Classification BLOCKER is reserved here for the actual stable-URL caching release-safety failure, not optional header absence. HTML acceptance remains incomplete without falsely claiming a present multi-day content error.

## Validation and change boundary

42 distinct unit tests pass across the ordinary suite (31 executed, 11 privileged installer tests explicitly skipped) and the separate root-only fixture suite (11/11 pass). Three shell entrypoints pass `bash -n`; static site and Golden audits pass. The hosted workflow now runs those syntax checks and explicitly runs root-only installer fixtures on the hosted runner; it does not alter Issue #10 protection and is not evidence of a hosted run already completed. Secret screening, documentation/JSON checks and final diff review precede commit/push. The current-live content-version gate intentionally returns exit 1/BLOCKER and is recorded as an unresolved release gate, not a failed unit test silently ignored.

Only evidence/docs/ops tooling/tests and the hosted test workflow changed in Git. Bounded production state changes were check-mode lock/fetch/cache activity and a retained script backup. No installed runtime replacement, public release mutation, nginx change/reload or contact request occurred. Full procedure and selected freshness policy: `ops/deploy/RELEASE-RUNBOOK.md`.

No website deployment performed

No nginx configuration changed

No Cloudflare configuration changed

No contact backend configuration changed

No merge to main performed


## 2026-09-15 compensating-control candidate

GitHub-native branch protection is unavailable under the chosen private/free
organization plan. It is not enabled and the repository must not be made public.
The reviewed alternative is the cryptographically signed production-release
boundary in `ops/deploy/P0-RELEASE-AUTHORIZATION.md`: exact main SHA, exact Hosted
CI success, explicit human signed annotated tag, fixed server trust root,
immutable tag identity, package/manifest validation, and explicit deployment.
There is no deployment-on-push workflow. Issue #10 may be reclassified to
**ACCEPTED RISK / COMPENSATED** only after Hosted CI and server installation/
non-deploying acceptance complete; source-only implementation is insufficient.
