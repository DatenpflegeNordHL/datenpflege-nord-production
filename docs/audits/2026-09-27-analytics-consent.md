# Audit 27.09.2026: Analytics consent

## Verification before modification

Baseline: fetched `origin/main`, `db9542d50a3c1651b37568c9b5b260ba82dc8cf6`.
Isolated worktree `/tmp/dpn-analytics-consent`, branch
`fix/analytics-consent-consistency`. Pre-existing untracked deployment files in
the user's original worktree were not copied or changed.

**F-01 VERIFIED.** Baseline `index.html:4–6`, `en/index.html:4–6`,
`softwareentwicklung-luebeck/index.html:4–6`,
`webentwicklung-luebeck/index.html:4–6`,
`ki-automatisierung-luebeck/index.html:4–6`,
`website-showcase/index.html:4–6`, all three `wissen/*/index.html:4–6`,
`impressum/index.html:5–7`, `datenschutz/index.html:5–7` load
`https://www.googletagmanager.com/gtag/js?id=G-NHB0PGPYTW` unconditionally.
`assets/service.js:1–4` unconditionally queues `js` and
`config G-NHB0PGPYTW`. No consent UI or decision storage exists.
`datenschutz/index.html:53` says “Kein Marketing-Tracking”; line 107 says
“keine Analyse-, Marketing- oder Profiling-Dienste”. EN links to this same
German privacy page; there is no separate English privacy document.

**Versioned CSP conflict VERIFIED; live conflict NOT VERIFIED.**
`ops/cloudflare/content-security-policy.txt:1` only allows self scripts and
self/GitHub connections. Live GET/HEAD on 27.09.2026 allows Tag Manager and
wildcard Google Analytics/Google connections. Media origin is already allowed
for both images and video in versioned and live CSP. Installed nginx config
was read only and matches the baseline's routing/security-header behavior.

Root cause: unconditional third-party script + unconditional configuration,
no consent gate, stale privacy statement, and drift between versioned and
Cloudflare CSP. Changes proceed only on these independently verified facts.

## Scope

Retain the measurement ID; load Google only after explicit analytics consent.
No production/configuration write, release tag, merge or contact submission.
GA collection endpoints are intercepted in browser tests so QA does not send
synthetic events to the real property. Loading the real Google script is a
read-only operation. Request attempts and cookies can still be observed.

## Minimal fix and review

- Eleven existing canonical pages replace the unconditional remote script with
  the shared local `assets/analytics-consent.js` and `.css`. No demo, URL owner,
  acquisition text, metadata or design component was changed.
- `assets/service.js` no longer configures GA. Consent code owns initialization,
  has a duplicate execution guard and issues one config per document. Equal
  reject/accept buttons, native non-modal dialog, labelled content, keyboard
  controls and a footer settings button work in DE/EN.
- Explicit accepted/denied decisions are stored locally. Missing, invalid or
  inaccessible storage fails closed. With inaccessible storage, decisions apply
  to the current document and a status message explains the limitation.
- Revocation sets Google's opt-out flag, removes reachable root-path `_ga*`
  cookies and reloads, including during script loading and across tabs. The
  reload stops the connected tag too. Already sent events cannot be recalled.
- Only the Analytics section and related tracking/date facts of the existing
  privacy page change. EN users receive English consent and an English summary
  there. Contractual provider, retention, international transfer and legal
  details remain explicitly marked for human review; no invented settings.
- Versioned CSP adds only the Google script origin and the default/observed EEA
  GA collection origins. No wildcards, inline allowance or default/style/image/
  media relaxation except the independently observed Google diagnostic image origin. The installed nginx and Cloudflare configuration is read
  only. Cloudflare ruleset version 5 already permits GA using wider wildcards;
  production policy was not changed. A future authorized release should review
  this policy drift separately; current live CSP permits the candidate origins.
- Two new local assets must be in the existing public release allowlist; that is
  the only deployment-script change. No deploy entrypoint was invoked.
