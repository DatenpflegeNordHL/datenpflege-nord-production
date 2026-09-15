# KEYWORD P0 VALIDATION — DatenpflegeNord

Status: exact P0 validation in progress
Last checked: 2026-09-13
Research source: `main@e72e01be18a3c8ad1ed43660ef8cb88f0a981bfa`
Queue source: `research/datenpflege-nord/KEYWORD-VALIDATION-QUEUE.md`
Scope: exact P0 set of 60 keywords

This file records quantitative and SERP validation of the exact Codex P0 queue. It is evidence for clustering and URL ownership. It is not permission to build or publish a page.

## 1. Exact P0 quantitative pass

All 60 P0 keywords from the queue were submitted in one SE Ranking DE metrics batch.

Result:
- 60 exact P0 keywords checked;
- 13 returned a direct quantitative row;
- 47 returned no reliable exact row;
- `no data` is not interpreted as zero demand. Many P0 terms are highly specific city + BOFU combinations and must be evaluated through parent demand, SERP intent and business fit.

### P0 keywords with direct metric rows

| Keyword | Volume | KD | CPC EUR | Provider intent | Current interpretation |
|---|---:|---:|---:|---|---|
| webdesign lübeck | 390 | 55 | 2.96 | Local + Commercial | Existing Lübeck Web owner: EXPAND |
| webdesigner lübeck | 390 | 0 reported | 2.96 | Informational label | Tool label conflicts with known commercial city SERP; same Lübeck Web cluster |
| webdesign kiel | 390 | 32 | 2.30 | Local + Commercial | Strong regional acquisition candidate |
| webdesigner kiel | 390 | 12 | 2.30 | Local + Commercial | Strong Kiel supporting/procurement term |
| webagentur lübeck | 320 | 55 | 1.29 | Local + Commercial | Same existing Lübeck Web owner |
| webagentur kiel | 320 | 0 reported | 1.05 | Informational label | Tool label conflicts with known commercial Kiel Web SERP; same Kiel cluster |
| webagentur hamburg | 160 | 52 | 1.93 | Local + Commercial | Valuable Hamburg Web term; service-area gate remains |
| softwareentwicklung lübeck | 110 | 34 | 0.62 | Local + Commercial | Existing owner valid; known job/study contamination |
| softwareentwicklung hamburg | 110 | 39 | 6.33 | Local + Commercial | Valuable but harder Hamburg market; service-area gate remains |
| softwareentwicklung kiel | 90 | 22 | 0.77 | Local + Commercial | Known city SERP is heavily job-dominated; lower acquisition priority |
| individualsoftware hamburg | 10 | 17 | 0.00 | Informational label | Supporting signal only; parent/BOFU terms matter more |
| webdesign hamburg | 10 | 66 | 2.98 | Local + Commercial | Exact phrase unexpectedly weak vs other Hamburg Web formulations |
| webdesigner hamburg | 10 | 59 | 2.98 | Local + Commercial | Exact phrase unexpectedly weak vs other Hamburg Web formulations |

### Exact P0 terms with no reliable keyword row

The no-data group includes the regional API/Schnittstellen terms, most KI/automation terms, regional process/workflow terms, most Individualsoftware longtails, internal-tools/software phrases, Landingpage city variants, Systemintegration city variants, and several transactional `entwickeln lassen` / `programmieren lassen` phrases.

Decision rule: do not reject these terms because the provider database has no row. Validate the parent phrase and the city/service SERP, then cluster the exact longtail under the correct owner when intent is aligned.

## 2. Parent-demand validation for P0 no-data families

