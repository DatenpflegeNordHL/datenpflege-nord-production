# KEYWORD / INTENT MAP — DatenpflegeNord

Status: Golden Website Build 2.0 URL-ownership gate
Last checked: 2026-09-10
Rule: **one primary commercial intent owner per URL**. Synonyms do not earn separate pages by themselves.

## 1. Gate used before a new indexable page exists

A candidate URL must pass all applicable checks:

1. **Business truth** — the service is genuinely offered and can be delivered.
2. **Intent distinction** — the user problem/journey is materially different from an existing page.
3. **SERP distinction** — competing result sets and page archetypes support a separate intent.
4. **Demand** — measured search demand or strong strategic commercial value exists.
5. **Proof** — the page can contain specific, verifiable substance rather than generic claims.
6. **Cannibalization** — it will not fight an existing URL for the same primary query set.
7. **Conversion fit** — the visitor has a clear next action relevant to the business.
8. **Maintenance fit** — the page can remain accurate after launch.

Statuses:

- **OWN** = current/approved intent owner.
- **EXPAND** = keep URL, improve its coverage before creating siblings.
- **HOLD** = promising candidate, but one or more gates are still unresolved.
- **BLOCK** = do not build until business/evidence changes.

## 2. Evidence-source rule

Keyword metrics are third-party estimates, not ground truth. Current evidence combines Ubersuggest, SE Ranking and direct current Google SERP snapshots. Where providers disagree, the disagreement is retained rather than averaged into a fake precision.

Google Search Console remains the first-party tie-breaker for actual impressions, clicks, CTR, ranking URLs and cannibalization once connected.

Current SE Ranking pre-deployment baseline (Germany, 2026-09-10):

- `datenpflege-nord.de` returned no organic keyword rows in the SE Ranking domain database;
- the first manual rank-tracking check returned eight measured priority queries, all outside the tracked Google top 100;
- backlink baseline: 0 backlinks / 0 referring domains / Domain InLink Rank 0;
- AI Search baseline: Link Presence 0, AI Opportunity Traffic 0, Brand Presence not yet measurable.

These are baseline measurements, not permanent conclusions about Google indexing.

## 3. Current URL ownership

| URL | Primary intent owner | Supporting intents | Status | Action |
|---|---|---|---|---|
| `/` | DatenpflegeNord brand + service overview | Software, web, AI/automation, systems/integrations, Lübeck/SH | OWN | Keep as brand/entity/conversion hub; reconcile OG/social message with actual offer |
| `/softwareentwicklung-luebeck/` | software development Lübeck | individual software, software agency/provider, web apps, internal tools, APIs, integrations, modernization | OWN + EXPAND | Protect local commercial target; distinguish service intent from strong job/study SERP noise; do not split synonyms yet |
| `/webentwicklung-luebeck/` | web development / business websites Lübeck | webdesign, website creation, landing pages, relaunch, technical web improvement | OWN + EXPAND | Keep as single owner for overlapping webdesign/web-development/website-creation intent; strengthen proof/local trust rather than creating lexical siblings |
| `/ki-automatisierung-luebeck/` | AI automation Lübeck | AI agents, n8n, LLM/API workflows, process automation | OWN + EXPAND | Keep local owner; strengthen use cases/process/proof; n8n is strongest future specialist child candidate but remains gated |
| `/en/` | English brand/service overview | English discovery | OWN | Keep only while maintained as a deliberate English experience |
| `/impressum/` | legal provider identity | company/register/contact | OWN | Legal truth only; no SEO expansion |
| `/datenschutz/` | privacy information | contact-system processing | OWN | Legal/privacy truth only; no SEO expansion |

## 4. High-priority candidate intents

### A. `Softwareentwicklung Lübeck`

SE Ranking exact/local evidence on 2026-09-10:

- estimated DE volume: ~110/month;
- KD: 34;
- intent: Local + Commercial in keyword data;
- city-level Lübeck SERP is mixed: many job/study results, but genuine development providers also rank prominently;
- DatenpflegeNord was not present in the returned city-level snapshot.

**Status: OWN `/softwareentwicklung-luebeck/` + EXPAND.**

