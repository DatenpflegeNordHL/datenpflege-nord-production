# SE Ranking Evidence — DatenpflegeNord

Checked: 2026-09-10
Scope: Germany / German, plus city-level Google SERP snapshots for Lübeck where noted.
Purpose: evidence for Golden Website Build 2.0. These numbers are planning evidence, not guarantees and not a substitute for Google Search Console.

## 1. Tracking project

A manual SE Ranking project was created for `https://datenpflege-nord.de` with website audit disabled and no automatic reports. Google Germany / German is attached as the rank-tracking engine. Ten high-priority keywords are tracked manually.

The first country-level position check returned measurable rows for eight keywords. All eight were outside the tracked Google top 100 on 2026-09-10 (`pos=0`). Two newly added keywords were not returned in the first stats response and must not be treated as confirmed ranking data yet.

## 2. Exact/high-confidence keyword evidence

| Keyword | DE monthly volume | KD | CPC / suggested bid | Intent / note | Current decision |
|---|---:|---:|---:|---|---|
| `softwareentwicklung lübeck` | 110 | 34 | ~€0.54–0.62 | Local + Commercial; SERP partly polluted by job intent | OWN `/softwareentwicklung-luebeck/` |
| `webentwicklung lübeck` | 40 | 52 | ~€2.11–3.42 | Local + Commercial; strong agency/webdesign SERP | OWN `/webentwicklung-luebeck/` |
| `website erstellen lassen lübeck` | 10 | 45 | low/unstable exact CPC | Local + Commercial; much thinner SERP than web development/webdesign | EXPAND existing web page; no clone URL |
| `n8n automatisierung` | 110 | n/a exact tracked row | ~€1.66 | Mixed informational + commercial; dedicated n8n service/agency pages present | HOLD specialist child; now stronger candidate |
| `individuelle softwareentwicklung` | 320 | 12 in keyword expansion | up to ~€13.67 in expansion dataset | Strong commercial fit; overlaps core software service | EXPAND existing software page |
| `softwareentwicklung agentur` | 140 | 30 in expansion dataset | ~€7.97 tracked / ~€9.11 expansion | Strong commercial procurement wording | Supporting intent; no new URL yet |
| `softwareentwicklung dienstleister` | 110 | 39 in expansion dataset | ~€16.49 tracked | Strong buyer intent | EXPAND existing software page |
| `ki automatisierung agentur` | 140 | 17 | ~€6.10 | Commercially valuable agency/procurement phrase although SE Ranking labels the row informational | Strengthen AI page; separate URL still HOLD |

Notes:
- SE Ranking and Ubersuggest disagree on some volumes/KD, especially `webentwicklung lübeck`. This is expected across third-party clickstream/search-volume models. Search Console will remain the first-party tie-breaker after connection.
- `ki automatisierung lübeck` returned volume 0 in the project dataset. This is not evidence that the service page has no strategic/local value; the local SERP still exists and the page is already a verified business-service owner.

## 3. Lübeck SERP evidence

### `softwareentwicklung lübeck`

City-level Google snapshot for Lübeck on 2026-09-10:
- heavy mixed intent: job boards occupy many organic positions;
- commercial providers still rank prominently, including RXM, EXORD and Software-and-Testing;
- `datenpflege-nord.de` did not appear in the returned top-90 organic snapshot.

Implication: keep the local software page, but avoid interpreting the full 110 monthly volume as pure buyer traffic. Commercial copy must clearly disambiguate service intent from employment/study intent.

### `webentwicklung lübeck`

City-level Google snapshot for Lübeck on 2026-09-10:
- strong commercial/local agency SERP;
- webdesign, website creation and web development are heavily blended;
- prominent results include HANSOLU, Netzhirsch, Seiten-Werk, Augustin Marketing, Popien, Mindweb, jamp and vicon;
- review-rich/local-business style results are common;
- `datenpflege-nord.de` did not appear in the returned snapshot.

Implication: `/webentwicklung-luebeck/` should remain the single owner for the overlapping webdesign/web-development/website-creation cluster. Proof/reviews/local authority matter at least as much as lexical keyword coverage.

### `website erstellen lassen lübeck`

