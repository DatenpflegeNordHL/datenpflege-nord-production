# P0 freshness release candidate — local evidence

Branch: `golden-p0-freshness`, based on validated Golden implementation/evidence
lineage `6381684` (`golden-p0-infra-evidence`). Main and the separate Anne demo
worktree remain untouched. This is candidate evidence, not production acceptance.

## Asset policy and coverage

79 versioned references to 19 distinct public assets: 61 HTML resource
references plus 18 social/structured-data references. Every public static asset
in the current allowlist is covered. Existing CSS uses only a data URI; existing
JS uses external GitHub resources and `/api/contact`, with no additional literal
local static dependency. These are audited, not falsely counted as versioned.

Full SHA-256 is computed from final asset bytes. A sorted dependency DFS visits
leaves first, rejects missing/unpackaged references and cycles before writes,
then rewrites parents. Nested image → module/CSS → HTML and JSON/module chains
are covered by fixtures. Full query hashes are required even for hashed names.

Generator: `ops/deploy/check_asset_versions.py --root . --generate`.
Checker: the same CLI without `--generate`; output identifies source, asset,
expected SHA-256 and observed version. Offline and read-only in checker mode.

Repeat generation returns `changed_files: []`; a full working-tree byte snapshot
before/after remains identical. Unit fixtures also prove unchanged mtimes.
Navigation, canonical, hreflang, sitemap page URLs, API, external and fragments
remain unversioned. Favicon/apple-touch-icon/OG/schema image bytes are versioned;
OG response policy remains deliberately `no-cache, no-store, must-revalidate`.
Sitemap bytes and meaningful-content lastmod are unchanged.

## HTML and browser gates

Minimal candidate diff: `ops/nginx/datenpflege-nord-html-freshness.patch`.
Server-level `Cache-Control` map yields `no-cache` for HTML including resolved
`.html` 304 responses (nginx clears MIME on 304), preserving server security
header inheritance. Other response policies and routes are unchanged.

`tests/test_nginx_freshness.py` passes two isolated nginx syntax tests and checks
all seven real pages, HTML 200/304, ETag, Last-Modified, security headers, static
CSS/JS/image/video caching, OG, robots, sitemap, health and stubbed contact.
No live contact/backend requests, nginx reload, production config or service
management occurs. The media vhost is not included or modified.

Real Chromium via agent-browser 0.27.0 proves normal navigation reaches HTML
revalidation/304. After meaningful fixture HTML and image bytes change, normal
navigation receives new HTML; new image/CSS hash URLs receive 200/new bytes.
An unchanged asset retains its URL. Fetching the old image URL still returns
browser-cached OLD bytes. Browser cache is never cleared during the experiment.
Future public-edge repeat instructions: `ops/nginx/FRESHNESS-CANDIDATE.md`.

## Local validation

| Gate | Result |
| --- | --- |
| unittest discovery, including actual browser | 56 discovered: 45 PASS, 11 privileged fixtures SKIPPED |
| asset tests (missing/wrong/malformed/duplicate version, missing asset, cycles, dependency order, idempotence, exclusions, metadata) | PASS |
| exact Git archive/package unit fixtures (3) | PASS |
| nginx baseline/candidate `nginx -t` and HTTP/browser checks | PASS |
| Python compileall | PASS using isolated `/tmp` bytecode cache |
| shell syntax: dpn-deploy, install helper, identity verifier | PASS |
| JS syntax: home-de, home-en, service | PASS |
| Static Site Audit | PASS: 7 pages |
| Golden Audit | PASS: 7 reachable canonical pages, service graphs |
| offline credential-signature secret scan, including pending files | PASS; no matches; not an arbitrary-secret guarantee |
| generator/checker | PASS: 79 references |
| repeat generation + full working-tree byte snapshot | PASS: zero changes |
| workflow YAML parse | PASS |
| git diff --check | PASS |
| production vhost vs baseline byte comparison | IDENTICAL |

The existing root-owned bytecode directory is left untouched. Isolated Python
cache output permits compile validation without filesystem permission changes.
Eleven existing root-only installation/rollback tests cannot run locally because
passwordless sudo is unavailable. Hosted CI explicitly runs those via sudo.

## Package integration and remaining gates

Finalized source → dependency/version generation → final bytes → Golden checks
→ exact committed Git archive/public package → canonical version/manifest gates
→ SHA-256 manifest. `verify_release_candidate.py` rejects archives requiring
regeneration; no post-manifest mutation is performed. The version-controlled
runtime validator loads its checker from the pinned target Git object, and
checks versions before manifest parity. The installed production executable is
not changed; future installation requires separately reviewed authorization.

Hosted CI is configured for this branch and PRs to main, checks out exact head
SHA and must run subsequently on the final candidate commit. It has NOT run in
this task; root-fixture and edge-release evidence remain open. Local exact-commit
verifier output is retained separately in `/tmp/dpn-release-candidate.json` after
candidate commit creation; no evidence file embeds its own circular commit SHA.

Issue #15's production acceptance remains open until an approved future release
proves asset URLs and HTML freshness at the public edge. No deployment is
recommended. Issue #10 remains a release gate: actual main protection must be
enforced, independently of any successful CI or freshness candidate.

No production deployment performed.
No merge to main performed.
No production nginx configuration changed.
Issue #10 remains a release gate.
