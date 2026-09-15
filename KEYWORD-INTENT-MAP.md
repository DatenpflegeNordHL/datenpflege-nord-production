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

## 2. Current URL ownership

| URL | Primary intent owner | Supporting intents | Status | Action |
|---|---|---|---|---|
| `/` | DatenpflegeNord brand + service overview | Software, web, AI/automation, systems/integrations, Lübeck/SH | OWN | Keep as brand/entity/conversion hub; reconcile OG/social message with actual offer |
| `/softwareentwicklung-luebeck/` | software development Lübeck | individual software, web apps, internal tools, APIs, integrations, modernization | OWN + EXPAND | Protect local commercial target; do not split synonyms yet |
| `/webentwicklung-luebeck/` | web development / business websites Lübeck | website creation, landing pages, relaunch, technical web improvement | OWN + EXPAND | Test/retarget language toward commercial “Website erstellen lassen” intent before creating another local web URL |
| `/ki-automatisierung-luebeck/` | AI automation Lübeck | AI agents, n8n, LLM/API workflows, process automation | OWN + EXPAND | Keep local owner; strengthen use cases/process/proof before splitting children |
| `/en/` | English brand/service overview | English discovery | OWN | Keep only while maintained as a deliberate English experience |
| `/impressum/` | legal provider identity | company/register/contact | OWN | Legal truth only; no SEO expansion |
| `/datenschutz/` | privacy information | contact-system processing | OWN | Legal/privacy truth only; no SEO expansion |

## 3. High-priority candidate intents

### A. `KI Automatisierung` — national/non-local hub

Measured signal: ~1,600 searches/month in the checked German dataset; difficulty around mid-30s.

**Status: HOLD.**

Why it is attractive:

- materially larger demand than the exact local AI query;
- current national SERPs are commercially meaningful;
- current service truth already includes agents, n8n, LLM and API workflows.

Blockers before `/ki-automatisierung/` may exist:

- current Organization/service-area truth is Lübeck + Schleswig-Holstein;
- need explicit business decision/evidence that projects are accepted nationally/remotely;
- must compare SERP/query overlap with `/ki-automatisierung-luebeck/`;
- need enough proof/use cases to avoid a generic national agency page.

If approved later: national hub owns broad `KI Automatisierung`, local page owns location-modified Lübeck/SH intent and links canonically/internal semantically to the hub without duplicating copy.

### B. `n8n Automatisierung`

Measured signal: ~110 searches/month, difficulty ~10, commercially relevant CPC.

**Status: HOLD — strongest specialist child candidate.**

Do not create yet because n8n is already covered by the AI page and may be an implementation technology rather than a standalone customer outcome. Separate URL only if current SERPs/query data show distinct tool-specific procurement intent and DatenpflegeNord wants to sell n8n implementation as a named service.

Until then, `/ki-automatisierung-luebeck/` owns local n8n intent as a section.

### C. `KI Agenten für Unternehmen`

Measured exact-ish demand in the first pass is low (~20/month for `ki agenten unternehmen`) but current SERPs clearly support a distinct commercial concept.

**Status: HOLD.**

Start as a substantial section/use-case cluster under AI automation. Promote to its own URL only if Search Console, broader keyword metrics and SERP overlap show independent demand and the page can contain concrete permissions, tools, human-in-the-loop/governance, integrations and real use cases.

### D. `Website erstellen lassen Lübeck`

Autocomplete and current SERPs show strong local commercial wording. Competitors use the phrase directly and lead with deliverable, process, proof and CTA rather than the developer-centric term `Webentwicklung`.

**Status: EXPAND existing `/webentwicklung-luebeck/`, not a new page.**

First change the current page's semantic coverage after final metric/overlap verification. Only create a second URL if both query sets demonstrably resolve to different SERP/user journeys. Default assumption is that they belong to the same commercial page.

### E. Individualsoftware

Business fit is strong and it is already semantically covered by `/softwareentwicklung-luebeck/`.

**Status: EXPAND existing page.**

Do not create `/individualsoftware-luebeck/` as a lexical duplicate. Reconsider only when measured data and SERP overlap support a separate procurement journey.

### F. API / Schnittstellen / Systemintegration

Business fit is verified; homepage and software page already mention APIs, databases, webhooks and integrations.

**Status: HOLD as standalone page; EXPAND within software now.**

A future dedicated URL requires measured commercial demand and proof of distinct integration projects/use cases.

### G. Website-Checks / SEO / GEO / Performance

Homepage social metadata currently references website checks and digital obligations, but visible/search positioning primarily sells software, web and AI automation.

**Status: BLOCK until Business Truth is resolved.**

If this is an actual sellable DatenpflegeNord service, it needs its own evidence, scope, conversion path and keyword analysis. If it is stale social copy, remove the mismatch instead of inventing an SEO service architecture around it.

## 4. Explicitly prohibited page patterns

Do not create:

- one near-identical page per Lübeck suburb/town merely to capture location modifiers;
- separate pages for `Softwareentwicklung Lübeck` and `Individualsoftware Lübeck` without distinct intent evidence;
- separate `KI Automatisierung`, `KI Agentur`, `KI Automatisierungs Agentur`, `KI für Unternehmen` pages for lexical variants;
- thin n8n, Make, Zapier, Claude, Codex or OpenAI pages merely because a tool is mentioned;
- city pages outside the verified service area without actual service truth and distinct local value;
- FAQ pages detached from the commercial page just to manufacture indexable URLs;
- customer/case-study pages without verified relationship and publication rights.

## 5. Current architecture target

### Core commercial layer

`/`

→ `/softwareentwicklung-luebeck/`

→ `/webentwicklung-luebeck/`

→ `/ki-automatisierung-luebeck/`

This remains the approved production architecture while the candidate gates are unresolved.

### Next likely expansion order, if gates pass

1. strengthen the three existing commercial pages;
2. decide whether broad/national AI automation belongs to the real service area;
3. evaluate n8n as the first specialist child page;
4. evaluate AI-agent intent separately;
5. only then evaluate API/integration and additional web-intent pages.

## 6. Content gap requirements for existing commercial pages

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

## 7. Measurement loop after launch

For every approved target URL, track at minimum:

- indexed/canonical status;
- query impressions and clicks;
- CTR;
- average position by query cluster;
- non-brand vs brand visibility;
- landing-page conversions/contact submissions;
- cannibalization between URLs;
- CWV/UX regression;
- backlink/referring-domain evidence where relevant.

Search Console is the primary first-party ranking/query source. Third-party volume is prioritization evidence, not a substitute for actual site query data.