The query is worth defending, but not every estimated search is a buyer. The page should make service/procurement intent unmistakable through deliverables, process, integration capability, decision criteria and proof.

### B. `Individualsoftware` / `individuelle Softwareentwicklung`

SE Ranking signal for `individuelle softwareentwicklung`:

- estimated DE volume: ~320/month;
- KD: 12 in the keyword-expansion dataset;
- CPC signal is high in the expansion dataset (up to ~€13.67);
- strong commercial fit with the existing software offer.

**Status: EXPAND existing `/softwareentwicklung-luebeck/`.**

Do not create `/individualsoftware-luebeck/` as a lexical duplicate. The existing software page already owns the buyer journey and should absorb this terminology naturally.

Supporting commercial software phrases also reinforce the same owner:

- `softwareentwicklung agentur`: ~140/month, KD ~30, high CPC;
- `softwareentwicklung dienstleister`: ~110/month, KD ~39, very high CPC signal.

These are supporting procurement terms, not automatic new URLs.

### C. `Webentwicklung Lübeck` / Webdesign / Website creation

SE Ranking exact/local evidence:

- `webentwicklung lübeck`: ~40/month, KD 52, Local + Commercial;
- earlier Ubersuggest data estimated a somewhat higher volume; retain this as cross-provider variance, not a contradiction to be averaged away;
- city-level Google SERP strongly blends Webentwicklung, Webdesign, Website-Erstellung and agency intent;
- review-rich/local-business style competitors are common;
- DatenpflegeNord was not present in the returned city-level snapshot.

**Status: OWN + EXPAND existing `/webentwicklung-luebeck/`.**

Proof, reviews, local/entity authority, service clarity and conversion value are more important here than multiplying near-identical pages.

### D. `Website erstellen lassen Lübeck`

SE Ranking exact/local evidence:

- estimated DE volume: ~10/month;
- KD: 45;
- Local + Commercial;
- city-level SERP is much thinner and noisier than `webentwicklung lübeck`, with ads and several irrelevant/weak organic results;
- the query overlaps the same website-procurement journey.

**Status: EXPAND existing `/webentwicklung-luebeck/`, not a new page.**

This now has stronger evidence than the earlier autocomplete-only decision. A separate `/website-erstellen-lassen-luebeck/` would create unnecessary cannibalization risk for a small exact local query.

### E. `KI Automatisierung` — national/non-local hub

Earlier Ubersuggest evidence showed materially larger broad demand for `KI Automatisierung`, while SE Ranking's related-query set shows broad terms are often informational and commercially ambiguous.

SE Ranking does show a stronger procurement phrase:

- `ki automatisierung agentur`: ~140/month;
- KD: 17;
- CPC: ~€6.10.

**Status: HOLD.**

Why it remains attractive:

- commercial agency/procurement demand exists;
- current service truth includes agents, n8n, LLM and API workflows;
- national AI-automation SERPs contain service providers.

Blockers before `/ki-automatisierung/` may exist:

- current Organization/service-area truth is Lübeck + Schleswig-Holstein;
- need explicit business decision/evidence that projects are accepted nationally/remotely;
- must compare Search Console/real-query overlap with `/ki-automatisierung-luebeck/` after indexing;
- need enough proof/use cases to avoid a generic national agency page.

If approved later: national hub owns broad national procurement intent, while the local page owns location-modified Lübeck/SH intent without duplicating copy.

### F. `n8n Automatisierung`

SE Ranking exact tracked keyword evidence:

- estimated DE volume: ~110/month;
- CPC: ~€1.66 in the tracked dataset;
- first tracked position: outside top 100 on 2026-09-10;
- the current German SERP is mixed informational + commercial and contains AI Overview;
- dedicated commercial n8n agency/service URLs occur repeatedly, including specialist implementation providers.

**Status: HOLD — strongest specialist child candidate.**

The SERP-distinction gate now passes much more strongly than in the first audit. The remaining blockers are Business Truth and proof: DatenpflegeNord must explicitly sell n8n implementation as a named standalone service, and the page must be able to show real integration/process substance rather than generic tool copy.

Until then, `/ki-automatisierung-luebeck/` owns n8n intent as a substantial section.

### G. `KI Agenten für Unternehmen`

