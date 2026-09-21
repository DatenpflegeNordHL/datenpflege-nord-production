# CSP rollout state

Production currently serves an enforcing `Content-Security-Policy` at the Cloudflare edge. The live policy observed on 2026-09-21 allows only same-origin images (`img-src 'self' data:`) and same-origin media (`media-src 'self'`). The Website Showcase intentionally publishes its legacy preview posters and videos from the dedicated origin `https://media.datenpflege-nord.de`, so the current edge policy blocks those resources.

The reviewed target policy is versioned in `ops/cloudflare/content-security-policy.txt`. Relative to the currently observed Production policy it changes only these directives:

```text
img-src 'self' data: https://media.datenpflege-nord.de;
media-src 'self' https://media.datenpflege-nord.de;
```

Do not add wildcard origins, broad HTTPS allowances or `unsafe-inline`. Applying or changing the Cloudflare response-header rule remains a production human gate and requires separate explicit authorization. Before promotion, browser-test the exact candidate policy against the Website Showcase and the existing public site, then repeat the public edge verification after the authorized release.
