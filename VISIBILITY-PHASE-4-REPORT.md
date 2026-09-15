# Visibility Phase 4 report

Date: 2026-09-15  
Branch: `golden-visibility-phase-4`  
Base: `ae276eddbbfb65dfd7e63c6ca74bb8ff0e19730c`

## Scope and changed URLs

This release candidate changes content on `/`, `/en/`, `/softwareentwicklung-luebeck/`, `/webentwicklung-luebeck/` and `/ki-automatisierung-luebeck/`. It creates no indexable URL. Meaningful-content `lastmod` changes are limited to those five URLs; legal pages remain unchanged.

The service pages already contained the Phase 1–3 decision sections. Phase 4 retains that depth and adds only missing commercial vocabulary where it answers an existing buyer question. It does not turn the pages into repeated FAQ collections.

## Homepage proof and positioning

- Removed five unattributed template logos and the complete logo belt from DE/EN markup, CSS and assets. They had no repository evidence tying them to clients, partners or shipped work.
- Removed the template Hero video/poster and its pointer-seeking JavaScript because the media visibly contained generic template headlines and buttons. A CSS-only background now carries no implied customer or product proof.
- Replaced the unsupported numeric repository fallback with an em dash. The browser may still obtain live values from the public GitHub API; the label now describes all public GitHub repositories consistently.
- Corrected the static OpenJarvis PR #708 status from open to merged after checking the public PR. Static proof entries now carry an explicit 2026-09-15 check date.
- Retained factual public GitHub links, their own/external scope labels, Dustin Zander's visible contact role, the Lübeck/Schleswig-Holstein operating region and the current legal entity.
- Added an answer-first Hero passage describing who is helped, the operational problems addressed, the four evidenced delivery areas and the next actions. The visible line `DatenpflegeNord · Green Vector Energo GmbH` keeps brand and operator together.
- Aligned German Open Graph and Twitter copy with the visible software/web/interfaces/controlled-automation offer. Removed the stale Website-Checks/digital-obligations positioning.

## Query cluster ownership and cannibalization

| Query cluster | Owner URL | Supporting section | Competing URL | Decision |
|---|---|---|---|---|
| DatenpflegeNord / Lübeck / Schleswig-Holstein services | `/` | Hero, service overview, public technical proof and contact | `/en/` is language support only | OWN |
| Softwareentwicklung Lübeck / Softwareentwicklungsagentur | `/softwareentwicklung-luebeck/` | Hero, `#entscheidung`, `#projektstart` | None | EXPAND existing owner |
| Individuelle Softwareentwicklung / Individualsoftware entwickeln lassen | `/softwareentwicklung-luebeck/` | `#entscheidung` comparison table | `/individualsoftware/` | HOLD separate URL |
| Schnittstellenentwicklung / Schnittstellenprogrammierung / API-Entwicklung / API-Programmierung / API-Integration | `/softwareentwicklung-luebeck/` | `#schnittstellen`; homepage assigns the interface card here | `/api-schnittstellenentwicklung/`, generic API page | HOLD separate URL |
| Webentwicklung / Webdesign / Webdesigner / Webagentur Lübeck | `/webentwicklung-luebeck/` | Hero and `#entscheidung` | `/webdesign-luebeck/` | HOLD separate URL |
| Website erstellen lassen / Unternehmenswebsite / Landingpage / Relaunch | `/webentwicklung-luebeck/` | Services, `#entscheidung`, `#projektstart` | Landingpage or website-create variants | HOLD separate URLs |
| KI-Automatisierung / KI-Agenten / LLM-Integrationen | `/ki-automatisierung-luebeck/` | Hero, service scope and `#entscheidung` | National AI hub, Hamburg/Kiel pages | HOLD |
| Prozessautomatisierung / Workflow-Automatisierung / n8n-Automatisierung | `/ki-automatisierung-luebeck/` | Services, rule/n8n/AI decision and `#projektstart` | `/n8n-automatisierung/`, city n8n clones | SUPPORT within existing owner; clones blocked |
| Webanwendung with business logic | `/softwareentwicklung-luebeck/` | Individual-software comparison; W links here | `/webentwicklung-luebeck/` | W describes websites/frontends and delegates application logic to S |
| Systemintegration broad acquisition | None | Narrow system-connection language under S only | Generic system-integration page | REJECT/HOLD |