- The existing CSP regression test now checks exact script/connect origins and
  bounded image origins and unchanged media/default/style sources, rejecting every wildcard. It
  does not grant unbounded domains. Real-browser tests are added to Hosted CI;
  Playwright is test tooling only, no runtime library or package manifest.

Google's current privacy controls document the opt-out flag and advertising
controls: https://developers.google.com/tag-platform/security/guides/privacy .
Configuration reference: https://developers.google.com/analytics/devguides/collection/ga4/reference/config .
CSP reference: https://developers.google.com/tag-platform/security/guides/csp .

## Additional audit points

| Point | Finding status and evidence | Action |
| --- | --- | --- |
| A HTTP/redirect defect | **NOT VERIFIED**: curl checked 52 HTTP/HTTPS, www/apex, slash variants of home, EN, three services, showcase and privacy; every final status 200, 0–2 hops, no loops. Full results in `2026-09-27-live-evidence.json`. Python urllib returned client-specific 403; independent curl and browser probes establish actual successful routing. | No change. Two hops for combined host/path normalization are expected, not a proven unnecessary chain. |
| B Header/security defect | **NOT VERIFIED**: live CSP, HSTS `max-age=31536000`, nosniff, strict-origin-when-cross-origin, SAMEORIGIN/frame-ancestors and restrictive Permissions-Policy observed. Cloudflare response-header ruleset read successfully (version 5). | No production header changes. Versioned GA CSP conflict repaired as above. |
| C Production browser defect beyond F-01 | **NOT VERIFIED**: six fresh Chromium contexts report no JS/CSP console errors in baseline evidence. All six show pre-consent Google requests and GA cookies, confirming F-01. | Consent fix only. |
| D Missing consent | **VERIFIED**: no consent UI or storage at baseline; script/config unconditional. | Consent implementation and automated four-state QA. |
| E Responsive defect | **NOT VERIFIED** as an unresolved defect: final consent candidate passes all 48 combinations (six pages × eight widths), with no document overflow and a usable dialog. Baseline hero tests also pass their seven widths. Hidden desktop service navigation at <=620px is existing intentional CSS (`assets/service.css`); brand/home and breadcrumbs preserve mobile navigation. | No unrelated layout/design change. |
| F No-JS contact completely broken | **NOT VERIFIED**: live no-JS DE/EN have an obfuscated direct email link but retain `form action="mailto:kontakt@datenpflege-nord.de"`; local no-JS retains direct link and same action. **NOT TESTABLE**: opening/using a visitor's installed mail application. | No form submission and no change: a meaningful mailto fallback remains. |
| Repository publicly visible | **VERIFIED**: `gh repo view --json visibility` returns PUBLIC. | No setting change. |
| Obvious tracked secrets | **NOT VERIFIED**: existing signature scanner reports PASS with no findings. This is the scanner's bounded scope, not a guarantee about all history. | No secrets changed. |
| Showcase media blocked by CSP | **NOT VERIFIED**: image/video origin already allowed in both versioned/live policy; candidate browser checks detect no CSP error. | No showcase-media changes. Google diagnostic image allowance is documented below. |
| Existing SEO/metadata defect | **NOT VERIFIED**: static/Golden regression gates pass for 17 HTML pages; existing metadata, sitemap, robots, canonical/hreflang and noindex demo behavior unchanged. | No SEO changes. |

## Human review / limits

The real Google script additionally dispatches to `G-KLH4MV8H8M` and sets its
cookie. This connected destination is not defined in the repository. No Google
property was created or altered; all destinations remain behind the same load
gate. Confirm the intended connected destination and actual contract/settings
in Google before legal sign-off. This is an independently observed configuration
gap, not a reason to invent provider/retention facts.

Local privileged installation fixtures could not run: `sudo -n` requires a
password. Those tests use isolated fixtures; no production installation was
attempted. Hosted CI already runs them as root. Local suite reports its skips
explicitly. A visitor's mail client and legal/provider decisions cannot be proven
by these automated tests.

