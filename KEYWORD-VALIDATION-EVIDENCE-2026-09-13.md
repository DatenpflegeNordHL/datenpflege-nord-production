# KEYWORD VALIDATION EVIDENCE — 2026-09-13

Status: preliminary validation wave while the Codex-generated 570/150 keyword files remain local and are not yet committed to GitHub.

This file records only keywords already known from the Golden research/watchlist. It must not be treated as a substitute for the exact `KEYWORD-VALIDATION-QUEUE.md` until that file is committed.

## Method

Source: SE Ranking DE keyword metrics + direct current Google DE SERP snapshots through SE Ranking.

First batch: 60 known high-priority/watchlist terms across Lübeck, Kiel, Hamburg, Schleswig-Holstein, n8n, API and Schnittstellen.

Result: 33 keywords returned quantitative data; 27 returned no reliable keyword row. No-data does not equal zero demand.

## Strongest measured regional web terms

| Keyword | Volume | KD | CPC | Provider intent | Current interpretation |
|---|---:|---:|---:|---|---|
| webdesign lübeck | 390 | 55 | 2.96 | Local + Commercial | Strong existing-owner expansion term |
| webdesigner lübeck | 390 | 0 reported | 2.96 | Informational label | Tool intent label conflicts with local SERP evidence; use as same Lübeck web cluster |
| webagentur lübeck | 320 | 55 | 1.29 | Local + Commercial | Strong procurement/supporting term |
| webdesign kiel | 390 | 32 | 2.30 | Local + Commercial | Strong regional build candidate, uniqueness gate still required |
| webdesigner kiel | 390 | 12 | 2.30 | Local + Commercial | Strong supporting Kiel procurement term |
| webagentur kiel | 320 | 0 reported | 1.05 | Informational label | Requires SERP interpretation; lexical demand is strong |
| website erstellen lassen hamburg | 260 | 37 | 4.91 | Local + Commercial | Strong buyer intent, high-competition market |
| webagentur hamburg | 160 | 52 | 1.93 | Local + Commercial | Strong supporting Hamburg procurement term |
| webentwicklung hamburg | 140 | 44 | 2.92 | Local + Commercial | Strong supporting Hamburg term |
| webdesigner schleswig-holstein | 170 | 27 | 1.52 | Local + Commercial | Strong statewide signal |
| webdesign schleswig-holstein | 110 | 28 | 2.92 | Local + Commercial | Strong statewide signal |
| webentwicklung lübeck | 40 | 52 | 2.11 | Local + Commercial | Lower demand than Webdesign; more job/career contamination |
| webentwicklung kiel | 30 | 20 | 0 | Local + Commercial | Supporting term |
| website erstellen lassen lübeck | 10 | 45 | 0 | Local + Commercial | Same buyer journey, not separate page by itself |
| webdesign hamburg | 10 | 66 | 2.98 | Local + Commercial | Exact phrase surprisingly weak versus other Hamburg web phrases |
| webdesigner hamburg | 10 | 59 | 2.98 | Local + Commercial | Same observation |

## Strongest measured software terms

| Keyword | Volume | KD | CPC | Intent | Current interpretation |
|---|---:|---:|---:|---|---|
| softwareentwicklung lübeck | 110 | 34 | 0.62 | Local + Commercial | Existing owner valid; SERP job/study contamination |
| softwareentwickler lübeck | 110 | 15 | 0.62 | Local + Commercial | Same owner, easier supporting term |
| softwareentwicklung kiel | 90 | 22 | 0.77 | Local + Commercial | Numerically attractive but city SERP is heavily job-dominated |
| softwareentwickler kiel | 90 | 12 | 0.77 | Local + Commercial | Same contamination problem |
| softwareentwicklung hamburg | 110 | 39 | 6.33 | Local + Commercial | Strong commercial value; harder market |
| softwareentwickler hamburg | 140 | 50 | 1.30 | Local + Commercial | Strong demand, high competition and possible job contamination |
| software agentur hamburg | 20 | 48 | 4.42 | Local + Commercial | Lower-volume direct procurement modifier |
| individualsoftware hamburg | 10 | 17 | 0 | Informational label | Supporting terminology; not standalone evidence |

No reliable SE Ranking row in this batch for exact `individualsoftware lübeck`, `individualsoftware kiel`, most Schleswig-Holstein software modifiers, or software-agentur variants outside Hamburg.

## AI / automation regional signals

| Keyword | Volume | KD | CPC | Intent | Current interpretation |
|---|---:|---:|---:|---|---|
| ki beratung hamburg | 70 | 9 | 3.45 | Local + Commercial | Very strong Hamburg candidate; service-area/unique-value gate remains |
| ki agentur hamburg | 70 | 12 | 4.17 | Local + Commercial | Very strong Hamburg candidate |

