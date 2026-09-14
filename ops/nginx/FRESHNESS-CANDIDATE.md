# HTML freshness candidate (not installed)

Baseline: read-only snapshot of the datenpflege-nord vhost on 2026-09-14.
`datenpflege-nord-html-freshness.patch` adds an http-context map and ONE header
in the existing website server. Apply only to an isolated snapshot for review.
Never apply this patch directly to `/etc/nginx` as part of candidate testing.

Policy: `Cache-Control: no-cache`. HTML may be stored and must revalidate before
normal reuse. ETag and Last-Modified are retained; nginx conditional GET can
return 304. nginx removes Content-Type on 304, so the map also recognizes the
resolved `.html` URI for that status. Other MIME types get an empty map value
and no header. The map must reside in http context (the vhost is included there).

The header sits beside existing server security headers, avoiding add_header
inheritance loss from a new location-level header. Existing location-specific
static/OG/contact headers remain exactly as in the baseline. In particular,
existing security-header inheritance gaps on those locations are outside this
minimal freshness change; they are not falsely described as repaired.

Tests launch baseline and patched candidate nginx with private pid/log files,
a temporary public tree, random loopback ports and a contact stub. They run
`nginx -t`, every page/HTML route, 200/304 validators/security comparisons,
CSS/JS/image/media/OG/robots/sitemap/health/contact checks. They never invoke
nginx reload or the production deployment entrypoint. The media-subdomain
configuration is neither included nor changed.

```bash
python3 -m unittest discover -s tests -p test_nginx_freshness.py
DPN_AGENT_BROWSER=/absolute/path/to/agent-browser \
  python3 -m unittest discover -s tests -p test_nginx_freshness.py
```

The browser test uses a unique isolated origin and ONE persistent browser cache:
normal navigation → same HTML → observed server 304; mutate meaningful test HTML
and leaf SVG → deterministic leaf/CSS/HTML URL update → normal navigation gets
new HTML and requests the new asset URLs with 200. Fetch of the OLD asset URL
still returns cached old bytes; the unchanged SVG keeps its original URL. No
cache clearing or forced no-cache fetch is used. The fixture changes HTML mtime
only to exercise nginx's existing coarse validator in a sub-second test; this
is not an asset version or production build timestamp.

Future release acceptance must additionally repeat normal navigation through
the public edge with browser DevTools/CDP network recording, preserving cache:
verify outgoing validators and 304 (or validated 200), change meaningful HTML
and an asset in an approved release, navigate normally, inspect the new HTML
and new hash URL/bytes, and confirm the unchanged asset URL. CDN/header overrides
must not negate `no-cache`; an origin-only candidate cannot certify the edge.
Do not release until Issue #10 main protection is actually enforced.
