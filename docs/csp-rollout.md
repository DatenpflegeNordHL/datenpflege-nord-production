# CSP rollout state

Production currently serves `Content-Security-Policy-Report-Only` at the Cloudflare edge. The policy is compatible with the currently deployed release by allowing only the exact SHA-256 hashes of its inline script/style blocks and the two existing GitHub runtime hosts. Executable inline JavaScript is not broadly allowed.

The repository branch removes all executable inline scripts, inline `<style>` blocks, style attributes and the `raw.githubusercontent.com` media dependency. Because repository changes must not be deployed directly from this hardening task, enforcement must wait for the pull request to be reviewed, merged and deployed.

After that deployment, replace the report-only value with the following target policy:

```text
default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; form-action 'self' mailto:; connect-src 'self' https://api.github.com; img-src 'self' data:; media-src 'self'; font-src 'self'; manifest-src 'self'; script-src 'self'; script-src-attr 'none'; style-src 'self'; style-src-attr 'none'; upgrade-insecure-requests
```

Keep it in report-only mode for a browser pass over all seven routes, including contact-form validation, GitHub feed refresh, reduced-motion emulation and fine-pointer hero scrubbing. Switch the header name to `Content-Security-Policy` only when the console and network log contain no CSP violations and no functional JavaScript errors. Do not add `unsafe-inline`, `raw.githubusercontent.com` or broader GitHub origins back to the target policy.
