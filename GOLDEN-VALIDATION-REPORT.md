# Golden Website Build 2.0 — Phase 1–3 validation report

Validation date: 2026-09-13. This is the canonical completion report for the local `golden-website-build-2-phase-1-3` branch. Repository evidence, read-only live-production observations and local browser measurements are separate evidence classes throughout this report.

## A. Scope

Phase 1–3 was limited to planning/audit documentation, deterministic audit/test tooling, shared service-page CSS, sitemap `lastmod` maintenance and content/schema/internal-link expansion of exactly these existing canonical owners:

- `https://datenpflege-nord.de/softwareentwicklung-luebeck/`
- `https://datenpflege-nord.de/webentwicklung-luebeck/`
- `https://datenpflege-nord.de/ki-automatisierung-luebeck/`

No new indexable URL, Kiel/Hamburg page, standalone API page, city-specific n8n page, unsupported service family, review/rating, location or sameAs entity is part of this implementation. Push, merge, deployment and production configuration changes are outside this task.

## B. Evidence provenance

Repository: `DatenpflegeNordHL/datenpflege-nord-production`.

- Golden foundation / PR #9 source actually used: `02987d9b710c9bcade535d4f37183dd6bebbac26` (`seo: validate exact P0 keyword queue`). The newest Golden validation/evidence documents were read from this foundation state.
- Research source: `main` / `origin/main` at `e72e01be18a3c8ad1ed43660ef8cb88f0a981bfa` (`docs: add DatenpflegeNord keyword research`).
- Earlier PR #11 concept inspected separately: `78c725111e930e29173c9e13a5dec3ea7d4ad528`; it was not treated as the newest keyword authority.
- The four `research/datenpflege-nord/` files were copied unchanged from `main`. Local files and `git show e72e01b:<path>` were SHA-256 compared and are byte-identical:
  - `KEYWORD-UNIVERSE-RAW.csv`: `41d50b497fdf236f41c251aebfd5a9f39ae27629e5a31653666216245df024ae`
  - `KEYWORD-CLUSTERS.md`: `57f21c67bc682b19183b00ab6769aaf84c976265098841deddc1f67d2bf8829a`
  - `KEYWORD-VALIDATION-QUEUE.md`: `34b2e3a7e2d2fe3c702555c9bff5cab2bc035fa3f64316ed234915f7cade95d1`
  - `NICHE-OPPORTUNITIES.md`: `ce37baef20af84ebdec4327aa14e355aa52c3cdbf830d93fc7ae1423b3e4800a`

Evidence classes:

1. **Repository evidence**: files, Git history, deterministic static audits and local source inspection.
2. **Local browser evidence**: loopback HTTP rendering and interaction tests against this branch; this is not production performance or production HTTP evidence.
3. **Live-production observations**: read-only HTTP checks against `https://datenpflege-nord.de/`; these describe the currently served site/edge behavior, not deployment of this branch.

## C. Changed implementation files

### Production-facing HTML / CSS / sitemap

- `softwareentwicklung-luebeck/index.html`
- `webentwicklung-luebeck/index.html`
- `ki-automatisierung-luebeck/index.html`
- `assets/service.css`
- `sitemap.xml`

### CI / audit tooling

- `.github/workflows/site-audit.yml`
- `scripts/golden_audit.py`
- `scripts/README.md`

### Tests

- `tests/test_golden_audit.py`

### Documentation / evidence

- `GOLDEN-IMPLEMENTATION-PLAN.md`
- `GOLDEN-CONTENT-OWNERSHIP-MAP.md`
- `GOLDEN-AUTHORITY-CONTENT-MAP.md`
- `INTERNAL-LINK-GRAPH.md`
- `API-SCHNITTSTELLEN-BRIEF.md`
- `KIEL-WEB-UNIQUE-VALUE-BRIEF.md`
- `AUTHORITY-ACTIVATION-PLAN.md`
- `GSC-VALIDATION-PLAN.md`
- `BING-INDEXNOW-PLAN.md`
- `AI-GEO-EVIDENCE-MAP.md`
- `GOLDEN-TECHNICAL-AUDIT.md`
- `GOLDEN-VALIDATION-REPORT.md`
- `research/datenpflege-nord/KEYWORD-UNIVERSE-RAW.csv`
- `research/datenpflege-nord/KEYWORD-CLUSTERS.md`
- `research/datenpflege-nord/KEYWORD-VALIDATION-QUEUE.md`
- `research/datenpflege-nord/NICHE-OPPORTUNITIES.md`