| Parent keyword | Volume | KD | CPC EUR | Intent label | Current role |
|---|---:|---:|---:|---|---|
| systemintegration | 3600 | 93 | 1.11 | Informational | REJECT as primary acquisition owner; too broad/hard |
| ki automatisierung | 920 | 54 | 3.09 | Informational | Large authority/commercial-support topic; needs narrower BOFU owners |
| prozessautomatisierung | 540 | 0 reported | 3.48 | Informational | Authority/decision hub; not clean money owner |
| api integration | 390 | 0 reported | 2.13 | Informational | GUIDE/AUTHORITY, not primary service owner |
| workflow automatisierung | 320 | 0 reported | 4.01 | Informational | Strong thematic support; SERP gate still pending |
| landingpage erstellen lassen | 260 | 29 | 5.48 | Informational label | SERP is materially commercial; Web cluster opportunity |
| individualsoftware | 260 | 21 | 11.62 | Informational label | Mixed hub/commercial support |
| ki integration | 140 | 17 | 3.93 | Informational | Strong narrower AI candidate; SERP gate pending |
| schnittstellenentwicklung | 110 | 6 | 3.72 | Informational label | STRONG COMMERCIAL NICHE based on SERP reality |
| api entwicklung | 110 | 16 | 2.21 | Informational | Strong adjacent integration term; SERP task pending |
| unternehmenswebsite erstellen lassen | 90 | 37 | 13.31 | Informational label | High-value procurement candidate; SERP gate pending |
| schnittstellenprogrammierung | 70 | 6 | 2.70 | Informational | Strong adjacent Schnittstellen term |
| individualsoftware entwickeln lassen | 30 | 9 | 15.94 | Informational label | VERY STRONG BOFU software term based on commercial SERP |
| webanwendung entwickeln lassen | 20 | 14 | 13.57 | Informational label | High-intent longtail candidate; SERP gate pending |
| interne tools entwickeln lassen | 0 | 4 | 0 | Informational | Semantic/problem language only; not a primary target by itself |
| automatisierung für unternehmen | 0 | 14 | 0 | Informational | Semantic/support term only unless SERP evidence proves otherwise |

No reliable parent row was returned for `schnittstelle programmieren lassen`, `interne software entwickeln lassen`, or `api programmieren lassen`.

## 3. Direct SERP gates completed

### `api integration`

SERP is overwhelmingly explanatory and authority-led. Upper results include SAP, IBM, OpenText, ServiceNow, Cleo, Jitterbit, Zapier, Red Hat, MuleSoft and Postman.

Decision: **GUIDE / AUTHORITY**. The high 390 volume does not justify a standalone commercial owner.

### `schnittstellenentwicklung`

Upper SERP contains many actual service pages, including providers such as AllBytes, PTC Solutions, Stein Entwicklung, LIMESODA, Sinusquadrat, TenMedia, Groenewold, Intercorp, Cixon, age up, Datenzeugs and DRIVE, alongside a smaller informational layer.

SERP features include AI Overview and People Also Ask.

Decision: **STRONG NICHE / COMMERCIAL CLUSTER CANDIDATE**.

Current coherent family:
- `schnittstellenentwicklung`: 110 / KD 6;
- `schnittstellenprogrammierung`: 70 / KD 6;
- `api entwicklung`: 110 / KD 16;
- `api programmierung`: 140 / KD 30 (measured in adjacent validation);
- `api integration`: 390 but informational, useful as authority/supporting content;
- `systemintegration`: broad semantic support, not a primary owner.

Working positioning candidate: **API- & Schnittstellenentwicklung**. Do not rename or publish yet; owner overlap and proof depth still need validation.

### `prozessautomatisierung`

Despite 540 volume, the upper SERP is dominated by definitions, guides and authority content from Haufe Akademie, SAP, Lexware, Salesforce, Personio, IBM, Springer and related resources. Commercial providers appear, but the dominant intent is learning/decision support.

SERP features include AI Overview and People Also Ask.

Decision: **AUTHORITY / DECISION HUB**, not a clean standalone money keyword. It should support narrower implementation offers such as n8n, KI integration, workflows and API/Schnittstellen work.

### `individualsoftware`

The exact 260-volume SERP is mixed. Wikipedia, glossaries, comparisons and decision guides are prominent, while service pages and ads also occur throughout.

Decision: **HUB + COMMERCIAL SUPPORT**, not a pure money owner on exact-match evidence alone.

### `individualsoftware entwickeln lassen`

Metrics: 30 volume, KD 9, CPC 15.94 EUR.

The SERP is strongly procurement-oriented. Upper results include Bauer + Kirch, HEC, LISE, EXWE, Sinovo, Djangsters, Newcubator, Andersen, and numerous other software-development providers; ads are also present.

