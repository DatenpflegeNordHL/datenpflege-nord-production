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

Keyword metrics are third-party estimates, not ground truth. Current evidence combines Ubersuggest, SE Ranking and direct current Google SERP snapshots. Where providers disagree, the disagreement is retained rather than averaged into fake precision.

Google Search Console remains the first-party tie-breaker for actual impressions, clicks, CTR, ranking URLs and cannibalization once connected.

Current SE Ranking pre-deployment baseline (Germany, 2026-09-10):

- `datenpflege-nord.de` returned no organic keyword rows in the SE Ranking domain database;
- a manual Google Germany rank-tracking project was created with audits disabled and manual checking only;
- the first tracked priority-query set is outside the tracked Google top 100;
- backlink baseline: 0 backlinks / 0 referring domains / Domain InLink Rank 0;
- AI Search baseline across AI Overview, AI Mode, ChatGPT, Perplexity and Gemini: Brand Presence 0, Link Presence 0, Share of Voice 0;
- SE Ranking does not currently resolve a stored AI-search brand entity for the domain; an explicit `DatenpflegeNord` brand query likewise returns no measurable presence;
- Google Search Console is not connected to the SE Ranking project yet.

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

## 4. Exact SE Ranking batch metrics

Germany database, batch checked 2026-09-10. These values are the preferred SE Ranking comparison set because all tracked keywords were measured in one endpoint and one snapshot.

| Query | Volume/mo | KD | CPC | Intent | Current URL decision |
|---|---:|---:|---:|---|---|
| `individuelle softwareentwicklung` | 320 | 12 | €13.67 | Local + Commercial | EXPAND software page |
| `softwareentwicklung agentur` | 140 | 30 | €9.11 | Local + Commercial | Supporting intent on software page |
| `ki automatisierung agentur` | 140 | 17 | €6.10 | Informational in provider classifier | HOLD within AI cluster; commercial SERP evidence still required |
| `softwareentwicklung lübeck` | 110 | 34 | €0.62 | Local + Commercial | OWN software page |
| `softwareentwicklung dienstleister` | 110 | 39 | €15.14 | Local + Commercial | Supporting procurement intent on software page |
| `n8n automatisierung` | 110 | 16 | €1.73 | Informational in provider classifier | HOLD specialist child candidate |
| `webentwicklung lübeck` | 40 | 52 | €2.11 | Local + Commercial | OWN web page |
| `ki agenten unternehmen` | 20 | 15 | €3.81 | Informational | HOLD / section first |
| `website erstellen lassen lübeck` | 10 | 45 | €0 | Local + Commercial | EXPAND existing web page |
| `ki automatisierung lübeck` | no data | no data | no data | no data | Keep local business owner; no volume-driven expansion claim |

Notable trend evidence from the same batch:

- `n8n automatisierung` rose from roughly 20/month in late 2025 to 110/month in the latest 2026 snapshot;
- `individuelle softwareentwicklung` remained materially larger than the exact Lübeck software query, despite easing from earlier 480/month readings to 320/month;
- `website erstellen lassen lübeck` stayed around 10/month across the returned twelve-month history.

Do not treat trend estimates as first-party traffic forecasts.

## 5. High-priority candidate intents

### A. `Softwareentwicklung Lübeck`

SE Ranking exact/local evidence on 2026-09-10:

- estimated DE volume: 110/month;
- KD: 34;
- intent: Local + Commercial;
- city-level Lübeck SERP is mixed: many job/study results, but genuine development providers also rank prominently;
- EXORD appears in both the local pack / local-result layer and organic results for the query;
- DatenpflegeNord was not present in the returned city-level snapshot and the tracked rank was outside top 100.

**Status: OWN `/softwareentwicklung-luebeck/` + EXPAND.**

The query is worth defending, but not every estimated search is a buyer. The page should make service/procurement intent unmistakable through deliverables, process, integration capability, decision criteria and proof.

### B. `Individualsoftware` / `individuelle Softwareentwicklung`

SE Ranking batch evidence:

- estimated DE volume: 320/month;
- KD: 12;
- CPC: €13.67;
- Local + Commercial classifier;
- strong business fit with the existing software offer.

