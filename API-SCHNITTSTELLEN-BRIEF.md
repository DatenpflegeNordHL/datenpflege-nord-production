# API / Schnittstellen — conditional future page brief

2026-09-13. **Decision A: EXPAND `/softwareentwicklung-luebeck/#schnittstellen` and implement that expansion in Phase 2–3. Decision B: HOLD `/api-schnittstellenentwicklung/`.** This brief does not approve a standalone page build.

## Purpose, intent and distinctness

Potential independent commercial purpose: a buyer has two existing systems and needs a defined data exchange, rather than a new end-user application. Primary candidate `Schnittstellenentwicklung`; secondary `Schnittstellenprogrammierung`, `API Entwicklung`, `API Programmierung`. `API Integration` is informational support; broad `Systemintegration` is not the acquisition target.

Evidence: P0 and V documents record commercial Schnittstellen SERP, 110/KD6; adjacent estimates 70/KD6, 110/KD16, 140/KD30. Fresh public discovery on 2026-09-13 also found [AllBytes](https://www.allbytes.de/schnittstellenentwicklung/), [Kuhfuss](https://www.kuhfuss-it.de/leistungen/schnittstellen-integration) and [siteway](https://www.siteway.de/expertise/schnittstellen-integration/) describing interface implementation. This corroborates a page archetype only. It is not a controlled Google-DE top-10 snapshot, proof of DatenpflegeNord capabilities in those vendors, or a quantified overlap pass.

## Actual capabilities and boundaries

First-party homepage/software copy verifies APIs, webhooks, database connections, integration of existing applications and extension/modernization. Do not claim specific ERP/CRM products, certifications, 24/7 operation, managed hosting, service-level commitments, guaranteed latency or compliance without separate evidence. Existing service area is Lübeck/Schleswig-Holstein; a generic URL must not quietly add national delivery promises.

## Proposed page structure if B eventually passes

1. Direct answer: connect existing applications when supported APIs/data access and responsibilities permit it; CTA asks for source, target and desired transfer.
2. Fit/non-fit: suitable for recurring defined handoffs; use an existing connector/export when it meets requirements; missing rights/interfaces may make custom work impractical.
3. Scope: consume an existing API, implement an application interface, receive webhooks, map fields, connect a database where access is appropriate.
4. Implementation: inventory APIs/versions/permissions → define data contract/source of truth → build smallest transfer with synthetic data → verify failure/retry/duplicate behavior → review access/logging/acceptance and handover.
5. Original example labeled illustrative: request form → validate fields → approval where needed → target API → confirmed result or visible exception queue. No customer names, measured savings or fabricated screenshots. Publish a reproducible demo before calling this first-party implementation proof.
6. Security/quality: least necessary rights, protected credentials, input validation, version changes, rate limits, duplicate deliveries, timeouts, retries, safe failure and data minimization. Present as project requirements to agree, not universal certifications or guarantees.
7. APIs/webhooks/databases: explain pull vs event delivery, permission and source-of-truth choice; state that suitability depends on actual vendor interfaces.
8. Process and handover: discovery documents, sample records without personal data, acceptance examples, responsibilities for operation/changes, source/documentation/use-rights questions; no unverified maintenance bundle.
9. Cost drivers: system count, API quality, data mapping, historical migration, error recovery, access model and required tests. No prices.
10. CTA: send systems, fields, trigger/frequency and one sanitized example via `/#kontakt`.

## FAQ evidence design

These are editorial questions derived from P0 procurement/informational query families, not claimed verbatim People Also Ask exports:

- Can existing software be connected without replacing it? (Schnittstellenentwicklung procurement)
- What if the system has no usable API? (integration feasibility; validate detailed SERP)
- What is the difference between API integration and API development? (informational vs procurement split)
- When is a webhook useful? (API vs Webhook support; exact SERP pending)
- What affects implementation cost? (INTEGRATION_COST raw cluster)
- What happens when a request fails or an event arrives twice? (original engineering value; not volume-validated)

Use visible answers; FAQ markup is not part of this plan.

## Links and cannibalization

If approved later, Software keeps a concise integration summary and links to the dedicated owner; Web and AI link only when their user journey needs integration details. The new page links back to Software for custom applications and to AI for multistep automation. An informational API guide must not repeat the sales page. Before migration record exact query ownership, same-context SERP URL overlap and GSC query→page evidence where available. Preserve existing canonicals unless a separate migration is approved.

## Gate record

| Gate | State | Required evidence to change state |
|---|---|---|
| Business fit | PASS for known scope | No additional claims |
| Parent commercial demand | PASS | P0/V snapshots retained |
| Adjacent terms and S overlap | HOLD | Comparable exact-query landing-URL sets + interpretation |
| Unique content depth | HOLD | Working owned demo, sample contract, tested failure cases |
| Independent conversion purpose | PARTIAL | Review that this is sold/handled independently of broader software discovery |
| National service-area expansion | HOLD | Explicit first-party confirmation if proposed |
| Release | BLOCK | #10/#15, preview and approved package |

Until those gates pass, the new HTML route and sitemap entry must not exist.