City-level Google snapshot for Lübeck on 2026-09-10:
- very small/thin organic result set compared with `webentwicklung lübeck`;
- commercial ads and a few exact-match service pages dominate;
- significant irrelevant/noisy organic results are present;
- `datenpflege-nord.de` did not appear in the returned result set.

Implication: do not create `/website-erstellen-lassen-luebeck/` as a near-duplicate. Continue using the existing web-development page as the commercial owner and cover the phrase naturally within it.

## 4. n8n SERP evidence

Country-level Google Germany snapshot for `n8n automatisierung` on 2026-09-10:
- AI Overview is present;
- n8n itself ranks first organically;
- SERP mixes guides/tutorials with commercial implementation providers;
- dedicated commercial/service results include `n8n-agentur.de`, Elastic Brains, Team23, Fleckinger Media, Seibert Group and other n8n-specific providers;
- dedicated URLs such as `/n8n`, `/n8n-automatisierung/` and n8n service pages are common.

Implication: n8n now passes the SERP-distinction gate more strongly than before. It still remains HOLD until Business Truth confirms that DatenpflegeNord wants to sell n8n implementation as a named standalone service and the future page can contain real process/integration proof rather than generic tool copy.

## 5. DatenpflegeNord organic baseline

SE Ranking domain-keyword database for Germany returned no organic keyword rows for `datenpflege-nord.de` at the time of checking.

The first manual rank-tracking check returned eight measured tracked keywords, all outside top 100 on 2026-09-10. This is a stronger baseline than generic web-search absence, but Search Console is still required to determine whether Google has impressions outside these selected queries and to inspect canonical/index state.

## 6. Backlink / authority baseline

SE Ranking backlink summary on 2026-09-10:

| Domain | Backlinks | Referring domains | Domain InLink Rank |
|---|---:|---:|---:|
| `datenpflege-nord.de` | 0 | 0 | 0 |
| `software-and-testing.de` | 46 | 37 | 31 |
| `exord.de` | 326 | 127 | 55 |
| `hansolu.de` | 24,288 | 374 | 67 |
| `netzhirsch.de` | 9,196 | 458 | 71 |

Interpretation:
- raw backlink counts for web agencies can be heavily inflated by sitewide footer/design-credit links;
- referring domains and source quality are therefore more useful planning signals than raw backlink totals;
- DatenpflegeNord is starting from an externally measurable authority baseline of zero in this dataset;
- first priority is legitimate entity/profile/reference links, not bulk directory or purchased-link volume.

## 7. AI / GEO baseline

SE Ranking AI Search overview for Germany / all supported engines returned:
- Brand Presence: not yet measurable / n/a;
- Link Presence: 0;
- AI Opportunity Traffic: 0;
- Average Position: n/a.

This is the canonical pre-optimization AI-search baseline for the current workstream. Do not claim existing AI-search visibility before new evidence appears.

## 8. Golden decisions changed by this evidence

1. `softwareentwicklung lübeck`: confirmed meaningful local demand, but mixed job/service intent means stronger commercial disambiguation is required.
2. `webentwicklung lübeck`: confirmed commercial owner; no separate webdesign or website-creation clone page.
3. `website erstellen lassen lübeck`: lower-volume, thin/noisy local SERP strengthens EXPAND-not-SPLIT decision.
4. `individuelle softwareentwicklung`: 320-volume supporting cluster strengthens expansion of the existing software page rather than a lexical duplicate.
5. `n8n automatisierung`: promoted from merely promising to the strongest specialist child-page candidate, but remains HOLD behind Business Truth/proof gate.
6. Authority/E-E-A-T is a major competitive deficit: legitimate referring-domain growth is now a P1 growth requirement.
7. AI/GEO visibility baseline is effectively zero; improvements must be measured from this point forward.

## 9. Required next evidence

- Google Search Console property connection and query/page/index baseline;
- Search Console cannibalization check after the content PR ships;
- verify Business Truth for n8n as a named sellable service;
- inspect backlink sources of a small number of relevant competitors for legitimate replicable opportunities, excluding obvious sitewide-credit spam;
- re-run tracked positions after production deployment and indexing, not merely after repository changes;
- measure AI Search again only after entity/authority/content changes have been live long enough to be crawled.