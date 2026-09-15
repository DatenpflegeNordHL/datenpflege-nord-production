# Golden technical / media / entity audit

Read-only production baseline: 2026-09-13, rechecked at `2026-09-13T18:59:30Z`. This is **not** verification of the new branch on production. Local baseline checks and final local validation are separate from these production observations.

## HTTP / indexability / delivery

| Check | Observed evidence | Decision |
|---|---|---|
| Seven canonical routes | All GET 200 with HTML; canonical/title/schema align with baseline source | PASS baseline only |
| robots and sitemap | GET 200; all seven canonical sitemap URLs; Google generic crawling allowed | PASS basic discovery; GSC indexation unknown |
| Edge robots parity | Live robots adds Cloudflare content signals and named crawler blocks, absent in repo | Record deployment transformation; no silent crawler-policy edits |
| HTTP and www home | Redirect to `https://datenpflege-nord.de/` and 200 | PASS sampled home variants |
| Missing route | `/golden-audit-nonexistent-20260913/` returns real HTTP 404 | PASS baseline |
| Slash redirect | All six tested no-slash subpages return 301 to `http://datenpflege-nord.de:8080/.../`; followed software case fails during TLS handling after one redirect | **P0 PRODUCTION REDIRECT / CANONICALIZATION DEFECT**; Issue #15 / reviewed nginx and deployment-contract verification required |
| Canonical/H1 | Correct origin, one H1 per page in parsed live baseline | PASS |
| Security headers | CSP enforcing, HSTS max-age 31536000, nosniff, Referrer-Policy, Permissions-Policy observed | Present; browser effectiveness still needs exact-release verification |
| Compression | HTML/JS observed zstd; CSS gzip with compressed curl requests | PASS samples |
| Cache | Sample CSS/JS/poster/portrait: public max-age 604800; robots max-age 14400; no explicit HTML Cache-Control observed | Version changed stylesheet query now; verify actual CDN query cache behavior before release |
| Contact | Existing local backend/form code; no actual message sent | Live delivery, trusted client IP and backend hash remain unverified |
| Release identity | Service HTML baseline byte hashes match source; other pages differ | No reviewed release SHA/manifest on live site proven |

All seven baseline titles and JSON-LD blocks match the source. Cloudflare transforms live output: observed examples include robots.txt augmentation, email-address obfuscation and an injected decoder script / modified homepage output. A simple full-file SHA-256 comparison between repository/origin HTML and Cloudflare-served HTML is therefore **not** sufficient production-parity evidence.

Future Production Truth must use a layered parity strategy: (1) release artifact/origin-file manifest, (2) server-side deployed-file verification, (3) HTTP semantic verification of important fields, (4) documented/expected CDN transformations and (5) browser-visible functional verification. CDN byte differences do not weaken the requirement to prove the reviewed release. No backend or Cloudflare setting changed in this task.

### P0 production redirect / canonicalization defect

Observation time: `2026-09-13T18:59:30Z` (read-only production check). Each response exposed `Server: cloudflare`; the returned `Location` itself points to the internal/upstream-looking `:8080` port. This proves Cloudflare was in the observed response path, but does **not** establish the underlying server cause.

| Requested URL | Status | Returned `Location` | Follow result |
|---|---:|---|---|
| `https://datenpflege-nord.de/softwareentwicklung-luebeck` | 301 | `http://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | Followed case failed with curl TLS `wrong version number`; effective URL reported `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/`, one redirect |
| `https://datenpflege-nord.de/webentwicklung-luebeck` | 301 | `http://datenpflege-nord.de:8080/webentwicklung-luebeck/` | Redirect target recorded; not fully followed |
| `https://datenpflege-nord.de/ki-automatisierung-luebeck` | 301 | `http://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | Redirect target recorded; not fully followed |
| `https://datenpflege-nord.de/en` | 301 | `http://datenpflege-nord.de:8080/en/` | Redirect target recorded; not fully followed |
| `https://datenpflege-nord.de/impressum` | 301 | `http://datenpflege-nord.de:8080/impressum/` | Redirect target recorded; not fully followed |
| `https://datenpflege-nord.de/datenschutz` | 301 | `http://datenpflege-nord.de:8080/datenschutz/` | Redirect target recorded; not fully followed |

The canonical trailing-slash versions of those pages return HTTP 200. Evidence classification: **live-production observation**, confidence **high** for the HTTP behavior reproduced above; root cause **unknown without reviewed configuration evidence**. Potential impact: canonical URL discovery, crawler behavior, link equity, user navigation, protocol consistency, exposure of an internal/upstream port and crawl efficiency. Remediation is outside this branch and belongs to Issue #15 plus reviewed production/nginx contract verification.

## Static scope and open browser/field checks

