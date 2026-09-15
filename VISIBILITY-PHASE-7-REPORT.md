# Visibility Phase 7 — Final Evidence

Status date: 2026-09-15

## Exact source state

- Phase-6 final branch: `golden-visibility-phase-6-intelligence`
- Phase-6 final SHA: `57a45f91af6e8e02d361d704813a62b7013f3560`
- Phase-7 branch: `golden-visibility-phase-7-authority`
- Phase-7 base SHA: `57a45f91af6e8e02d361d704813a62b7013f3560`
- Phase-7 implementation commit: `6c3a21398a1cfc223beed8049494a34491141417`
- Phase-7 implementation remote SHA: `6c3a21398a1cfc223beed8049494a34491141417`
- Phase-7 release-gate follow-up / validated source SHA: `abf013131551e82738762b36ec47efb0b82a5f99`
- Phase-7 validated remote SHA: `abf013131551e82738762b36ec47efb0b82a5f99`

This report is a later evidence-only commit. The validated source SHA above contains the implementation, release-allowlist correction and final responsive authority styling used for the successful hosted validation run. The report commit itself is documentation-only, so its own hash is intentionally not embedded recursively.

## Indexable URL changes

### New authority owner

`/wissen/ki-prozessautomatisierung/`

- National informational / commercial-decision intent, not a second Lübeck service page.
- Answer-first coverage of deterministic automation, bounded AI steps, Human-in-the-Loop, validation, APIs/workflows/n8n/LLMs, logging, fallback paths and maintenance.
- Client-side Automation Decision Matrix with eight process/risk inputs and four bounded recommendation classes.
- No server submission, tracking, financial output, fabricated ROI, customer example or performance promise.
- Core content remains readable without JavaScript.
- Truthful `Organization`, `WebPage`, `TechArticle` and `BreadcrumbList` graph; no FAQPage, Review, AggregateRating or LocalBusiness expansion.

### Expanded authority owner

`/wissen/website-relaunch-checkliste/`

- Added nonnumeric Relaunch cost drivers rather than a separate cost article.
- Added the required eight-stage project model from baseline through post-launch verification, including objective, key checks, typical responsibility and failure risk.
- Added explicit SEO/technical migration coverage for URLs, redirects, canonicals/indexability, internal links, content/search task, release parity and post-launch checks.
- Existing 36-point interactive checklist remains the single working tool and was not duplicated.

### Existing commercial owner bridge

`/ki-automatisierung-luebeck/`

- Added one contextual link to the KI process authority guide.
- Local commercial intent, n8n implementation and Lübeck ownership remain on the existing service page.

No substantive Phase-7 rewrite was necessary for `/softwareentwicklung-luebeck/`, `/webentwicklung-luebeck/` or `/wissen/individualsoftware-kosten/`: the validated Phase-6 gaps were already covered. The Individualsoftware authority HTML changed only because the shared `authority.js` content hash changed.

## Final keyword ownership

| Intent / cluster | Primary owner |
|---|---|
| Softwareentwicklung / Softwareentwickler Lübeck | `/softwareentwicklung-luebeck/` |
| Individualsoftware cost / Make-or-Buy / Standardsoftware comparison | `/wissen/individualsoftware-kosten/` |
| API / Schnittstellen implementation | `/softwareentwicklung-luebeck/#schnittstellen` |
| Webentwicklung / Webagentur / Webdesign Lübeck | `/webentwicklung-luebeck/` |
| Website Relaunch checklist / SEO / project plan / cost information | `/wissen/website-relaunch-checkliste/` |
| KI Automatisierung Lübeck / n8n implementation | `/ki-automatisierung-luebeck/` |
| KI Prozessautomatisierung decision / architecture | `/wissen/ki-prozessautomatisierung/` |

No intentional cluster has two primary owners. Standalone API, generic KI headterm, n8n authority, city-n8n and Systemintegration pages remain unbuilt. Kiel Web remains gated; Hamburg AI and Schleswig-Holstein Web remain HOLD.

## Authority acquisition plan

`AUTHORITY-ACQUISITION-PHASE-7.md` contains the prioritized, entity-safe shortlist.

Top immediate SAFE NOW opportunities:

1. Correct the public `DatenpflegeNordHL` GitHub identity: it is a **User** profile, not an Organization. The public API currently exposes Lübeck and `Datenpflege Nord`, five public repositories, but no profile website and no bio. Add the canonical domain and concise truthful scope without exposing the private production repository.
2. Strengthen useful public documentation around the self-owned `Codex-Looper` project; do not create empty repositories for links and do not present forks as own projects.
3. Continue substantive upstream OSS contributions and prepare permission-based project references where role and publication rights are explicit.

High-value targets after entity resolution include DigitalHub.SH, DiWiSH, the one correct Google Business entity, OMR Reviews/ProvenExpert where profile maintenance and genuine reviews are appropriate, plus a small number of relevant local citations. IT-Region Schleswig-Holstein is explicitly treated as potentially fee-bearing for a new enterprise account, not as a free backlink tactic.

