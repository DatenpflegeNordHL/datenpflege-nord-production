# MASTER SITE EVIDENCE — DatenpflegeNord

Status: canonical evidence pack for Golden Website Build 2.0
Last checked: 2026-09-10
Production repository: `DatenpflegeNordHL/datenpflege-nord-production`
Baseline production commit: `65468e875fa0f4318cc07d7e4cbe843cacb24569`
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

Issue #13 tracks the legal-purpose/name reconciliation before aggressive external entity/profile work.

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

Website-Checks / SEO / GEO / Performance remain a business-truth decision because social-preview messaging references them while the visible commercial architecture currently centers on software, web and AI automation.

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

A later file commit is **not automatically a later sitemap `lastmod`**. The 2026-09-08 change was primarily social-preview metadata/cache-busting, and 2026-08-25 contains technical hardening. Neither alone proves that primary indexed content changed enough to justify a new `lastmod`.

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

## 6. Search visibility and brand baseline

Current measured evidence on 2026-09-10:

- Ubersuggest backlink/domain data: Domain Authority 1, 0 backlinks, 0 referring domains.
- SE Ranking independently reports 0 backlinks, 0 referring domains and Domain InLink Rank 0.
- SE Ranking's German domain-keyword database returns no current organic keyword rows for `datenpflege-nord.de`.
- A manual SE Ranking project was created for `datenpflege-nord.de` with site audit disabled and position checking set to manual, preventing recurring trial-credit use.
- Ten priority keywords are attached to Google Germany rank tracking. Eight returned first position rows and were outside the tracked top 100; two had not yet produced position rows in the first status pull.
- Multiple exact public searches combining the brand with core services produced no result in the queried public search corpus.
- The visually similar domain `datenpflegenord.de` **without the hyphen** resolves in current search results to a different automotive-care/e-commerce site. It must never be treated as the DatenpflegeNord canonical domain or as first-party evidence.
- Google Search Console is not connected to the SE Ranking project and remains the preferred first-party source for impressions, queries, rankings, canonical/index status and CTR.

Interpretation: this does **not** prove that `datenpflege-nord.de` is unindexed. It does prove that the checked third-party datasets currently show no measurable organic footprint for the domain.

### Brand/domain-confusion risk

Because the no-hyphen domain is already associated with a different indexed website, protect brand/entity consistency aggressively:

- canonical domain remains exactly `https://datenpflege-nord.de/`;
- use the same domain in schema, social profiles, business listings, citations and backlinks;
- do not add `datenpflegenord.de` to `sameAs`, redirects, canonicals or citations unless ownership and purpose are independently verified in the future;
- monitor branded queries for spelling variants in Search Console once connected;
- strengthen independent brand/entity signals rather than attempting doorway pages for misspellings.

A structured local-business search did not produce a reliable DatenpflegeNord entity result in the checked source. Treat Google Business Profile / local-entity presence as a data gap, not as proof of absence.

## 7. Measured keyword evidence

### Preferred SE Ranking batch snapshot

Germany database, one batch endpoint, checked 2026-09-10:

| Query | Monthly volume | KD | CPC | Intent |
|---|---:|---:|---:|---|
| individuelle softwareentwicklung | 320 | 12 | €13.67 | Local + Commercial |
| softwareentwicklung agentur | 140 | 30 | €9.11 | Local + Commercial |
| ki automatisierung agentur | 140 | 17 | €6.10 | Informational classifier |
| softwareentwicklung lübeck | 110 | 34 | €0.62 | Local + Commercial |
| softwareentwicklung dienstleister | 110 | 39 | €15.14 | Local + Commercial |
| n8n automatisierung | 110 | 16 | €1.73 | Informational classifier |
| webentwicklung lübeck | 40 | 52 | €2.11 | Local + Commercial |
| ki agenten unternehmen | 20 | 15 | €3.81 | Informational classifier |
| website erstellen lassen lübeck | 10 | 45 | €0 | Local + Commercial |
| ki automatisierung lübeck | no data | no data | no data | no data |

The same SE Ranking history window shows `n8n automatisierung` rising from roughly 20/month in late 2025 to 110/month in the latest snapshot. `website erstellen lassen lübeck` remained around 10/month across the returned history.

### Cross-provider variance

Earlier Ubersuggest data estimated:

- `softwareentwicklung lübeck`: ~110/month, lower KD estimate;
- `webentwicklung lübeck`: ~70/month, KD ~55;
- `ki automatisierung`: ~1,600/month, KD ~35;
- `ki automatisierung agentur`: ~170/month, KD ~17;
- `n8n automatisierung`: ~110/month, KD ~10;
- `ki agenten unternehmen`: ~20/month.

Do not average provider disagreement into fake precision. Search Console remains the first-party tie-breaker after indexing/visibility exists.