**Status: EXPAND existing `/softwareentwicklung-luebeck/`.**

Do not create `/individualsoftware-luebeck/` as a lexical duplicate. The existing software page already owns the buyer journey and should absorb this terminology naturally.

Supporting commercial software phrases reinforce the same owner:

- `softwareentwicklung agentur`: 140/month, KD 30, CPC €9.11;
- `softwareentwicklung dienstleister`: 110/month, KD 39, CPC €15.14.

These are supporting procurement terms, not automatic new URLs.

### C. `Webentwicklung Lübeck` / Webdesign / Website creation

SE Ranking exact/local evidence:

- `webentwicklung lübeck`: 40/month, KD 52, CPC €2.11, Local + Commercial;
- earlier Ubersuggest data estimated a somewhat higher volume; retain this as cross-provider variance, not a contradiction to be averaged away;
- city-level Google SERP strongly blends Webentwicklung, Webdesign, Website-Erstellung and agency intent;
- review-rich/local-business style competitors are common;
- DatenpflegeNord was not present in the returned city-level snapshot and tracked outside top 100.

**Status: OWN + EXPAND existing `/webentwicklung-luebeck/`.**

Proof, reviews, local/entity authority, service clarity and conversion value are more important here than multiplying near-identical pages.

### D. `Website erstellen lassen Lübeck`

SE Ranking exact/local evidence:

- estimated DE volume: 10/month;
- KD: 45;
- Local + Commercial;
- twelve-month trend is essentially flat at ~10/month;
- city-level SERP is much thinner and noisier than `webentwicklung lübeck`, with ads and several irrelevant/weak organic results;
- the query overlaps the same website-procurement journey.

**Status: EXPAND existing `/webentwicklung-luebeck/`, not a new page.**

This now has stronger evidence than the earlier autocomplete-only decision. A separate `/website-erstellen-lassen-luebeck/` would create unnecessary cannibalization risk for a small exact local query.

### E. `KI Automatisierung` — national/non-local hub

Earlier Ubersuggest evidence showed materially larger broad demand for `KI Automatisierung`, while SE Ranking's related-query set shows broad terms are often informational and commercially ambiguous.

SE Ranking exact batch evidence for the procurement-adjacent phrase:

- `ki automatisierung agentur`: 140/month;
- KD: 17;
- CPC: €6.10;
- provider classifier labels the phrase informational, so commercial intent must be established from the SERP rather than assumed from wording alone.

**Status: HOLD.**

Why it remains attractive:

- current service truth includes agents, n8n, LLM and API workflows;
- national AI-automation SERPs contain service providers;
- broader demand is materially larger than the exact local AI phrase.

Blockers before `/ki-automatisierung/` may exist:

- current Organization/service-area truth is Lübeck + Schleswig-Holstein;
- need explicit business decision/evidence that projects are accepted nationally/remotely;
- must compare Search Console/real-query overlap with `/ki-automatisierung-luebeck/` after indexing;
- need enough proof/use cases to avoid a generic national agency page.

If approved later: national hub owns broad national procurement intent, while the local page owns location-modified Lübeck/SH intent without duplicating copy.

### F. `n8n Automatisierung`

SE Ranking exact batch + tracked SERP evidence:

- estimated DE volume: 110/month;
- KD: 16;
- CPC: €1.73;
- provider classifier: Informational;
- estimated search demand rose substantially across the returned twelve-month history;
- first tracked position for DatenpflegeNord: outside top 100 on 2026-09-10;
- current German top-30 SERP is mixed informational + commercial;
- high-authority information/vendor results include IONOS and n8n itself;
- commercial/service pages also rank, including `n8n-agentur.de` at position 6 and TEAM23 at position 10 in the tracked snapshot.

**Status: HOLD — strongest specialist child candidate.**

The SERP-distinction gate now passes materially better than in the first audit: Google accepts both education and procurement/service pages for this query. The remaining blockers are Business Truth and proof. DatenpflegeNord must explicitly sell n8n implementation as a named standalone service, and the page must contain real integration/process substance rather than generic tool copy.

Until then, `/ki-automatisierung-luebeck/` owns n8n intent as a substantial section.