## D. Content decisions

| Cluster / asset | Decision | Final Phase 1–3 state |
|---|---|---|
| Softwareentwicklung Lübeck | OWN / EXPAND | Existing software owner expanded |
| Individualsoftware entwickeln lassen | EXPAND | Buyer-decision content implemented in Software owner |
| API-/Schnittstellenentwicklung | EXPAND | Implemented as `#schnittstellen` within Software owner |
| Standalone `/api-schnittstellenentwicklung/` | HOLD | No route created; overlap/unique-proof gate remains open |
| Webdesign / Webentwicklung Lübeck | OWN / EXPAND | Existing Web owner expanded for overlapping buyer intent |
| Standalone `/webdesign-luebeck/` | HOLD | No lexical duplicate route created |
| KI / n8n / controlled automation | OWN / EXPAND | Existing AI owner expanded with rule/AI/approval and project-start decisions |
| Authority/decision sections approved for Phase 1–3 | BUILD | Implemented only inside the three existing owners |
| Standalone Phase-4 authority assets | HOLD | Not built in this task |
| Kiel Web | HOLD | Unique-value brief has not passed; no route created |
| Hamburg service opportunities | HOLD | Explicit service-area truth missing; no route created |
| City-specific n8n pages | BLOCK | No city clone pages permitted |
| Unsupported SEO/GEO/marketing/managed-IT/IT-support/hosting sales pages | BLOCK | Outside verified Business Truth |
| Broad `Systemintegration` as acquisition owner | REJECT | Too broad / scope-confusing; only contextual wording allowed |

## E. SEO / GEO implementation

Actually implemented:

- Software owner: Individualsoftware procurement language, standard-vs-extension-vs-custom decision table, modernization/project-start inputs, nonnumeric cost drivers, ownership/maintenance questions and API/Schnittstellen planning/failure boundaries.
- Web owner: Webdesign/Webentwicklung buyer language, website-vs-landingpage-vs-relaunch decisions, project-start inputs, integrations, nonnumeric cost drivers and technical acceptance criteria.
- AI owner: deterministic workflow vs KI vs agent decision criteria, human approval boundaries, n8n/API context, process inputs, failure cases and project-start criteria.
- Descriptive contextual links between owners and existing contact CTA.
- Meaningful sitemap dates updated only for the three materially changed service URLs.

Still planning/HOLD only: dedicated API page, dedicated Webdesign page, all Kiel/Hamburg pages, standalone comparison/cost/use-case articles, Google Business activation, authority outreach, GSC/Bing connection, IndexNow implementation and Phase 4 assets.

## F. Schema / entity changes

On each of the three service owners, `WebPage` now references the existing `WebSite` via `isPartOf` and the existing `BreadcrumbList` via `breadcrumb`; edited `WebPage` name/description stays aligned with visible metadata. The Web service `name`/`serviceType` changes to `Webdesign und Webentwicklung`, matching visible service wording.

Unchanged by design: Organization legal identity and `@id`, canonical domain, provider relation, Lübeck/Schleswig-Holstein `areaServed`, legal pages, sameAs, physical location data and ratings/reviews. No `LocalBusiness`, `FAQPage`, `Review` or `AggregateRating` schema was added.

Issue #13 remains the gate for future legal/entity expansion; this branch does not reinterpret or alter legal identity.

## G. Internal linking

Deterministic graph validation traverses actual same-origin HTML links from the homepage. All seven canonical pages are reachable; sitemap membership alone is not accepted as reachability.

- `/` links directly to the three service owners.
- Software links contextually to AI decision content and to the other service owners.
- Web links to Software `#entscheidung` and `#schnittstellen` where business logic/integrations cross the service boundary.
- AI links to Software `#schnittstellen` for system/API access.
- All three service owners link to `/#kontakt` and retain related-service navigation.
- `/en/` does **not** directly link to the three service pages. Its actual discovery path is `/en/` → `/` → service owner.

No Phase-4 content or regional/API HOLD candidate exists as an orphan because none was created.

## H. Accessibility / mobile browser evidence

Local loopback browser tests against the production-facing Phase 1–3 tree covered the three service pages at 1440 px, 390 px and 320 px:

- no horizontal page overflow at any tested viewport;
- decision-nav anchors reach their target sections;
- contact CTA resolves to `/#kontakt`;
- the three service-page viewport runs produced no browser console errors or resource-load failures;
- Software comparison table fits normally on desktop and uses contained horizontal scrolling on narrow viewports;
- at 320 px the comparison wrapper is focusable and `ArrowRight` changes its horizontal scroll position, demonstrating keyboard access to overflowed columns;
- no-JS load retains decision, Schnittstellen and project-start content in initial HTML;
- Reduced Motion media emulation matches; computed `scroll-behavior` becomes `auto` and transition/animation durations collapse to approximately `0.01ms`;
- mocked contact-form behavior, without a real network submission: an empty submit is blocked before any POST; mocked failure reports the existing retry/email fallback message; mocked success reports `Nachricht gesendet. Vielen Dank.` and resets fields; fallback action remains `mailto:kontakt@datenpflege-nord.de`.
- the deliberate mocked HTTP 500 in the contact error-path test produces the browser's expected failed-resource console entry. A normal-motion headless homepage run also reported `net::ERR_ABORTED` for the unchanged hero MP4 request; the same local asset independently returns HTTP 200 with the expected `video/mp4` response, while Reduced Motion correctly avoids requesting the video. This is recorded as a local headless-media observation, not as production delivery evidence.

These results are local browser evidence only. They are not production CWV, field INP, CDN or backend acceptance evidence.

## I. Test matrix

Final static commands are rerun from the completed working tree before the local commit. The final result column is updated only from that run.

| Check | Command / method | Final result |
|---|---|---|
| All unit tests incl. Golden tests | `python3 -m unittest discover -s tests` | PASS; 14 tests |
| Existing static site audit | `python3 scripts/site_audit.py` | PASS; 7 HTML pages |
| Golden audit | `python3 scripts/golden_audit.py` | PASS; 7 reachable canonical pages, structure/indexability and three service graphs |
| JavaScript syntax | `node --check assets/home-de.js`, `home-en.js`, `service.js` | PASS |
| Python compile | `python3 -m py_compile scripts/site_audit.py scripts/golden_audit.py` | PASS |
| Whitespace/diff integrity | `git diff --check` | PASS |
| Exact route freeze | filesystem discovery + Golden canonical-scope gate | 7 canonical HTML routes only; no added route |
| Sitemap change scope | direct XML inspection | 7 URLs; only S/W/A use `2026-09-13` lastmod |
| Research parity | SHA-256 local vs `git show e72e01b:<file>` | PASS; all four byte-identical |
| Secret/credential pattern scan | changed/untracked Phase 1–3 file set | PASS; no credential-like assignment/private-key material found |
| External HTML links | explicit read-only HEAD checks | PASS; Cloudflare privacy/DPA, GitHub privacy/API and five linked GitHub PRs plus DeoMail privacy returned 200 |
| Browser 1440/390/320 | local loopback + headless browser/CDP | PASS; details in H |
| Table keyboard overflow | local browser at 320 px | PASS; focus + ArrowRight moved `scrollLeft` |
| No-JS decision content | browser with JS disabled | PASS |
| Mock contact empty/error/success | local mocked `/api/contact`; no real request | PASS |
| Reduced Motion | browser media emulation | PASS |
| Local hero video HTTP delivery | direct loopback GET of `/assets/hero/mainframe-hero.mp4` | PASS; HTTP 200, `video/mp4`, 4,588,424 bytes |

Hosted GitHub Actions CI is **not** claimed as passed. This task forbids push; therefore the new local commit cannot have hosted CI evidence yet.

## J. Live-production observations

These are read-only observations of the currently served production site, rechecked 2026-09-13 at `2026-09-13T18:59:30Z`; they do not prove this branch is deployed.

- Canonical trailing-slash homepage/service/English/legal URLs sampled: HTTP 200.
- `robots.txt`: 200. `sitemap.xml`: 200.
- Missing test route `/golden-audit-nonexistent-20260913/`: HTTP 404.
- External HTML links listed in section I: explicit HEAD checks returned HTTP 200.
- Sample delivery: HTML/JS zstd and CSS gzip observed with compressed requests.
- Security headers observed: enforcing CSP, HSTS `max-age=31536000`, `X-Content-Type-Options: nosniff`, Referrer-Policy and Permissions-Policy.
- Sample static assets: `Cache-Control: public, max-age=604800`; live robots sample `max-age=14400`; no explicit HTML cache-control was observed in the sampled baseline.
- Cloudflare was in the observed response path (`Server: cloudflare`). Live output is transformed: observed examples include robots.txt augmentation, email-address obfuscation and an injected decoder script / modified homepage bytes.