Autocomplete evidence additionally repeats variants around `KI Automatisierung Beratung`, `KI Automatisierung für KMU`, `KI Automatisierung Mittelstand`, `KI Automatisierung Prozesse`, `n8n Automatisierung Unternehmen`, `n8n Workflow Automatisierung`, `Website erstellen lassen Lübeck` and `Homepage erstellen lassen Lübeck`.

Do not publish a separate page because an autocomplete suggestion exists. Volume, SERP overlap, business fit, proof and cannibalization must all pass.

## 8. Current SERP evidence and competitor archetypes

### Softwareentwicklung Lübeck

A city-targeted Lübeck Google snapshot shows a mixed-intent SERP with substantial job/study noise, but genuine commercial software providers also rank prominently. EXORD and RXM are among the visible commercial providers. DatenpflegeNord did not appear in the returned snapshot.

Implication: the existing `/softwareentwicklung-luebeck/` owner is valid, but copy must clearly signal buyer/service intent rather than competing semantically with employment/education pages.

### Webentwicklung Lübeck / Website erstellen lassen Lübeck

The Lübeck web-development SERP strongly blends Webentwicklung, Webdesign, Website-Erstellung and agency intent. Review-rich/local-business providers are common. The exact `website erstellen lassen lübeck` SERP is smaller and noisier while clearly belonging to the same procurement journey.

Implication: keep `/webentwicklung-luebeck/` as one owner and expand semantic/commercial coverage. Do not create a duplicate `website-erstellen-lassen-luebeck` page.

### n8n Automatisierung

The tracked German top-30 snapshot for `n8n automatisierung` is mixed informational + commercial:

- informational/vendor results include IONOS and n8n itself;
- commercial service providers also rank;
- `n8n-agentur.de` ranked at position 6 in the tracked snapshot;
- TEAM23's n8n service page ranked at position 10.

The SERP-distinction gate therefore passes more strongly than in the first audit, but the intent is not purely transactional. A future standalone n8n page must combine implementation/service value with real educational/process substance.

### Competitor content architecture

- EXORD can rank its homepage for the exact local software cluster, showing that a lexical child page is not required for every term.
- Netzhirsch distributes web visibility across a commercial agency/service page and supporting knowledge content.
- Established local web competitors frequently combine service clarity, reviews, local entity signals, proof and explicit conversion CTAs.

## 9. Authority and AI-search evidence

### Referring-domain benchmark

SE Ranking snapshot 2026-09-10:

| Domain | Backlinks | Referring domains | Domain InLink Rank |
|---|---:|---:|---:|
| `datenpflege-nord.de` | 0 | 0 | 0 |
| `exord.de` | 326 | 127 | 55 |
| `hansolu.de` | 24,288 | 374 | 67 |
| `www.iseo.de` | 1,599 | 396 | 63 |
| `www.netzhirsch.de` | 9,196 | 458 | 71 |

HANSOLU and Netzhirsch have large sitewide design-credit/footer-link patterns, so raw backlink counts overstate unique authority. The referring-domain and source-quality gap remains material even after that caveat.

### AI Search baseline

SE Ranking does not currently resolve a stored AI-search brand for `datenpflege-nord.de`. Explicit `DatenpflegeNord` analysis across Google AI Overview, Google AI Mode, ChatGPT, Perplexity and Gemini returns:

- brand presence: 0;
- link presence: 0;
- share of voice: 0;
- AI opportunity traffic: 0;
- average position: not measurable.

Competitor comparison:

| Brand | Brand presence | Link presence | Share of voice |
|---|---:|---:|---:|
| Netzhirsch | 39 | 92 | 61.20% |
| ISEO | 32 | 23 | 30.33% |
| HANSOLU | 1 | 15 | 6.36% |
| EXORD | 2 | 2 | 2.11% |
| DatenpflegeNord | 0 | 0 | 0% |

In this comparison the measurable competitor signal came from **Google AI Overview**. ChatGPT, Perplexity, Gemini and Google AI Mode returned zero for all five compared brands in the same dataset.

Netzhirsch's AI Overview-specific snapshot reports brand presence 39, link presence 92, AI opportunity traffic 26 and average position 10.82.

Interpretation: there is no evidence that an AI-specific schema trick will solve this. The measurable gap is broader entity/content/authority distribution.

## 10. Proof / E-E-A-T inventory

Verified proof currently available:

- public GitHub profile linked by Organization schema;
- static and live-updated public GitHub activity on homepage;
- public pull requests/open-source work explicitly separated from customer work;
- named direct contact person with portrait and role;
- repository contains deterministic site checks and documented contact-backend deployment/rollback procedure.

### Template client-logo belt — resolved in Draft PR #12