SERP features include AI Overview, People Also Ask, ads and reviews.

Decision: **VERY STRONG BOFU SOFTWARE TERM**. It should be incorporated into the software acquisition owner/cluster. A separate URL is not approved until overlap with `/softwareentwicklung-luebeck/`, `individuelle softwareentwicklung` and other buyer terms is quantified.

### `landingpage erstellen lassen`

Metrics: 260 volume, KD 29, CPC 5.48 EUR.

The upper SERP starts with multiple actual providers and service pages (e.g. Seiten-Werk, ucentric media, Kigoo) and remains materially commercial throughout, although builders/guides such as HubSpot, Wix and IONOS create a mixed layer.

Decision: **STRONG COMMERCIAL WEB SUBCLUSTER / EXPAND CANDIDATE**. Do not create a separate Landingpage URL solely from this result. First compare overlap against Webdesign, Website erstellen lassen and the existing Web owner.

## 4. First P0 decision matrix

| Cluster | Evidence status | Current decision |
|---|---|---|
| Lübeck Web | strong direct metrics + known commercial city SERP | **EXPAND existing owner** |
| Kiel Web | strong direct metrics + strongly commercial city SERP | **STRONG BUILD CANDIDATE / HOLD uniqueness gate** |
| Hamburg Web | measurable procurement terms, higher competition | **HOLD service-area + uniqueness** |
| Lübeck Software | measurable local demand + existing owner; job contamination | **EXPAND existing owner with stronger BOFU language** |
| Kiel Software | measurable demand but job-heavy city SERP | **HOLD / lower regional priority** |
| Hamburg Software | measurable demand + high CPC, harder market | **HOLD service-area + SERP/uniqueness** |
| Individualsoftware / entwickeln lassen | parent mixed; BOFU variant very strong | **EXPAND software acquisition cluster** |
| API Integration | high volume but informational SERP | **GUIDE / AUTHORITY** |
| API & Schnittstellenentwicklung | low/moderate volume, low KD, commercial SERP | **TOP NICHE CANDIDATE / HOLD owner-proof gate** |
| Systemintegration | huge volume, KD 93, broad informational intent | **REJECT as primary acquisition target** |
| Prozessautomatisierung | large informational/decision SERP | **AUTHORITY HUB / supporting content** |
| Landingpage erstellen lassen | commercially strong mixed SERP | **EXPAND Web cluster / overlap gate** |
| regional KI/automation exact longtails | many exact terms have no provider row | **EVIDENCE PENDING; use parent + city SERP, do not reject** |

## 5. Current priority changes after exact P0 validation

1. **API- & Schnittstellenentwicklung moves into the highest niche-validation tier.** It combines strong business fit, low KD and service-heavy SERPs better than broad Systemintegration/API Integration.
2. **Individualsoftware entwickeln lassen becomes a key BOFU software phrase** despite modest raw volume because CPC, KD and SERP procurement intent are unusually strong.
3. **Kiel Web remains the strongest new regional landing-page candidate.**
4. **Lübeck Web should be expanded around real market vocabulary** before creating lexical sibling pages.
5. **Process automation should be used as an authority/decision layer**, not treated as a clean sales keyword merely because volume is high.
6. **Landingpage creation is a meaningful Web subcluster**, but URL separation remains unproven.
7. **Exact city + longtail no-data terms must be clustered rather than discarded.**

## 6. Open P0 gates

Still to validate before P0 can be considered complete:
- `api entwicklung` direct SERP commerciality and overlap with Schnittstellenentwicklung;
- `schnittstellenprogrammierung` overlap with Schnittstellenentwicklung;
- `workflow automatisierung` SERP intent;
- `ki integration` SERP intent;
- `unternehmenswebsite erstellen lassen` SERP intent and Web overlap;
- `webanwendung entwickeln lassen` SERP intent and Software/Web ownership;
- exact city-family SERPs only where parent demand + business fit justify the cost;
- Hamburg publication/service-area truth;
- GSC first-party query/impression/CTR evidence after indexing.

Golden rule:

`Business Truth → Exact Queue → Parent Demand → SERP Reality → Regional Fit → Cluster Ownership → BUILD / EXPAND / HOLD / REJECT`
