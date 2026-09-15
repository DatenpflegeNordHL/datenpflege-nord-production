# Visibility Phase 5 — Authority and decision content

Date: 2026-09-15  
Branch: `golden-visibility-phase-5-authority`  
Base: `8656a3e73a88c99dae8fcea46cdcaab4e9dd0986`

## New canonical URLs and intent

| URL | Primary intent | Commercial owner | Boundary |
|---|---|---|---|
| `/wissen/individualsoftware-kosten/` | Informational-commercial decision support for cost drivers, scope and Make-or-Buy | `/softwareentwicklung-luebeck/` | Does not target local software procurement as its primary title or structure; contains no numeric price claim. |
| `/wissen/website-relaunch-checkliste/` | Relaunch planning, risk prevention and technical acceptance | `/webentwicklung-luebeck/` | Does not target Webdesign/Webagentur Lübeck as its primary intent. |

No other indexable page was added. The site now contains nine canonical HTML pages.

## Unique value

The Individualsoftware guide combines:

- an answer-first explanation of why price follows scope;
- concrete cost drivers before and after go-live;
- a four-option Standardsoftware / extension / integration / Individualsoftware matrix;
- a client-side 13-factor scope check that returns low, medium or high complexity rather than a fictional Euro estimate;
- dynamically selected clarification questions and a seven-step project path;
- browser-local state only, reset and an explicit no-transfer statement.

No internal quote dataset or sourced market benchmark exists in the reviewed evidence. The page therefore publishes no price range.

The Relaunch guide combines:

- a complete KEEP / UPDATE / MERGE / REDIRECT / REMOVE URL decision model;
- 36 visible tasks across preparation, staging, go-live and post-launch;
- local progress persistence and reset;
- release parity, canonical/slash, asset freshness, cache/revalidation, mobile widths, keyboard, reduced-motion, schema, sitemap and post-launch verification checks derived from the public-safe Golden process;
- a clear rejection of blanket homepage redirects.

All checklist and article content remains present when JavaScript is disabled. No internal paths, token handling, production topology or signing details are exposed.

## Schema and authorship

Both pages use one `TechArticle`, one `WebPage`, one `BreadcrumbList` and the existing entity-safe `Organization` identity. The visible author is Dustin Zander, already represented by the existing public profile. No title, certification, customer count or qualification was added. `Green Vector Energo GmbH` remains the legal organization and `DatenpflegeNord` its alternate public name. No FAQ, review, rating or LocalBusiness schema was added.

## Internal links and cannibalization

Each commercial owner links once to its supporting authority asset with a task-specific anchor. Each guide links back to its owner and offers contact only after the decision content. The guides do not link to each other and were not added to a global footer.

| Query cluster | Primary owner | Supporting page/section | Decision |
|---|---|---|---|
| Individualsoftware entwickeln lassen | `/softwareentwicklung-luebeck/` | Scope guide | Commercial owner retained. |
| Individualsoftware Kosten | `/wissen/individualsoftware-kosten/` | Money-page project-start summary | Authority page owns detailed cost/scope intent. |
| Softwareentwicklung Lübeck | `/softwareentwicklung-luebeck/` | None | Commercial owner retained. |
| Webdesign Lübeck | `/webentwicklung-luebeck/` | None | Commercial owner retained. |
| Website Relaunch, commercial/local | `/webentwicklung-luebeck/` | Checklist | Commercial owner retained. |
| Website Relaunch Checkliste | `/wissen/website-relaunch-checkliste/` | Money-page relaunch summary | Authority page owns planning intent. |
| KI Automatisierung Lübeck | `/ki-automatisierung-luebeck/` | None | Frozen pending first-party GSC query evidence. |

Result: one primary owner per cluster; no new regional or tool-specific owner.

## GSC readiness and sitemap

`GSC-VALIDATION-PLAN.md` now includes both URLs in the inspection list and a dedicated monitoring table for impressions, clicks, CTR, average position, query cluster, Google canonical and index status. The baseline starts only after real GSC access/data exists. No verification token was added.

Both new URLs were added to `sitemap.xml` with the actual publication date. Unchanged legal-page dates were not altered. The two changed Money pages already carry the same meaningful-content date.

## Deterministic validation

- Asset version generator: PASS; second run `changed_files=[]`.
- Asset checker: PASS; 71 versioned references across 14 assets.
- Static site audit: PASS; 9 HTML pages.
- Golden audit: PASS; 9 reachable canonical pages, three service graphs and two authority graphs.
- Python unit suite: 78 discovered, OK; 16 local environment skips. The separately executed browser suite covers the unavailable local browser fixture; privileged installer fixtures remain outside this content change.
- Browser suite: PASS; 12 checks covering both pages at 1440, 390 and 320 px with JavaScript enabled and disabled.
- Browser interactions: keyboard activation, visible focus, reduced motion, local-state persistence, reset and zero horizontal overflow PASS.
- Schema, canonical, sitemap and internal links: PASS through deterministic audits.
- Python compile, shell syntax, JavaScript syntax and workflow YAML parsing: PASS.
- Secret scan: PASS, no findings.
- `git diff --check`: PASS.

## HOLD decisions

Kiel Web, Hamburg AI, n8n city pages, API Lübeck, Systemintegration Lübeck and all further city clones remain HOLD/REJECT according to the existing gates. No KI/n8n authority page was created because first-party GSC assignment evidence is still unavailable. Issue #13 remains open; no register change or expanded legal-entity claim was introduced. Issue #10 and Issue #15 remain parked for later release activation.