Issue #13 safety is enforced throughout: current legal organization is `Green Vector Energo GmbH`, public brand is `DatenpflegeNord`, and no completed `NordWerk Digital GmbH` registration is claimed.

## Schema, sitemap and internal links

- Sitemap contains the new KI authority canonical with meaningful `2026-09-15` lastmod.
- Static audit recognizes 10 canonical HTML pages.
- Golden audit recognizes 3 service graphs and 3 authority graphs.
- KI authority ↔ local KI service links are contextual and bidirectional.
- KI authority links to the existing Software API/Schnittstellen section rather than creating a competing API owner.
- Ownership and internal-link documentation were updated for the 10-page / 3-authority architecture.

## Validation evidence

PASS:

- Static Site Audit: 10 HTML pages.
- Golden Audit: 10 reachable canonicals; 3 service graphs; 3 authority graphs.
- Canonical, internal-link, sitemap and affected hreflang checks through the static audit.
- Authority schema validation through the Golden audit.
- Asset Version Check: PASS, 79 references after adding the new KI authority HTML to the closed release allowlist.
- Asset Generator Idempotence: PASS, second generation produced zero changed files.
- New KI page asset hashes independently verified: 8 versioned local references matched final bytes, including the changed `authority.js` SHA-256.
- Secret scan: PASS, no credential-signature findings.
- Python source compile without bytecode writes: PASS, 20 files.
- Shell syntax: PASS for `dpn-deploy` and all four deployment helper scripts.
- JavaScript syntax: PASS for home DE/EN, service and authority assets.
- YAML parsing: PASS for both GitHub workflow files.
- `git diff --check`: PASS on the staged Phase-7 implementation.
- Full `python3 -m unittest discover -s tests`: 78 run, 16 expected environment/privilege/browser-fixture skips, PASS.

Real Brave browser QA PASS:

- New KI authority page at 1440 px, 390 px and 320 px: no document-level horizontal overflow, one H1, no heading-level skips, usable CTA, matrix present.
- Keyboard Tab moved focus to a visible 3 px outline on the skip link.
- Emulated `prefers-reduced-motion: reduce` reduced maximum transition/animation duration to effectively zero.
- Automation Decision Matrix selected the AI-assisted branch for unstructured/partly-rule-based input, persisted through reload, reset to defaults and returned focus to the first control.
- JavaScript-disabled load retained definition, architecture, matrix HTML and more than 10,000 characters of readable core content; no JS-generated question list appeared.
- Relaunch page at 1440/390/320: no document-level horizontal overflow, correct heading hierarchy, cost/project-plan/SEO migration sections present.
- Relaunch checklist persisted through reload and reset from 1/36 back to 0/36.
- Visual screenshots at all three KI widths were inspected; no clipping or broken responsive layout was observed.
- Narrow-screen authority typography was tightened after the 320 px visual review; the final browser probe reports document `scrollWidth == clientWidth` at 1440, 390 and 320 px.

## Release-candidate gate resolution

The first full-suite rerun exposed one real packaging gap in `test_release_candidate.ReleaseCandidateTests.test_finalized_archive_manifest_and_no_mutation`: the closed release allowlist in `ops/deploy/dpn-deploy` did not yet contain `wissen/ki-prozessautomatisierung/index.html`.

The source allowlist now includes exactly that new public HTML path. No deployment was run. After the fix, the complete local suite passes: **78 tests, 16 expected skips, 0 failures/errors**. The canonical/Golden audits and asset generator also pass against the corrected package scope.

No validator or test was weakened or bypassed.

Hosted GitHub Actions run `34963094835` remains historical evidence for implementation SHA `6c3a21398a1cfc223beed8049494a34491141417` before the allowlist correction.

- That earlier hosted CI conclusion was **FAILURE**, isolated to the now-corrected release-candidate allowlist mismatch.
- The hosted log independently reports `BROWSER_FRESHNESS_PASS`: normal HTML navigation reached 304; changed HTML/leaf/CSS URLs were fetched; unchanged URL was retained; no cache clearing was used.
- Hosted asset-version and secret-scan output completed successfully before the unit-suite failure.

Hosted GitHub Actions run `34999400378` supersedes that result for validated source SHA `abf013131551e82738762b36ec47efb0b82a5f99`:

- Hosted CI conclusion: **SUCCESS**.
- Main suite: 78 tests, browser fixture active, 15 expected skips, PASS.
- Privileged install suite: 15 tests under `sudo`, PASS.
- `BROWSER_FRESHNESS_PASS` confirmed normal-navigation freshness without cache clearing.
- Static Site Audit: 10 HTML pages, PASS.
- Golden Audit: 10 reachable canonicals, 3 service graphs, 3 authority graphs, PASS.
- Exact release-candidate verification completed with `result: PASS`.

No production deployment was attempted or required to resolve this source-level gate.

## Gates retained

- GSC remains unavailable. Query-to-owner splits, regional expansion and future n8n/API splits must be revisited with first-party GSC evidence when available.
- Issue #13 remains OPEN; broad external legal/entity profile activation remains gated.
- Issue #10/#15 remain parked; Phase 7 did not alter their activation state.
- No regional landing pages were created.
- No production deployment or merge to `main` was performed.