Earlier measured exact-ish demand was low, but current SERPs support a distinct commercial concept around permissions, integrations, human approval and governance.

**Status: HOLD.**

Start as a substantial decision/use-case cluster under AI automation. Promote to its own URL only if Search Console, expanded keyword evidence and SERP overlap show independent demand and the page can contain concrete implementation proof.

### H. API / Schnittstellen / Systemintegration

Business fit is verified; homepage and software page already mention APIs, databases, webhooks and integrations.

**Status: HOLD as standalone page; EXPAND within software now.**

A future dedicated URL requires measured commercial demand, distinct SERP intent and proof of integration projects/use cases.

### I. Website-Checks / SEO / GEO / Performance

Homepage social metadata currently references website checks and digital obligations, but visible/search positioning primarily sells software, web and AI automation.

**Status: BLOCK until Business Truth is resolved.**

If this is an actual sellable DatenpflegeNord service, it needs its own evidence, scope, conversion path and keyword analysis. If it is stale social copy, remove the mismatch instead of inventing an SEO service architecture around it.

## 5. Authority implications from current SERPs

SE Ranking backlink evidence shows a material authority gap:

- DatenpflegeNord: 0 referring domains;
- Software-and-Testing: 37;
- EXORD: 127;
- HANSOLU: 374;
- Netzhirsch: 458.

Raw backlink counts for established web agencies are often inflated by sitewide footer/design-credit links, so referring-domain quality and relevance are the planning metric, not raw link count.

For local web SERPs, review-rich and local/entity-heavy competitors are common. Therefore external entity proof, legitimate reviews/citations and relevant referring domains are a core growth requirement, not an optional off-page afterthought.

## 6. Explicitly prohibited page patterns

Do not create:

- one near-identical page per Lübeck suburb/town merely to capture location modifiers;
- separate pages for `Softwareentwicklung Lübeck` and `Individualsoftware Lübeck` without distinct intent evidence;
- separate `KI Automatisierung`, `KI Agentur`, `KI Automatisierungs Agentur`, `KI für Unternehmen` pages for lexical variants;
- thin n8n, Make, Zapier, Claude, Codex or OpenAI pages merely because a tool is mentioned;
- city pages outside the verified service area without actual service truth and distinct local value;
- FAQ pages detached from the commercial page just to manufacture indexable URLs;
- customer/case-study pages without verified relationship and publication rights.

## 7. Current architecture target

### Core commercial layer

`/`

→ `/softwareentwicklung-luebeck/`

→ `/webentwicklung-luebeck/`

→ `/ki-automatisierung-luebeck/`

This remains the approved production architecture while the candidate gates are unresolved.

### Next likely expansion order, if gates pass

1. strengthen and deploy the three existing commercial pages;
2. establish indexing/query baseline in Google Search Console;
3. build legitimate authority/entity signals and measure referring-domain growth;
4. verify n8n as an explicit sellable service and then evaluate it as the first specialist child page;
5. decide whether broad/national AI automation belongs to the real service area;
6. evaluate AI-agent intent separately;
7. only then evaluate API/integration and additional web-intent pages.

## 8. Content gap requirements for existing commercial pages

Before new URLs multiply, each core page should be able to answer:

- what exact business problem does this solve?
- for whom is it appropriate/not appropriate?
- what concrete deliverables can be produced?
- which systems/data sources can be connected?
- what is the implementation sequence?
- how is the result tested/verified?
- what proof can be shown without exaggeration?
- what happens after launch/handover?
- what are the real decision questions/FAQs?
- what is the next conversion step?

No fabricated prices, project counts, turnaround promises, ROI percentages, certifications, hosting locations or customer names.

## 9. Measurement loop after launch

For every approved target URL, track at minimum:

- indexed/canonical status;
- query impressions and clicks;
- CTR;
- average position by query cluster;
- non-brand vs brand visibility;
- landing-page conversions/contact submissions;
- cannibalization between URLs;
- CWV/UX regression;
- backlink/referring-domain evidence where relevant;
- AI/LLM brand and link presence where evidence is available.

Search Console is the primary first-party ranking/query source. SE Ranking and other third-party tools are prioritization, SERP and competitive evidence, not substitutes for actual site query data.
