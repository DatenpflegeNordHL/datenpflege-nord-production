# MASTER SITE EVIDENCE — DatenpflegeNord

Status: canonical evidence pack for Golden Website Build 2.0
Last checked: 2026-09-10
Production repository: `DatenpflegeNordHL/datenpflege-nord-production`
Baseline commit: `65468e875fa0f4318cc07d7e4cbe843cacb24569`
Primary domain: `https://datenpflege-nord.de/`

## 1. Evidence policy

No SEO page, service claim, location claim, customer/reference claim or schema entity may be added from assumption alone. Evidence classes:

- **A — first-party verified:** repository/production-owned content or directly controlled evidence.
- **B — independent public evidence:** third-party/public source corroborates the fact.
- **C — measured search evidence:** current keyword/SERP/search-source data.
- **D — pending/unverified:** plausible or internally stated, but not safe to publish as established fact.

P0/P1 changes must not rely on D evidence.

## 2. Business truth

| Fact | Current truth | Evidence | Confidence |
|---|---|---|---|
| Public brand | DatenpflegeNord / Datenpflege Nord | A: production HTML/schema | High |
| Current legal entity | Green Vector Energo GmbH | A: Impressum/schema; B: public register index | High |
| Register | Amtsgericht Lübeck, HRB 25869 HL | A + B | High |
| Business address | Arnimstraße 35, 23566 Lübeck, Germany | A: Impressum/schema | High |
| Managing director / contact person | Dustin Zander | A: Impressum/homepage/schema | High |
| Public email | kontakt@datenpflege-nord.de | A: homepage/Impressum/backend config | High |
| Primary service region currently claimed | Lübeck + Schleswig-Holstein | A: homepage/service schema | High |
| Pending company name | NordWerk Digital GmbH | A: Impressum says registration pending | Pending |

### Legal/entity rule

Until a current independent register source confirms the renaming, `Green Vector Energo GmbH` remains the legal organization name in Impressum and Organization schema. `NordWerk Digital GmbH` must not replace it as established legal identity merely because the filing is pending.

## 3. Verified service truth

Current first-party service offer:

1. **Individual software development**
   - web applications and internal tools
   - APIs, webhooks and integrations
   - database/system connections
   - extension and modernization of existing systems
   - automation as part of software delivery
2. **Web development**
   - company websites and landing pages
   - web solutions/web applications
   - relaunch and technical modernization
   - integrations
3. **AI and automation**
   - AI agents
   - n8n workflows
   - LLM integrations
   - API integrations
   - controlled business-process automation
4. **Systems and interfaces**
   - APIs, databases, webhooks and data flows between existing systems

Tools named publicly include GitHub, Claude Code and OpenAI Codex. They are implementation tools, not separate customer outcomes, and must not become primary SEO targets without search and business evidence.

## 4. Current production URL inventory

Indexable URLs present in the current sitemap:

- `/`
- `/softwareentwicklung-luebeck/`
- `/webentwicklung-luebeck/`
- `/ki-automatisierung-luebeck/`
- `/en/`
- `/impressum/`
- `/datenschutz/`

Robots currently allows crawling and references `/sitemap.xml`.

### Sitemap `lastmod` status

The sitemap reports 2026-08-09 for most pages and 2026-08-08 for Impressum. Repository history contains later file changes, including frontend hardening on 2026-08-25 and a site-wide Open Graph/social-preview refresh on 2026-09-08.

The deeper history review changes the initial conclusion: a later file commit is **not automatically a later sitemap `lastmod`**. The 2026-09-08 change was primarily social-preview metadata/cache-busting, and 2026-08-25 contains technical hardening. Neither alone proves that the page's primary indexed content changed enough to justify a new `lastmod`.

Golden rule: sitemap dates must represent meaningful page changes and be traceable to a deterministic content/release rule. Do not stamp deployment dates, current dates or every file commit blindly. The current dates therefore remain **under review, not proven defective**.

## 5. Metadata/entity observations

### Strong baseline

- unique canonical URLs exist on reviewed pages;
- homepage has DE/EN hreflang including x-default;
- service pages expose WebPage + Service + BreadcrumbList JSON-LD;
- homepage exposes Organization + WebSite JSON-LD;
- one-H1 policy and basic accessibility checks are enforced by repository audit code;
- social metadata exists;
- local-resource existence, unsafe inline executable content, form labelling and several CSP/accessibility regressions are checked deterministically.

### Current message inconsistency

Homepage search metadata and visible content position the business as software development, web development and AI automation. Homepage Open Graph/Twitter copy instead says “Website-Checks und KI-Systeme für KMU” and references technical website checks/digital obligations.

Do not reconcile this by guess. First determine whether Website-Checks/SEO/GEO/Performance are a current sellable service or stale campaign/social copy. Then make title, visible copy, social metadata, schema and landing-page ownership consistent.

## 6. Search visibility baseline

Current evidence on 2026-09-10:

- Ubersuggest returned no domain-overview data for `datenpflege-nord.de` in Germany.
- Multiple exact public searches combining the brand with core services produced no result in the queried search corpus.

Interpretation: this does **not** prove that the domain is unindexed. It means no independently measured organic visibility baseline is currently available from the checked sources. Google Search Console remains the preferred first-party source for coverage, impressions, queries, positions and CTR.

## 7. Measured keyword evidence — first pass

Germany, German-language data checked 2026-09-10:

| Query | Monthly volume | SEO difficulty | CPC | Decision signal |
|---|---:|---:|---:|---|
| softwareentwicklung lübeck | 110 | 17 | €2.74 | Strong local commercial target |
| webentwicklung lübeck | 70 | 55 | €4.58 | Existing page valid, but commercial wording needs SERP comparison |
| ki automatisierung | 1,600 | 35 | ~€8.50 | Large non-local market; requires service-area decision + overlap gate |
| ki automatisierung agentur | 170 | 17 | €11.76 | Commercial sub-intent, likely same hub initially |
| n8n automatisierung | 110 | 10 | €5.51 | Strong specialist candidate, not yet approved as separate URL |
| ki agenten unternehmen | 20 | 31 | ~€11.67 | Relevant but low volume; likely section/supporting intent initially |
| ki automatisierung für unternehmen | 10 | 23 | ~€9.86 | Supporting commercial long-tail |

Autocomplete evidence additionally repeats variants around `KI Automatisierung Beratung`, `KI Automatisierung für KMU`, `KI Automatisierung Mittelstand`, `KI Automatisierung Prozesse`, `n8n Automatisierung Unternehmen`, `n8n Workflow Automatisierung`, `Website erstellen lassen Lübeck` and `Homepage erstellen lassen Lübeck`.

Do not publish a separate page because an autocomplete suggestion exists. Volume, SERP overlap, business fit, proof and cannibalization must all pass.

## 8. Current SERP evidence and competitor archetypes

Observed current result patterns include:

- local software providers targeting individualized software and business-process solutions;
- local web providers targeting **“Website erstellen lassen”** more directly than the technical phrase “Webentwicklung”;
- AI-automation providers leading with business process, integration, control/governance and measurable outcomes;
- n8n specialists using dedicated commercial service pages, connected-system examples and workflow/use-case proof;
- AI-agent pages using distinct process examples but substantial semantic overlap with broader AI automation.

Common useful patterns, only where truthfully supportable:

- problem/outcome framing before tool lists;
- concrete use cases and connected systems;
- implementation/process steps;
- verifiable project/repository/customer proof;
- FAQ coverage for real decision questions;
- direct commercial CTA;
- explicit audience such as SMEs/Mittelstand when it matches the offer;
- privacy/hosting/governance claims only with evidence.

## 9. Proof / E-E-A-T inventory

Verified proof currently available:

- public GitHub profile linked by Organization schema;
- static and live-updated public GitHub activity on homepage;
- public pull requests/open-source work explicitly separated from customer work;
- named direct contact person with portrait and role;
- repository contains deterministic site checks and documented contact-backend deployment/rollback procedure.

### Client-logo proof gap

The homepage contains five graphics under `images/clients-logo/` in a visual brand belt. Before treating any as client/customer proof, verify for every logo:

1. identity of organization/brand;
2. actual relationship to DatenpflegeNord;
3. permission/right to display the mark;
4. permitted wording: client, project, partner, technology/reference, or decorative only.

Until verified, do not turn these graphics into accessible customer claims, schema, case studies or SEO proof.

## 10. Technical / deployment evidence

Baseline state:

- `main` is **not branch protected**;
- required status checks are not enforced on `main`;
- the baseline static audit ran for pull requests to `main` and manual dispatch only;
- latest reviewed baseline `main` commit returned no combined commit statuses;
- deterministic checks already cover core metadata/canonical structure, H1 count, duplicate IDs, resources, labels, JSON-LD parseability, selected hreflang/DE-EN drift, social metadata and CSP-related static rules;
- backend inventory documents loopback contact service, nginx route, external secret storage, rate limiting and rollback; its explicit production-parity statement dates to 2026-08-25 and must be re-verified before backend deployment.

Golden-build branch changes:

- canonical evidence pack added;
- static site audit additionally runs on pushes to `main` as a **post-push backstop**;
- social-preview workflow changed to manual-only and its GitHub Actions dependencies pinned to immutable SHAs.

Important: the push audit is not a substitute for branch protection. Preventive protection with required PR/status checks remains a P0 administrative gate.

## 11. Performance evidence

Repository asset evidence:

- hero video: ~4.59 MB;
- hero poster: ~57 KB;
- homepage JS: ~15 KB per language file;
- homepage CSS: ~26 KB plus profile CSS ~3 KB;
- profile WebP: ~14 KB.

The hero video is `preload="none"`, has a poster, and its source is assigned by JS only for fine-pointer/non-reduced-motion sessions. Size alone is therefore not proof of poor LCP. Eligible desktop transfer/CPU impact still requires measurement.

No fresh lab/field Core Web Vitals result is currently in this evidence pack. Do not invent a performance pass.

## 12. Data gaps blocking final architecture / release

### P0

- branch protection + required PR/status-check gate for `main`;
- fresh production-vs-repository parity check before any deployment;
- verified live HTTP/security/cache headers before final technical sign-off.

### P1

- Google Search Console query/index/CTR evidence;
- fresh Lighthouse/CrUX/Core Web Vitals evidence;
- verified provenance/rights for client-logo belt;
- business decision/evidence for Website-Checks / SEO / GEO / Performance as a public service;
- expanded metrics for Website-erstellen-lassen/Webdesign, Individualsoftware, API/Integration and AI-consulting clusters;
- SERP-overlap gate before splitting AI automation, n8n, AI agents and process automation into separate URLs;
- deterministic sitemap `lastmod` policy.

## 13. Golden release rule

No change is complete until all applicable stages pass:

`Business Truth → Search/Intent Evidence → URL Ownership → Implementation → Static CI → Preview Review → Merge Gate → Production Deploy → Live HTTP/HTML/Schema/CWV Verification → Index/Ranking Monitoring`

A green repository alone is not production proof, and a working production page alone is not migration/deployment proof.
