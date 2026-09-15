# Internal link architecture

Updated 2026-09-15. Seven canonical pages; no new commercial/content URLs approved.
All paths resolve under `https://datenpflege-nord.de/`.

```mermaid
graph TD
  H[Homepage] --> S[Software Lübeck]
  H --> W[Web Lübeck]
  H --> A[KI / Automatisierung Lübeck]
  H <--> E[English overview]
  S <--> W
  S <--> A
  W <--> A
  S --> C[Homepage contact]
  W --> C
  A --> C
  H --> I[Impressum]
  H --> D[Datenschutz]
```

## Actual Phase 1–3 edges

| Source | Destination | Purpose / natural anchor |
|---|---|---|
| `/` | S, W, A | Service-detail links; one click from homepage |
| `/` | `/softwareentwicklung-luebeck/#schnittstellen` | Homepage systems/interfaces card assigns API and interface intent explicitly to S |
| S | `#entscheidung`, `#schnittstellen`, `#projektstart` | Local decision navigation: Standard oder individuell; APIs und Schnittstellen; Projekt vorbereiten |
| W | `#entscheidung`, `#projektstart` | Website-Entscheidung and project preparation |
| A | `#entscheidung`, `#projektstart` | Workflow choice and process inputs |
| W | `/softwareentwicklung-luebeck/#entscheidung` | Web application with business logic belongs to Software |
| W | `/softwareentwicklung-luebeck/#schnittstellen` | API/Schnittstellen planning for website integration |
| A | `/softwareentwicklung-luebeck/#schnittstellen` | API access and data connections, avoiding duplicate tutorial |
| S | `/ki-automatisierung-luebeck/#entscheidung` | Multistep workflow/approval choice beyond the interface |
| Each core owner | Other two core owners | Existing related-service cards |
| Each core owner | `/#kontakt` | Existing next-action CTA; linked input checklist improves inquiry context |
| `/en/` | `/` | The English overview links back to the German homepage; it does **not** directly link to S, W or A. Service discovery from `/en/` is therefore `/en/` → `/` → S/W/A. |
| All pages | Legal pages / home | Provider identity, privacy and return path |

Fragments are not sitemap URLs or new canonical owners. Links must be present in initial HTML, readable without JavaScript and resolve to unique IDs. No links to HOLD candidates, no repeated exact-keyword anchor blocks or city lists.

## Supporting and regional architecture after future gates

Each new decision asset must receive a contextual link from its commercial owner and link back with a task-specific anchor. A future API owner requires a deliberate update to S/W/A and this graph. A passing Kiel page would link to W where the broader service explanation helps and have its own truthful conversion reason; a redirecting city funnel or duplicated service page is unacceptable. Hamburg remains HOLD on area truth.

## Validation

`python3 scripts/site_audit.py` checks internal targets/fragments. `python3 scripts/golden_audit.py` traverses HTML links from home and fails on orphan canonical pages; mere sitemap membership does not count as reachability. Record actual final graph findings in GOLDEN-VALIDATION-REPORT. No Phase-4 standalone content exists to orphan in this scope.