### G. `KI Agenten für Unternehmen`

SE Ranking batch evidence for `ki agenten unternehmen`:

- 20/month;
- KD 15;
- CPC €3.81;
- provider classifier: Informational;
- demand is small and volatile compared with the software/n8n clusters.

**Status: HOLD.**

Start as a substantial decision/use-case cluster under AI automation. Promote to its own URL only if Search Console, expanded keyword evidence and SERP overlap show independent demand and the page can contain concrete implementation proof around permissions, integrations, human approval and governance.

### H. API / Schnittstellen / Systemintegration

Business fit is verified; homepage and software page already mention APIs, databases, webhooks and integrations.

**Status: HOLD as standalone page; EXPAND within software now.**

A future dedicated URL requires measured commercial demand, distinct SERP intent and proof of integration projects/use cases.

### I. Website-Checks / SEO / GEO / Performance

Homepage social metadata currently references website checks and digital obligations, but visible/search positioning primarily sells software, web and AI automation.

**Status: BLOCK until Business Truth is resolved.**

If this is an actual sellable DatenpflegeNord service, it needs its own evidence, scope, conversion path and keyword analysis. If it is stale social copy, remove the mismatch instead of inventing an SEO service architecture around it.

## 6. Authority and AI-search implications

SE Ranking backlink evidence shows a material authority gap:

- DatenpflegeNord: 0 referring domains;
- EXORD: 127;
- HANSOLU: 374;
- ISEO: 396;
- Netzhirsch: 458.

Raw backlink counts for established web agencies can be inflated by sitewide footer/design-credit links. Referring-domain quality, editorial relevance and local/entity value are therefore the planning metrics, not raw backlink count.

AI-search comparison in the SE Ranking German database across Google AI Overview, Google AI Mode, ChatGPT, Perplexity and Gemini:

| Brand | AI brand presence | AI link presence | Share of voice |
|---|---:|---:|---:|
| Netzhirsch | 39 | 92 | 61.20% |
| ISEO | 32 | 23 | 30.33% |
| HANSOLU | 1 | 15 | 6.36% |
| EXORD | 2 | 2 | 2.11% |
| DatenpflegeNord | 0 | 0 | 0% |

In this comparison, measurable competitor presence came from **Google AI Overview**; the same comparison returned zero for all five brands in ChatGPT, Perplexity, Gemini and Google AI Mode.

Netzhirsch's AI Overview-specific snapshot reported brand presence 39, link presence 92, AI opportunity traffic 26 and average position 10.82.

Implication: DatenpflegeNord's current problem is not an isolated missing AI tag or schema trick. It lacks the broader authority/entity/content footprint that already allows some competitors to be cited in Google's AI layer.

## 7. Competitor keyword evidence

EXORD currently ranks for the exact local software cluster, including `softwareentwicklung lübeck` and `softwareentwickler lübeck`; the returned SE Ranking data shows top local/organic visibility for the homepage. This demonstrates that a dedicated lexical child URL is not required to compete for the core local software intent.

Netzhirsch distributes web visibility across a commercial webdesign-agency page and supporting knowledge content. Its ranking portfolio includes broad terms such as `webdesign agentur`, `webagentur`, `webentwicklung agentur` and `professionelles webdesign`.

Implication: our next gains should come from stronger service-page substance, evidence and authority rather than multiplying location/keyword variants.

## 8. Explicitly prohibited page patterns

Do not create:

- one near-identical page per Lübeck suburb/town merely to capture location modifiers;
- separate pages for `Softwareentwicklung Lübeck` and `Individualsoftware Lübeck` without distinct intent evidence;
- separate `KI Automatisierung`, `KI Agentur`, `KI Automatisierungs Agentur`, `KI für Unternehmen` pages for lexical variants;
- thin n8n, Make, Zapier, Claude, Codex or OpenAI pages merely because a tool is mentioned;
- city pages outside the verified service area without actual service truth and distinct local value;
- FAQ pages detached from the commercial page just to manufacture indexable URLs;
- customer/case-study pages without verified relationship and publication rights.

## 9. Current architecture target

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

## 10. Content gap requirements for existing commercial pages

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

## 11. Measurement loop after launch

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
