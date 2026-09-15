# Google Search Console validation plan

Updated 2026-09-15. **First-party measurement dependency.** Access has not been established in this task. “Not connected to SE Ranking” does not prove no GSC property exists. No property, DNS, token or account changes were made, and no verification token was added.

## Ready-to-connect targets

| Item | Prepared value |
|---|---|
| Property target | Domain property `datenpflege-nord.de` if already owned or eligible for DNS verification |
| Preferred canonical domain | `https://datenpflege-nord.de/` (hyphenated, HTTPS) |
| Wrong-domain exclusion | `datenpflegenord.de` is unrelated and must not be selected or consolidated |
| Verification requirement | Owner checks existing properties first; otherwise complete Google's current DNS verification with an authorized DNS operator |
| Sitemap submission | `https://datenpflege-nord.de/sitemap.xml` |
| Baseline date | Capture on the actual connection date; planned release-preparation baseline is `2026-09-15`, not a fabricated data start |
| Initial inspection list | `/`, `/softwareentwicklung-luebeck/`, `/wissen/individualsoftware-kosten/`, `/webentwicklung-luebeck/`, `/wissen/website-relaunch-checkliste/`, `/ki-automatisierung-luebeck/`, `/en/`, `/impressum/`, `/datenschutz/` |

## Query/page monitoring template

| Period | Query | Cluster | Landing page | Country | Device | Impressions | Clicks | CTR | Position | Google canonical | Last crawl | Qualified lead evidence | Decision |
|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|
| YYYY-MM-DD–YYYY-MM-DD | exact exported query | Software / Web / Automation / Brand | canonical URL | DE | mobile/desktop | GSC value | GSC value | GSC value | GSC value | inspected value | inspected value | aggregate/no PII | retain, revise, investigate or HOLD |

## Connection and baseline

Business owner first checks existing properties and grants the minimum useful access to the canonical site. Prefer the existing domain property for `datenpflege-nord.de`; verify ownership through the account's supported flow if none exists. Never use unrelated `datenpflegenord.de`. Keep credentials/exported personal data outside this repository. Account/DNS changes need separate authorization.

Export the longest available baseline, then comparable complete 28-day windows with search type, country and device fixed. Save extraction date, timezone/report dates, property and filter definitions. Sparse/suppressed query rows are not zero demand. The [Search Console Performance report](https://support.google.com/webmasters/answer/7576553) documents clicks, impressions, CTR and average position; interpret these with their report dimensions and limitations.

| Analysis | Required evidence | Action criterion |
|---|---|---|
| Submitted vs indexed | Nine canonical sitemap URLs, Page Indexing reasons, inspection per owner | Investigate exclusions individually; no blanket indexing requests |
| Canonicals / duplicates | User canonical vs Google canonical, crawl date, rendered HTML | Resolve genuine mismatch; do not split owners first |
| Query and page impressions | Query→page table for S/W/A, country/device/time | Update ownership from observed data; multiple URLs may be legitimate for different tasks |
| CTR and average position | Clicks/impressions/position by comparable cluster | Improve titles/snippets when relevance and impressions justify; avoid noisy tiny samples |
| Brand | DatenpflegeNord, Datenpflege Nord, hyphenated domain/spelling variants | Track entity confusion separately; no wrong-domain ownership inference |
| Local | Lübeck/Luebeck, Kiel, Hamburg, Schleswig-Holstein modifiers | Impressions do not establish ability to serve a city |
| Long-tail procurement | entwickeln lassen, erstellen lassen, Schnittstellen, n8n integration | Promote useful sections; revise priorities over third-party volume |
| Crawl/index exclusions | Noindex, blocked resources, redirects, errors, duplicate/crawled-not-indexed | Match reason to live HTML/HTTP and last crawl |
| CWV | Mobile/desktop groups, available LCP/INP/CLS field data | No data = unknown; correlate with lab evidence |
| Schema / rich results | Supported enhancement reports and URL inspection | Validate syntax and factual parity; absent Service rich-result report is not necessarily an error |
| Leads | Aggregate successful qualified inquiries per landing page where lawful measurement exists | No PII in logs/exports; no new analytics or invented conversions in this task |

### Phase-5 authority monitoring

After a later approved release, monitor the two new URLs independently. Baselines begin only when real GSC data exists.

| URL | Intended query family | Watch for competing page | Measurements |
|---|---|---|---|
| `/wissen/individualsoftware-kosten/` | Individualsoftware Kosten, Kostentreiber, Standardsoftware oder Eigenentwicklung, Projektumfang | `/softwareentwicklung-luebeck/` | Impressions, clicks, CTR, average position, query cluster, Google canonical and index status |
| `/wissen/website-relaunch-checkliste/` | Website Relaunch Checkliste, Redirect-Mapping, Relaunch Fehler vermeiden | `/webentwicklung-luebeck/` | Impressions, clicks, CTR, average position, query cluster, Google canonical and index status |

If the authority page and Money page appear for the same query, classify the query task before changing ownership. Commercial/local terms stay with the Money page; planning and checklist terms stay with the authority asset.

## Cadence and decision loop

Before release: archive current query/page/index baseline if access exists. After later release verification: submit/confirm `https://datenpflege-nord.de/sitemap.xml`; inspect home and the three changed owners. At 7 days inspect crawl/canonical regressions; at 28 days compare complete query/CTR windows; at 90 days review sustained visibility, qualified leads and ownership. If sample is insufficient, extend observation rather than generating more pages.

Record cluster, query, primary/secondary ranking URL, impressions, clicks, CTR, position, device/country, period, lead evidence and next decision. S/W overlap on Webanwendungen needs human task interpretation. API or regional BUILD decisions require Business Truth and unique value even when impressions grow.

Google AI feature traffic is included in Web search reporting; do not label a GSC slice an exact AI-citation counter. Separate repeatable manual AI source observations by prompt/date/engine from measured GSC traffic. Third-party volume never outranks actual first-party query evidence.