Result: one canonical owner remains assigned to every commercial cluster. No doorway, synonym or regional clone was created.

## Decision content retained and clarified

- **Software:** standard software versus extension/custom build, internal tools, modernization, APIs/webhooks/databases, data ownership, failure paths, cost drivers, source/use/maintenance responsibilities and first-assessment inputs. Added natural software-agency and API-programming language.
- **Web:** company websites, landing pages, relaunch/modernization, responsive delivery, technical performance foundations, crawlable metadata/internal links, contact paths, integrations, cost drivers, acceptance checks and maintenance responsibility. Clarified the landing-page buyer question.
- **Automation:** repeatable data transfer, structured information processing, n8n workflows, LLM integration, bounded AI agents, API-triggered steps, failure handling and human approval. Added explicit process/n8n-automation wording while retaining rule-first guidance.

No fixed prices, savings percentages, ranking guarantees, autonomous-employee claims, generic SEO/GEO agency offer or unsupported maintenance promise was added.

## Internal links and schema

The homepage now links the systems/interfaces card directly to `/softwareentwicklung-luebeck/#schnittstellen`. Existing owner-to-owner decision links and contact CTAs remain descriptive and intact. All seven canonical pages remain reachable from home.

No FAQPage, LocalBusiness, Review or AggregateRating schema was added. Existing Service/WebPage/Breadcrumb graphs remain aligned with visible content. `Green Vector Energo GmbH` remains the legal Organization and `DatenpflegeNord` the public alternate brand. Canonicals, hreflang and page count are unchanged.

## Entity-safe authority decisions

Issue #13 remains open. No independent evidence of a completed NordWerk Digital GmbH registration or changed software/digital corporate purpose was found in the supplied evidence or introduced during this work. The authority plan now separates factual brand, GitHub, author and real-project work that is SAFE NOW from legal-entity citation expansion that must WAIT FOR REGISTER UPDATE. No sameAs expansion or second Google Business entity was created.

## GSC readiness

No Search Console access or data is claimed. `GSC-VALIDATION-PLAN.md` now records the domain-property target, canonical domain, verification requirements, sitemap URL, seven-URL inspection list, connection-date baseline rule and a query/page monitoring template. It contains no verification token.

## Remaining HOLD items

- Kiel Web page
- Hamburg AI page and all unsupported Hamburg service pages
- city-specific n8n pages
- standalone API page
- broad Systemintegration acquisition page
- national service hubs without explicit service-area and unique-value evidence
- legal-name/purpose migration and aggressive entity citations pending Issue #13
- any client/reference/review claim without evidence and permission

## Validation record

Populate after final generation and tests:

- Static site audit: PASS — seven HTML pages.
- Golden audit: PASS — seven reachable canonical pages, three service graphs and homepage proof gate.
- Asset-version checker: PASS — 55 references to 12 assets, no missing or wrong version.
- Asset generator idempotence: PASS — second run changed no file and preserved the complete diff hash.
- HTML/schema/internal-link/canonical/hreflang: PASS — no canonical or hreflang identity changed; no new route; schema remains entity-safe.
- Python/shell/JavaScript/YAML checks: PASS.
- Unit suite: PASS — 75 discovered, 59 executed locally, 16 intentionally skipped (15 root-only isolated installer fixtures and the separately executed browser fixture).
- Secret scan: PASS — no credential signatures found in tracked or pending files.
- Browser: PASS — 15 page/viewport combinations across 1440, 390 and 320 px; HTTP 200, zero horizontal overflow, headings/CTAs/decision sections present, keyboard focus visible, reduced-motion honored, zero console/page errors. Contact submission was not invoked.
- `git diff --check`: PASS.