Existing site audit covers titles/descriptions/canonicals, one H1, IDs, internal links/fragments, local assets, JSON parsing, labels, DE/EN hreflang/structure, social fields and selected CSP/reduced-motion constraints. Golden audit adds graph reachability, local indexability/heading/image checks and service schema relationships. Neither substitutes for full WCAG assessment, search-engine schema interpretation or production headers.

Hreflang: reciprocal DE/EN home pair with x-default; no fabricated English service alternates. Important content renders in initial HTML; JS is deferred. Service page CSS is render-blocking, small and shared; no new script or external font dependency. Final local mobile/keyboard/browser evidence is recorded in `GOLDEN-VALIDATION-REPORT.md`; local browser proof is not production CWV or server parity. LCP, CLS, INP, accessibility contrast and actual transfer must be measured in the appropriate release/field environment, not inferred solely from asset sizes. No field CWV pass is claimed. Lighthouse TBT, if measured, is not INP.

## Structured data audit and scoped design

| Type | Baseline / proposed change | Gate |
|---|---|---|
| Organization | Home detailed legal entity, abbreviated same-ID service records | Preserve identity; #13 open, no sameAs/location expansion |
| WebSite | Canonical origin/publisher on home | Keep; service WebPage `isPartOf` can reference it |
| WebPage | Present for service pages | Sync title/description; link existing website and breadcrumb IDs |
| BreadcrumbList | Existing positions and URLs match visible home/service breadcrumb | Keep, connect WebPage reference |
| Service | Actual provider, URL, area and service type | Web label may include evidenced design; no new commercial category |
| LocalBusiness | Not necessary to invent a location-based subtype | HOLD pending legal and real location/profile suitability |
| FAQPage/ratings/reviews | Not needed for this change | No addition |

Use only applicable factual properties; Google's [Organization guidance](https://developers.google.com/search/docs/appearance/structured-data/organization) emphasizes accurate administrative/entity information. A [LocalBusiness implementation](https://developers.google.com/search/docs/appearance/structured-data/local-business) must describe real business details, not a service-area office fiction. Syntax success is not rich-result eligibility.

## Media inventory (all important assets)

| Asset / use | Dimensions / delivery | Alt/loading assessment | Action |
|---|---|---|---|
| `assets/branding/datenpflegenord-logo.svg`, seven-page navigation | Declared 523×104, scalable SVG, no raster srcset needed | Empty alt appropriate inside separately named home link; eager default | Keep; check accessible parent name |
| `assets/profile/dustin-zander.webp`, DE/EN home | Declared 480×600; 14,304 bytes | `Dustin Zander`, lazy, async decoding; intrinsic ratio reserved | Keep; fixed modest asset, no unneeded variants |
| `assets/hero/mainframe-poster.jpg`, DE/EN video poster | 57,423 bytes; background-style decorative video box | Poster not an img and needs no fabricated alt; video aria-hidden | Eager poster/LCP candidate; measure actual LCP before preload changes |
| `assets/hero/mainframe-hero.mp4`, DE/EN hero | ~4.59 MB; CSS positioned video fills reserved hero | `preload=none`; JS source only fine-pointer/non-reduced-motion; decorative | Measure eligible desktop cost; ensure mobile/reduced-motion makes no video request |
| `images/clients-logo/logo-1.svg` | 125×29, repeated DE/EN belt | Empty alt does not resolve false-proof appearance | Remove via reviewed PR #12 cleanup before release |
| `images/clients-logo/logo-2.svg` | 106×31, same belt | Same provenance issue | Same |
| `images/clients-logo/logo-3.svg` | 159×29, same belt | Same provenance issue | Same |
| `images/clients-logo/logo-4.svg` | 140×37, same belt | Same provenance issue | Same |
| `images/clients-logo/logo-5.svg` | 108×30, same belt | Same provenance issue | Same |
| `og-datenpflege-nord.png` | Shared social card, outside body/LCP | Social message still promotes unverified Website-Checks | HOLD redesign/reconciliation with actual offer before release; no fake screenshot |
| `apple-touch-icon.png`, `favicon.svg` | Icon metadata assets | No body alt applicable | Keep; asset dimensions checked locally |

All body images already have width, height and alt attributes. The hero video relies on its CSS box rather than HTML intrinsic dimensions; verify layout stability in browser. Raster files have descriptive names except generic template marks, which should be removed instead of renamed as clients. No new raster asset or compression dependency introduced.

Useful original visuals: software decision table implemented as HTML; interface source→validation→approval→target diagram and n8n failure-path diagram are good future owned-demo assets. Web relaunch URL mapping is useful after a real sanitized migration example exists. No fake project screenshots.

## Required later verification

Use RELEASE-VERIFICATION plus GOLDEN-IMPLEMENTATION-PLAN. Fix/explain the exposed-port redirects, verify all host/path variants and cache behavior, record exact artifact SHA and edge transformations, inspect browser/contact flow, obtain GSC/CrUX evidence and confirm meaningful sitemap dates. Server settings and external accounts remain outside this local implementation.
