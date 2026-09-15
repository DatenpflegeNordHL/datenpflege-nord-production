# Golden Website Build 2.0 — implementation contract

Recorded 2026-09-13 **before public HTML changes** and reconciled with the final local Phase 1–3 working tree during validation. Scope: safe Phase 1–3 only.
Branch: `golden-website-build-2-phase-1-3`. No push, merge, deployment, profile activation or indexing submission is authorized by this package.

## Repository and evidence truth

Foundation: PR #9 at `02987d9b710c9bcade535d4f37183dd6bebbac26`.
Research: four `research/datenpflege-nord/` files copied byte-for-byte from main at `e72e01be18a3c8ad1ed43660ef8cb88f0a981bfa`; those files are absent from the foundation tree despite the validation document referencing them. They must be included when reviewing this stacked branch. No merge into main was performed.

Read the seven canonical documents completely; read the four research files, including all 570 CSV rows (570 unique keywords), 150 queue entries and 56 cluster records. Read homepage and all three service pages. Inspect PR #11 as an earlier concept, not as current keyword authority. Latest exact-P0 validation takes precedence over the raw research's `METRIC_PENDING` flags, speculative regional reach and automatic opportunity ordering. Metrics are historical provider estimates, not newly measured traffic.

No repository OpenSpec or Beads state exists. This contract and the existing canonical evidence own acceptance criteria; no parallel specification/task framework is introduced. Small static HTML site: use its dependency-free audit and targeted local inspection.

## 1. Current Golden compliance audit

| Stage | Current finding | Gate |
|---|---|---|
| Business Truth | Four service families verified; Lübeck/SH context; current legal identity retained | PASS for existing scopes; #13 open for entity expansion |
| Search / intent evidence | 2026-09-13 validation: 60 P0 checked, 13 metric rows, 47 no reliable exact rows | PARTIAL; no-data is not zero |
| Keyword cluster | Web buyer synonyms overlap; Individualsoftware buyer phrase distinct from definitions | PASS for expansion |
| SERP reality | Web commercial; local software job-mixed; Schnittstellen commercial; API Integration informational | PASS for existing sections; standalone overlap incomplete |
| URL ownership / cannibalization | Three owners, no new indexable routes | PASS for expansion; new owners HOLD |
| Unique value | Decision table, requirements checklist, integration failure cases, bounded automation decisions | PASS as scoped below; no fictional proof |
| Content / entity / authority design | Companion maps define boundaries and later evidence work | PASS for planning only |
| Implementation | Three existing Lübeck service owners, scoped CSS/sitemap changes, Golden audit tooling and planning documents are complete locally | Phase 1–3 only; no new indexable route |
| Static CI | Baseline checks passed before edits; final-tree results belong in `GOLDEN-VALIDATION-REPORT.md` | Local validation only; hosted GitHub CI cannot be claimed before push |
| Preview | Final local browser evidence belongs in `GOLDEN-VALIDATION-REPORT.md` | Local browser proof is distinct from production measurement |
| Merge / approved package | #10 signed-release compensating control and #15 activation contract must be installed/accepted | BLOCK |
| Production / live verification | Read-only baseline exists; broken slash redirect discovered | BLOCK release; baseline is not new-release proof |
| Indexation / monitoring / iteration | GSC access not established, Bing status unverified | P0 external measurement dependency; future stages pending |

The Golden sequence is not shortened: unperformed downstream stages remain pending/blocked rather than being represented as passed.

## 2. Missing gates

- #10: GitHub API rechecked 2026-09-13: main `protected: false`.
- #15: reviewed transport/activation script, nginx mapping, rollback, permissions, artifact/live parity absent. PR #16 is a separate unmerged package implementation, not available on this branch.
- New live failure: all six tested no-slash production subpages redirect with HTTP 301 to `http://datenpflege-nord.de:8080/.../`. The fully followed software-development case then fails during TLS handling on port 8080. This is a P0 production redirect/canonicalization defect; remediation belongs to Issue #15/server-contract work and is outside this branch.
- #13: current registered legal name/purpose reconciliation; no new legal facts or external profiles.
- GSC query/canonical/index/CTR/CWV data and verified Bing property.
- Kiel unique regional usefulness/logistics proof; Hamburg explicit service-area truth; independent API owner SERP overlap and original proof depth.
- Existing homepage template logos, stale GitHub fallback and social Website-Checks mismatch remain release concerns; PR #12 concepts are not released truth.
- Fresh production mobile/field CWV, real backend parity and separately authorized mail delivery test.

## 3. URL ownership

See [GOLDEN-CONTENT-OWNERSHIP-MAP.md](GOLDEN-CONTENT-OWNERSHIP-MAP.md).
Software owns procurement, internal applications and API implementation; Web owns websites/design/relaunch; AI owns controlled automation, n8n and KI integration. API decision A applies now: expand software; dedicated API route HOLD.

## 4. Existing files modified in Phase 1–3