Exact Lübeck/Kiel/Schleswig-Holstein KI modifiers and regional Prozessautomatisierung modifiers returned no reliable rows in this batch. They remain evidence-pending, not rejected.

## n8n signals

| Keyword | Volume | KD | CPC | Intent label | Interpretation |
|---|---:|---:|---:|---|---|
| n8n automatisierung | 110 | 16 | 1.73 | Informational | Strong topical/commercial-support signal |
| n8n agentur | 90 | 5 | 2.94 | Informational | Tool intent label is too broad; prior SERP evidence shows dedicated provider pages in the upper SERP, so standalone commercial child remains a strong candidate |
| n8n beratung | 0 | 5 | 0 | Informational | Do not prioritize by itself |
| n8n für unternehmen | no reliable row | — | — | — | Keep as semantic/supporting candidate only |

## API / Schnittstellen signals

| Keyword | Volume | KD | CPC | Intent label | SERP interpretation |
|---|---:|---:|---:|---|---|
| api integration | 390 | 0 reported | 2.13 | Informational | SERP is overwhelmingly explanatory/knowledge content; GUIDE/AUTHORITY candidate, not primary money page |
| api entwicklung | 110 | 16 | 2.21 | Informational | Needs separate commerciality check before page decision |
| schnittstellenentwicklung | 110 | 6 | 3.72 | Informational | SERP strongly mixed toward real commercial service pages; high-value niche candidate |
| schnittstellenprogrammierung | 70 | 6 | 2.70 | Informational | Strong adjacent niche/supporting term; likely same commercial cluster pending overlap check |

### Direct SERP gate: `api integration`

Top results are dominated by explanatory/authority pages from SAP, IBM, OpenText, ServiceNow, Cleo, Jitterbit, Zapier, Red Hat, MuleSoft and Postman. The user intent is primarily informational/educational.

Decision: **GUIDE / AUTHORITY**, not a standalone commercial service owner based on this phrase alone.

### Direct SERP gate: `schnittstellenentwicklung`

Top results are dominated by actual service pages from providers such as AllBytes, PTC Solutions, Stein Entwicklung, LIMESODA, Sinusquadrat, TenMedia, Groenewold, Intercorp, Cixon, age up, Datenzeugs, DRIVE and others, alongside a smaller number of glossaries/educational results.

SERP features include **AI Overview** and People Also Ask.

Decision: **STRONG NICHE / COMMERCIAL CLUSTER CANDIDATE**. This keyword materially outperforms the generic `api integration` phrase for DatenpflegeNord's actual business fit.

Potential positioning to validate further:
- Schnittstellenentwicklung
- API- & Schnittstellenentwicklung
- Systeme verbinden / Systemintegration
- Schnittstelle entwickeln lassen
- API-Schnittstellen für Unternehmen

Do not rename a product category yet. First validate neighboring terms, SERP overlap, regional modifiers and proof depth.

## Current first-wave priority changes

1. **Schnittstellenentwicklung moves up** into the top niche-validation tier because of 110 volume, KD 6, strong business fit and commercial SERP composition.
2. **API Integration moves down** as a money keyword despite 390 volume; it is primarily authority/content intent.
3. **Kiel Web remains one of the strongest regional acquisition opportunities.**
4. **Hamburg KI remains a strong regional opportunity** with unusually low KD relative to commercial intent.
5. **Kiel Software remains lower priority than Kiel Web** because raw volume is heavily diluted by jobs.
6. **Statewide Schleswig-Holstein Web remains meaningful**, especially Webdesigner/Webdesign, but statewide page ownership still requires overlap/uniqueness proof.

## Data gaps / next steps

1. Commit the exact Codex research files to GitHub:
   - `KEYWORD-UNIVERSE-RAW.csv`
   - `KEYWORD-CLUSTERS.md`
   - `NICHE-OPPORTUNITIES.md`
   - `KEYWORD-VALIDATION-QUEUE.md`
2. Replace this provisional watchlist with the exact P0/P1 queue once committed.
3. Validate `api entwicklung`, `schnittstellenprogrammierung`, `schnittstelle entwickeln lassen`, `systemintegration`, `systeme verbinden`, and regional interface/API modifiers.
4. Run full metrics on the exact P0 60 from Codex.
5. Run targeted SERP checks only for terms whose metrics + business fit justify the cost.
6. Connect GSC for first-party impressions/CTR/query evidence when available.

Golden rule remains:

`Business Truth → Keyword Metrics → SERP Reality → Regional/Niche Fit → Cluster Ownership → BUILD / EXPAND / HOLD / REJECT`