The first candidate responsive run reproduced a new 320px privacy-footer
horizontal overflow: the added settings button enlarged the existing no-wrap
`.footer-links`. Root cause was confirmed using element bounding rectangles.
The consent code now marks only its own footer container and the consent CSS
allows that container to wrap. Existing page styles/design remain untouched;
the full responsive run passes after this repair.

Test harness notes: desktop service navigation is deliberately hidden on narrow
screens; the test verifies the still-visible home/brand link and keyboard access
rather than requiring a desktop-only element to remain visible. GitHub feed
reads use deterministic test responses in consent QA to avoid public rate limits.
Chromium can report `ERR_ABORTED` for intercepted keepalive/beacon collection
responses. The harness records those specific mocked aborts separately and
continues to fail on all internal failures, real third-party failures and all
console/CSP errors. This is not evidence of successful delivery to Google;
collection delivery and property reporting were intentionally not tested.

A later real-script run reproduced a CSP violation for Google’s diagnostic
image `https://www.googletagmanager.com/td` after consent. This is independent
browser evidence, so the final policy also adds that one exact origin to
`img-src`. No Analytics image wildcard is added. The fallback collection host
`www.google-analytics.com` is confirmed in the fetched real script’s URL builder
(`https://` + region-or-`www` + `.google-analytics.com/g/collect`); the EEA browser
actually uses `region1.google-analytics.com`. Script, connection and diagnostic
image allowances therefore each have a concrete reason.

## Final local acceptance

- Repository suite: 101 tests, OK, 15 privileged fixture tests skipped locally.
  Existing real-browser hero, contact stub, reduced-motion and nginx freshness
  tests ran successfully with installed agent-browser 0.27.0 and `--no-sandbox`.
  Contact payloads were sent only to isolated test fixtures, never production.
- Static Site Audit: PASS, 17 HTML pages. Golden Audit: PASS.
- Asset graph/hash check: PASS, 145 references. Deterministic generator's second
  run: `changed_files: []`. No manually chosen hashes.
- Secret scanner: PASS, zero findings. Diff whitespace, changed JS syntax,
  deployment shell syntax and Python syntax: PASS.
- Consent Chromium suite: 12 scenarios and 48 responsive cases PASS, real
  Google script and enforced versioned CSP; collection endpoints intercepted.
  Eight widths: 320, 360, 390, 430, 768, 1024, 1440, 1920. Screenshots at 390/844
  and 1440/900 were visually reviewed; labelled content and equally usable
  buttons fit. No redesign.
- Requests before decision: NO. After rejection: NO. After acceptance: YES
  (intercepted collection attempt for `G-NHB0PGPYTW`). Duplicate initialization:
  NO; one script/config/pageview per document. CSP/JS errors: NO in final QA.
  Decision persists after reload: YES. Settings can be changed: YES.
- Storage blocked/corrupt, cross-tab revocation, in-flight script revocation and
  no-JS DE/EN contact fallback: PASS. No mail client delivery was tested.
- Exact final Git archive verification and Hosted CI are required before this
  PR is reported complete; their SHA/run evidence is linked in the final PR
  report. These gates do not authorize production activation or merge.

The browser evidence JSON strips generated client IDs/full collection queries.
It retains statuses, page/width checks and host/path/measurement-ID evidence.
A separate read-only agent-browser live smoke was also performed; unlike the
intercepted baseline and acceptance suites, ordinary live navigation can trigger
the site's pre-existing analytics. No GA property/settings were changed, and
no claims are made about unchanged reporting counters.

Stricter cross-tab probing also captured an already consented pageview flushed
from GA's send buffer on reload (`en=page_view`, original document ID). This is
a real limitation of the loaded Google library: the opt-out flag/reload do not
retroactively cancel previously captured queued data. The public privacy text
now states that limitation. Fresh rejection and post-reload documents remain
request-free. The stable cross-tab test waits for initial collection to finish
before measuring new requests from withdrawal; it does not erase captured
requests. Do not interpret “no requests after rejection” as a promise to cancel
in-flight or already buffered consented events.