Consequently, simple full-file SHA-256 equality between repository/origin HTML and Cloudflare-served HTML is **not** sufficient production-parity proof. Future Production Truth must layer: (1) release artifact/origin-file manifest, (2) server-side deployed-file verification, (3) HTTP semantic verification of important fields, (4) expected/documented CDN transformations and (5) browser-visible functional verification.

### P0 production redirect / canonicalization defect

All six tested no-trailing-slash production subpages return HTTP 301 with `Server: cloudflare` and a `Location` pointing to `http://datenpflege-nord.de:8080/.../`:

| Requested URL | Status | Returned `Location` | Follow result |
|---|---:|---|---|
| `https://datenpflege-nord.de/softwareentwicklung-luebeck` | 301 | `http://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | Followed case fails with curl/OpenSSL `wrong version number`; effective URL reported `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/`, one redirect |
| `https://datenpflege-nord.de/webentwicklung-luebeck` | 301 | `http://datenpflege-nord.de:8080/webentwicklung-luebeck/` | Location recorded; not fully followed |
| `https://datenpflege-nord.de/ki-automatisierung-luebeck` | 301 | `http://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | Location recorded; not fully followed |
| `https://datenpflege-nord.de/en` | 301 | `http://datenpflege-nord.de:8080/en/` | Location recorded; not fully followed |
| `https://datenpflege-nord.de/impressum` | 301 | `http://datenpflege-nord.de:8080/impressum/` | Location recorded; not fully followed |
| `https://datenpflege-nord.de/datenschutz` | 301 | `http://datenpflege-nord.de:8080/datenschutz/` | Location recorded; not fully followed |

Classification: **P0 PRODUCTION REDIRECT / CANONICALIZATION DEFECT**. Confidence is high for the reproduced HTTP behavior. Exact server cause remains unknown because configuration evidence was not inspected in this branch. Potential impact includes canonical discovery, crawler behavior, link equity, user navigation, protocol consistency, exposed internal/upstream port and crawl efficiency. Remediation belongs to Issue #15 plus reviewed production/nginx deployment-contract verification and is intentionally not performed here.

## K. Open release blockers

### P0

- Issue #10: main protection / required Static site audit remains unresolved; GitHub API evidence reported `main protected: false`.
- Issue #15: production deployment contract / reviewed route-nginx-backend/rollback/parity contract remains unresolved.
- Production no-slash `:8080` redirect/canonicalization defect described above.

### P1 / external dependencies

- Issue #13 legal/entity alignment.
- GSC first-party query/index/canonical/CTR/CWV evidence.
- Google Business/local-entity ownership, duplicate and factual-tuple verification.
- Authority/referring-domain activation based on real relationships and artifacts.
- Production CWV/field evidence.
- Server-side release/parity evidence that accounts for expected Cloudflare transformations.
- Live contact-path acceptance under the reviewed deployment/backend contract.
- Homepage/template-proof cleanup, including existing logo/provenance and social-card concerns.
- Business-Truth decision for the existing Website-Checks positioning before treating it as a verified offer.

## L. Release decision

**PHASE 1–3 LOCAL IMPLEMENTATION: PASS**.

**PRODUCTION RELEASE: BLOCKED**.

These are separate decisions. A locally valid content branch does not satisfy the unresolved production, entity and measurement gates.

## M. Next safe actions

1. Review the resulting local Phase 1–3 commit and exact diff without pushing it.
2. Resolve Issue #10 main protection / required-check configuration outside this branch.
3. Resolve Issue #15 deployment contract and the production no-slash `:8080` redirect defect with reviewed production configuration evidence.
4. Resolve Issue #13 legal/entity alignment before external entity/profile expansion.
5. Prepare an approved preview/release package and hosted CI run only after a later authorized push.
6. Obtain GSC/Bing/local-entity baselines and production parity/CWV/contact evidence before any indexation or release activation.


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