- `softwareentwicklung-luebeck/index.html`: Individualsoftware buyer decision, alternatives, requirements, costs/ownership questions and API depth; metadata aligned.
- `webentwicklung-luebeck/index.html`: Webdesign buyer language, project alternatives, requirements/risks/cost drivers; metadata and Service label aligned.
- `ki-automatisierung-luebeck/index.html`: deterministic workflow vs AI, approvals, input checklist, integration boundaries; metadata aligned.
- `assets/service.css`: responsive accessible decision table only; versioned stylesheet query on the three pages to avoid the observed seven-day cached old CSS.
- `sitemap.xml`: change only the three service `lastmod` values to the meaningful content-edit date `2026-09-13`; no deployment stamping.
- `.github/workflows/site-audit.yml`: run the supplementary Golden graph/schema/indexability audit after existing checks.
- `scripts/README.md`: document additional deterministic checks and their limits.

## 5. New files in this Phase 1–3 branch

- `GOLDEN-IMPLEMENTATION-PLAN.md` (this contract)
- `GOLDEN-CONTENT-OWNERSHIP-MAP.md`
- `GOLDEN-AUTHORITY-CONTENT-MAP.md`
- `INTERNAL-LINK-GRAPH.md`
- `GSC-VALIDATION-PLAN.md`
- `AUTHORITY-ACTIVATION-PLAN.md`
- `BING-INDEXNOW-PLAN.md`
- `AI-GEO-EVIDENCE-MAP.md`
- `KIEL-WEB-UNIQUE-VALUE-BRIEF.md` (gate assessment, not a page)
- `API-SCHNITTSTELLEN-BRIEF.md` (future conditional brief; HOLD)
- `GOLDEN-TECHNICAL-AUDIT.md`
- `GOLDEN-VALIDATION-REPORT.md`
- `scripts/golden_audit.py`
- `tests/test_golden_audit.py`

Research files added relative to PR #9, already present unchanged on main: `research/datenpflege-nord/KEYWORD-UNIVERSE-RAW.csv`, `KEYWORD-CLUSTERS.md`, `KEYWORD-VALIDATION-QUEUE.md`, `NICHE-OPPORTUNITIES.md`.
Inherited PR #9 evidence/workflow/license changes remain visible in a main comparison; distinguish them from this task's changes.

## 6–7. Content and internal-link architecture

Homepage → three existing service owners. Each service links to the other two and `/#kontakt`. Software anchors: `#entscheidung`, `#schnittstellen`, `#projektstart`. Web: `#entscheidung`, `#projektstart`. AI: `#entscheidung`, `#projektstart`. Contextual Web/AI links point to software's interface/decision sections. Commercial Webanwendungen with business logic belong to Software; a website/frontend remains Web. Supporting assets are scoped in the authority map; none becomes a separate Phase-4 URL now. Internal graph must prove all seven canonical pages reachable from home.

## 8. Schema changes

Retain Organization legal identity, IDs, provider and Lübeck/SH service area. Match WebPage title/description to edited metadata. Add `isPartOf` reference to the existing WebSite and `breadcrumb` reference to the existing BreadcrumbList on each service. Web Service name/type may read `Webdesign und Webentwicklung`, supported by visible design/frontend work. No ratings, reviews, prices, new locations, FAQPage, artificial AI schema, or sameAs expansion. LocalBusiness remains HOLD pending #13 and verified real location/profile suitability. Organization is a valid conservative representation; being locally discoverable alone does not require a type migration.

## 9–11. Authority, GSC and Bing plans

See the activation, GSC and Bing/IndexNow companion plans. They specify ownership checks, evidence, acceptance and monitoring; no external writes are included. GSC is P0 measurement input and overrides estimated volume when actual query evidence becomes available. IndexNow design submits only a reviewed release delta after production verification.

## 12. Release verification plan

Repository Truth → CI Truth → Preview Truth → Approved Release Package → Production Truth.

1. Run all repository unit tests, site audit, Golden audit and three JS syntax checks; inspect diff/whitespace and research parity.
2. Local loopback preview: all three pages at mobile/desktop widths, table overflow, heading/CTA visibility, keyboard links, console/network, reduced motion and no-JS content. Local preview is not a server-equivalent release preview.
3. Before merge: resolve #10 and #15; reconcile PR #9/#11/#12/#14/#16 dependencies; ensure internal docs/tests never enter webroot. Obtain exact-head hosted CI and a reviewed artifact preview. User release approval is outside this task.
4. Before activation: record reviewed SHA, artifact/manifest digest, script digest, rollback target, ownership, nginx route and backend separation. Fix the exposed-port redirect through a reviewed server change. Preserve external secrets.
5. After a later authorized deployment: GET all seven routes, redirects, robots, sitemap, titles, descriptions, canonicals, schema and body; compare hashes/assets with artifact; verify headers/cache invalidation/mobile/form behavior and release identity. No real message without explicit delivery authorization.
6. Capture LCP/CLS and interaction lab evidence; field INP/CWV from GSC/CrUX if available. Missing field samples stay unknown.
7. Only then submit sitemap/released changed URLs, inspect indexation/canonicals and start 7/28/90-day query, CTR, lead and authority review. No rankings or completed Golden release claimed before evidence.

## Acceptance criteria

No new canonical routes, no altered legal tuple, no invented service/location/customer/price/SLA claims. Three page-specific decision sections offer concrete alternatives, limitations, input requirements and next action. Every new internal fragment resolves. Metadata/schema remain coherent. New tests exercise real negative cases, not keyword counts. Reports distinguish baseline, local checks, hosted CI, preview and production truth.
