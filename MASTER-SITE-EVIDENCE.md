# MASTER SITE EVIDENCE — DatenpflegeNord

Status: canonical evidence pack for Golden Website Build 2.0
Last checked: 2026-09-10
Production repository: `DatenpflegeNordHL/datenpflege-nord-production`
Baseline commit: `65468e875fa0f4318cc07d7e4cbe843cacb24569`
Primary domain: `https://datenpflege-nord.de/`

## 1. Evidence policy

No SEO page, service claim, location claim, customer/reference claim or schema entity may be added from assumption alone. Evidence classes:

- **A — first-party verified:** repository/production-owned content or directly controlled account.
- **B — independent public evidence:** third-party/public source corroborates the fact.
- **C — measured search evidence:** keyword/SERP data from a current SEO/search source.
- **D — pending/unverified:** plausible or internally stated, but not safe to publish as established fact beyond already-required qualified wording.

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
| Pending company name | NordWerk Digital GmbH | A: Impressum says registration pending | **Pending** |

### Legal/entity rule

Until a current independent register source confirms the renaming, `Green Vector Energo GmbH` remains the legal organization name in Impressum and Organization schema. `NordWerk Digital GmbH` must not replace it as established legal identity merely because the filing is pending.

## 3. Verified service truth

Current first-party service offer:

1. Individual software development
   - web applications
   - internal tools
   - APIs
   - integrations/webhooks
   - database/system connections
   - extending existing systems
   - automation as part of software delivery
2. Web development
   - company websites
   - landing pages
   - web solutions/web applications
   - relaunch/technical modernization
   - integrations
3. AI and automation
   - AI agents
   - n8n workflows
   - LLM integrations
   - API integrations
   - controlled business-process automation
4. Systems/interfaces
   - APIs
   - databases
   - webhooks
   - data flows between existing systems

Tools named publicly as development tools include GitHub, Claude Code and OpenAI Codex. These are implementation tools, not separate customer outcomes and therefore must not become primary SEO landing-page targets without search/business evidence.

## 4. Current production URL inventory

Indexable URLs present in the canonical sitemap:

- `/`
- `/softwareentwicklung-luebeck/`
- `/webentwicklung-luebeck/`
- `/ki-automatisierung-luebeck/`
- `/en/`
- `/impressum/`
- `/datenschutz/`

Robots currently allows crawling and references `/sitemap.xml`.

### Sitemap defect

The current sitemap still reports `lastmod` 2026-08-09 for the main service URLs and 2026-08-08/09 for legal pages while `main` contains verified changes through 2026-09-08. `lastmod` must reflect meaningful page changes or be generated from a deterministic source; stale dates are not acceptable as canonical build metadata.

## 5. Metadata/entity observations

### Strong baseline

- unique canonical URLs exist on reviewed pages;
- homepage has DE/EN hreflang including x-default;
- service pages expose WebPage + Service + BreadcrumbList JSON-LD;
- homepage exposes Organization + WebSite JSON-LD;
- one H1 policy and basic accessibility checks are enforced by repository audit code;
- social metadata exists;
- local resource existence, unsafe inline executable content, form labelling and several CSP/accessibility regressions are checked deterministically.

### Current inconsistency

Homepage search metadata positions the company as software development, web development and AI automation. Homepage Open Graph/Twitter copy instead says “Website-Checks und KI-Systeme für KMU” and references technical website checks/digital obligations. These messages describe different offers and must be reconciled before further entity/content expansion.

## 6. Search visibility baseline

Current evidence on 2026-09-10:

- Ubersuggest returned no domain overview data for `datenpflege-nord.de` in Germany.
- Multiple exact web searches combining the brand with software development, web development and AI automation returned no result in the queried search corpus.

Interpretation: do **not** claim that the domain is unindexed. Treat this as “no independently measured organic visibility baseline currently available from the checked sources.” Search Console remains the preferred first-party source for index coverage, impressions, queries and CTR.

## 7. Measured keyword evidence — first pass

Germany, German-language current keyword data checked 2026-09-10:

| Query | Monthly volume | SEO difficulty | CPC | Intent/source note |
|---|---:|---:|---:|---|
| softwareentwicklung lübeck | 110 | 17 | €2.74 | Commercial |
| webentwicklung lübeck | 70 | 55 | €4.58 | Informational in provider dataset; SERP still commercially mixed |
| ki automatisierung | 1,600 | 35 | €8.50 in related dataset | Commercial |
| ki automatisierung agentur | 170 | 17 | €11.76 | Navigational-labelled provider data; commercial landing-page SERP |
| n8n automatisierung | 110 | 10 | €5.51 | Strong specialist opportunity |
| ki agenten unternehmen | 20 | 31 | ~€11.67 | Low-volume but high commercial relevance |
| ki automatisierung für unternehmen | 10 | 23 | ~€9.86 | Long-tail commercial relevance |