The five homepage `images/clients-logo/` graphics were traced to the upstream `pulkitxm/claude-directory` Tailgrids/SynthAI template and are not verified DatenpflegeNord clients.

Draft PR #12 removes the complete logo belt, associated CSS and the five SVG assets. It also corrects static GitHub proof fallbacks, including OpenJarvis PR status/date accuracy and removal of an unverifiable hard-coded public-repository count.

The proof gap is therefore **resolved in the staged code**, but not yet production truth because PR #12 remains unmerged/unreleased.

## 11. Technical / deployment evidence

Baseline production state:

- `main` is **not branch protected**;
- required status checks are not enforced on `main`;
- deterministic checks cover core metadata/canonical structure, H1 count, duplicate IDs, resources, labels, JSON-LD parseability, selected hreflang/DE-EN drift, social metadata and CSP-related static rules;
- backend inventory documents loopback contact service, nginx route, external secret storage, rate limiting and rollback; its explicit production-parity statement dates to 2026-08-25 and must be re-verified before backend deployment.

Golden staged work:

- PR #9: evidence baseline, keyword/authority maps, release verification runbook, local third-party MIT license, workflow hardening;
- PR #11: content strengthening of the three existing service pages only;
- PR #12: template-logo/proof cleanup;
- PR #14: contact-service systemd hardening + backend tests/CI;
- PR #16: deterministic allowlist-based public release package, SHA-256 manifest, strict verifier and CI artifact upload.

### Release-package proof

PR #16 builds a deterministic package:

- `release-package/webroot/` = explicitly allowlisted public files only;
- `release-package/RELEASE-MANIFEST.sha256` = metadata outside public webroot;
- manifest verification rejects changed, missing, extra and symlinked files;
- the verified package contains 28 public files;
- CI uploads the tested package as a GitHub Actions artifact.

This solves the repository-side publication boundary. Issue #15 remains P0 for the **server-side transport/activation contract**: actual `/usr/local/sbin/dpn-deploy`, nginx/webroot mapping, ownership/modes, rollback and production parity still require server evidence.

### Branch protection

Issue #10 remains P0. GitHub Rulesets for this private repository require a plan/visibility capability not currently available through the checked API path, and the connected GitHub App cannot use classic administration endpoints. Do not make the production repository public merely to obtain protection.

## 12. Performance evidence

Repository asset evidence:

- hero video: ~4.59 MB;
- hero poster: ~57 KB;
- homepage JS: ~15 KB per language file;
- homepage CSS: ~26 KB before the staged proof-cleanup removal of the logo-belt CSS;
- profile WebP: ~14 KB.

The hero video is `preload="none"`, has a poster, and its source is assigned by JS only for fine-pointer/non-reduced-motion sessions. Size alone is therefore not proof of poor LCP. Eligible desktop transfer/CPU impact still requires measurement.

No fresh lab/field Core Web Vitals result is currently in this evidence pack. Do not invent a performance pass.

Live HTTP/nginx/Cloudflare verification remains a data gap because the current shell environment could not resolve external DNS reliably. That environment failure is not evidence that the production domain is down.

## 13. Data gaps blocking final architecture / release

### P0

- branch protection + required PR/status-check gate for `main`;
- server-side deployment-contract verification for `/usr/local/sbin/dpn-deploy`, document root, ownership, activation and rollback;
- fresh production-vs-reviewed-release parity check before any deployment;
- verified live HTTP/security/cache headers before final technical sign-off.

### P1

- Google Search Console query/index/CTR/canonical evidence;
- fresh Lighthouse/CrUX/Core Web Vitals evidence;
- verified local/business-profile entity signals;
- business decision/evidence for Website-Checks / SEO / GEO / Performance as a public service;
- Business Truth decision whether n8n implementation is a named standalone sellable service;
- explicit service-area decision before a national `/ki-automatisierung/` hub;
- deterministic sitemap `lastmod` policy;
- post-release browser verification of CSP report-only → enforcing eligibility.

Resolved/staged rather than still open:

- template client-logo provenance is resolved through Draft PR #12 removal;
- repository-side deterministic public webroot packaging/parity mechanism is implemented and tested in Draft PR #16;
- backend static/systemd hardening is implemented and CI-verified in Draft PR #14, though production parity remains open.

## 14. Golden release rule

No change is complete until all applicable stages pass:

`Business Truth → Search/Intent Evidence → URL Ownership → Implementation → Static CI → Preview Review → Merge Gate → Production Deploy → Live HTTP/HTML/Schema/CWV Verification → Index/Ranking Monitoring`

Release truth must additionally satisfy:

`Repository Truth → Preview Truth → Production Truth`

A green repository alone is not production proof, and a working production page alone is not migration/deployment proof.
