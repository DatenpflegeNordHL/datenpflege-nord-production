# Bing / Copilot / IndexNow deployment design

2026-09-13. **HOLD implementation/activation until an approved release and verified property.** No verification key generated, DNS changed or URL submitted.

## Bing ownership and discovery

Check the owner's existing Bing Webmaster Tools account/property for `https://datenpflege-nord.de/`. Reuse existing verification; if absent, obtain the currently offered verification record/file/tag from that account (or supported GSC import after GSC ownership). The [Bing help entry](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b) is dynamic and exposed no usable instructions to this audit; confirm the actual flow in the account rather than inventing a token or claiming success.

After authorized verification and live release acceptance, submit the canonical `https://datenpflege-nord.de/sitemap.xml`, inspect all seven URLs, then monitor crawl/index/canonical findings and available search/referral reports. Bing indexation improves discovery eligibility; it does not prove Copilot citation or rankings.

## IndexNow contract

Follow [IndexNow documentation](https://www.indexnow.org/documentation): a host-bound key file verifies submitted URLs; supported batches contain up to 10,000 URLs, and changes include additions, updates and deletions. This site only needs a tiny release delta. A key file is intentionally publicly readable verification material, not a secret credential.

Future implementation should:

1. Create and review the verification file outside this content change; explicitly allowlist it in the public package. Verify the exact HTTPS key location after deployment.
2. Compare the **previous deployed** and **new approved** manifests plus the page-content change ledger. Draft Git diffs alone are not release deltas. Map `dir/index.html` to its canonical trailing-slash URL. Never submit private docs, scripts, assets, query variants or previews.
3. Prepare an immutable list of added/meaningfully changed/deleted canonical URLs for that release SHA. Do not send every sitemap entry for a deployment, timestamp edit or shared CSS-only change.
4. Submit only after successful production parity. Payload uses `host: datenpflege-nord.de`, verified `keyLocation` on that host, and `urlList` limited to the reviewed set. For this content scope the expected changed set is the three Lübeck service URLs; additions/deletions are empty. Recompute at final release if other changes are combined.
5. Removed URLs must actually return the intended 404/410 or reviewed redirect. Never announce a draft deletion. Exclude noindex, unrelated hosts, fragments and internal evidence.
6. Record release SHA, URL list/digest, timestamp, HTTP response and retry state. Treat 200/202 as protocol acknowledgment, not indexed/ranked proof. Retry transient 429/5xx failures with bounded backoff; investigate validation/ownership errors before retrying. Dedupe submissions per release to avoid repeated whole-site requests.

No ranking guarantee, no special AI files/schema. Any change to release allowlists, verification files or post-release submission automation needs its own tested implementation and explicit external-action authorization.