Raw autocomplete evidence also contains recurring variants around `KI Automatisierung Beratung`, `KI Automatisierung für KMU`, `KI Automatisierung Mittelstand`, `KI Automatisierung Prozesse`, `n8n Automatisierung Unternehmen`, `n8n Workflow Automatisierung`, `Website erstellen lassen Lübeck` and `Homepage erstellen lassen Lübeck`.

Do not publish a separate page merely because a suggestion exists. Volume, SERP overlap, business fit and cannibalization must all pass.

## 8. Current SERP competitor evidence

Observed current competitors/search-result archetypes include:

- software: local/region-targeted custom-software providers, including EXORD and TripleConsult;
- AI/automation in Lübeck: Digitalisierung Direkt, Hanse Computing, EDGE Digital and local/category aggregators;
- national AI automation: dedicated AI-automation agencies with detailed process/use-case architecture;
- n8n: specialist n8n agencies using dedicated service, industry/use-case and proof sections;
- web: Lübeck web-design/web-agency pages targeting “Website erstellen lassen”, not only the technical term “Webentwicklung”.

Common winning-page patterns observed:

- problem/outcome framing before tool lists;
- concrete use cases and connected systems;
- process/implementation steps;
- trust/proof sections;
- FAQ coverage;
- strong commercial CTA;
- clear audience such as SME/Mittelstand;
- deployment, privacy or EU-hosting claims where actually evidenced.

## 9. Proof/E-E-A-T inventory

Verified proof currently available:

- public GitHub profile linked by Organization schema;
- static and live-updated public GitHub activity on homepage;
- public pull requests/open-source work is explicitly separated from customer work;
- named direct contact person with portrait and role.

### Proof data gaps

The homepage includes five graphics under `images/clients-logo/` inside a visual brand belt. Before this section is treated as client/customer proof, verify for every logo:

1. identity of organization/brand;
2. actual relationship to DatenpflegeNord;
3. permission/right to display the mark;
4. wording allowed: client, project, partner, technology/reference, or decorative only.

Until verified, these graphics must not be converted into accessible/customer claims, schema, case studies or SEO proof.

## 10. Technical/deployment evidence

- `main` at baseline SHA is **not branch protected**.
- required status checks are not enforced on `main`.
- `.github/workflows/site-audit.yml` runs on pull requests to `main` and manual dispatch, not as a preventive gate for direct pushes.
- latest reviewed `main` commit has no combined commit statuses returned by the connector.
- deterministic repository checks already test titles/descriptions/canonicals at a basic level, social metadata, H1 count, duplicate IDs, resource existence, form labelling, JSON-LD validity, selected hreflang/DE-EN drift and CSP-related static rules.
- contact backend inventory documents loopback service `127.0.0.1:8091`, nginx `/api/contact`, DeoMail delivery, secret file outside the repository and a defined rollback procedure; that production parity was last explicitly audited in that README on 2026-08-25 and must be re-verified before backend deployment.

## 11. Performance evidence

Repository asset evidence:

- hero video: ~4.59 MB;
- hero poster: ~57 KB;
- homepage JS: ~15 KB per language file;
- homepage CSS: ~26 KB plus profile CSS ~3 KB;
- profile WebP: ~14 KB.

The hero video is `preload="none"`, uses a poster, and its source is assigned by JS only for fine-pointer/non-reduced-motion sessions. Therefore size alone is not proof of poor LCP, but network/CPU impact on eligible desktop sessions must be measured before declaring performance passed.

No fresh lab/field Core Web Vitals measurement is present in this evidence pack yet. Do not invent one.

## 12. Data gaps blocking final architecture

### P0/P1 blockers

- first-party Google Search Console index/query/CTR evidence;
- verified live HTTP/security/cache headers;
- fresh CWV/Lighthouse/CrUX evidence;
- production-vs-repo deployment parity after 2026-08-25 for backend and current static release;
- verified provenance/rights for client-logo belt;
- decision whether “Website-Checks / SEO / GEO / Performance” is an actual sellable DatenpflegeNord service or stale social-copy language;
- expanded keyword metrics for website-build, individual-software, API/integration and AI-consulting clusters;
- SERP-overlap check before splitting AI automation, n8n, AI agents and process automation into separate URLs.

## 13. Golden release rule

No change is considered complete until all applicable stages pass:

`Business Truth → Search/Intent Evidence → URL Ownership → Implementation → Static CI → Preview Review → Merge Gate → Production Deploy → Live HTTP/HTML/Schema/CWV Verification → Index/Ranking Monitoring`

A green repository alone is not production proof, and a working production page alone is not migration/deployment proof.
