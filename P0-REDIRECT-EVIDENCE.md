# P0 Redirect Evidence

Observation window: 2026-09-13, final origin isolation at `2026-09-13T21:22:25+02:00`.

Evidence classes are deliberately separated:

- **Public edge observation:** requests to `datenpflege-nord.de`, response path includes Cloudflare (`Server: cloudflare`).
- **Origin observation:** direct read-only requests to `127.0.0.1:8080` with `Host: datenpflege-nord.de`, bypassing Cloudflare.
- **Configuration evidence:** read-only inspection of active nginx configuration on the host.

## Expected invariant

Every non-canonical HTTP/HTTPS slash variant must converge through a bounded redirect chain to `https://datenpflege-nord.de/<canonical-path>/`. No redirect chain may expose `:8080`, localhost, an internal hostname or an origin-only address. The canonical public result must use HTTPS.

## Public edge matrix

All requests below used read-only HTTP GETs. `rc=35` is curl/OpenSSL `wrong version number` after the chain reaches `https://datenpflege-nord.de:8080/.../`.

| Requested URL | First status | First Location | Edge | Final/follow result | Expected | Result |
| --- | ---: | --- | --- | --- | --- | --- |
| `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | — | Cloudflare | 200, 0 redirects | same URL, 200 | PASS |
| `https://datenpflege-nord.de/softwareentwicklung-luebeck` | 301 | `http://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | Cloudflare | rc=35 after 1 redirect; effective `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | HTTPS canonical slash URL | **FAIL** |
| `http://datenpflege-nord.de/softwareentwicklung-luebeck/` | 301 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | Cloudflare | 200 after 1 redirect | HTTPS canonical slash URL | PASS |
| `http://datenpflege-nord.de/softwareentwicklung-luebeck` | 301 | `https://datenpflege-nord.de/softwareentwicklung-luebeck` | Cloudflare | rc=35 after 2 redirects; effective `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | HTTPS canonical slash URL | **FAIL** |
| `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | — | Cloudflare | 200, 0 redirects | same URL, 200 | PASS |
| `https://datenpflege-nord.de/webentwicklung-luebeck` | 301 | `http://datenpflege-nord.de:8080/webentwicklung-luebeck/` | Cloudflare | rc=35 after 1 redirect; effective `https://datenpflege-nord.de:8080/webentwicklung-luebeck/` | HTTPS canonical slash URL | **FAIL** |
| `http://datenpflege-nord.de/webentwicklung-luebeck/` | 301 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | Cloudflare | 200 after 1 redirect | HTTPS canonical slash URL | PASS |
| `http://datenpflege-nord.de/webentwicklung-luebeck` | 301 | `https://datenpflege-nord.de/webentwicklung-luebeck` | Cloudflare | rc=35 after 2 redirects; effective `https://datenpflege-nord.de:8080/webentwicklung-luebeck/` | HTTPS canonical slash URL | **FAIL** |
| `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | — | Cloudflare | 200, 0 redirects | same URL, 200 | PASS |
| `https://datenpflege-nord.de/ki-automatisierung-luebeck` | 301 | `http://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | Cloudflare | rc=35 after 1 redirect; effective `https://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | HTTPS canonical slash URL | **FAIL** |
| `http://datenpflege-nord.de/ki-automatisierung-luebeck/` | 301 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | Cloudflare | 200 after 1 redirect | HTTPS canonical slash URL | PASS |
| `http://datenpflege-nord.de/ki-automatisierung-luebeck` | 301 | `https://datenpflege-nord.de/ki-automatisierung-luebeck` | Cloudflare | rc=35 after 2 redirects; effective `https://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | HTTPS canonical slash URL | **FAIL** |
| `https://datenpflege-nord.de/en/` | 200 | — | Cloudflare | 200, 0 redirects | same URL, 200 | PASS |
| `https://datenpflege-nord.de/en` | 301 | `http://datenpflege-nord.de:8080/en/` | Cloudflare | rc=35 after 1 redirect; effective `https://datenpflege-nord.de:8080/en/` | HTTPS canonical slash URL | **FAIL** |
| `http://datenpflege-nord.de/en/` | 301 | `https://datenpflege-nord.de/en/` | Cloudflare | 200 after 1 redirect | HTTPS canonical slash URL | PASS |
| `http://datenpflege-nord.de/en` | 301 | `https://datenpflege-nord.de/en` | Cloudflare | rc=35 after 2 redirects; effective `https://datenpflege-nord.de:8080/en/` | HTTPS canonical slash URL | **FAIL** |
| `https://datenpflege-nord.de/impressum/` | 200 | — | Cloudflare | 200, 0 redirects | same URL, 200 | PASS |
| `https://datenpflege-nord.de/impressum` | 301 | `http://datenpflege-nord.de:8080/impressum/` | Cloudflare | rc=35 after 1 redirect; effective `https://datenpflege-nord.de:8080/impressum/` | HTTPS canonical slash URL | **FAIL** |
| `http://datenpflege-nord.de/impressum/` | 301 | `https://datenpflege-nord.de/impressum/` | Cloudflare | 200 after 1 redirect | HTTPS canonical slash URL | PASS |
| `http://datenpflege-nord.de/impressum` | 301 | `https://datenpflege-nord.de/impressum` | Cloudflare | rc=35 after 2 redirects; effective `https://datenpflege-nord.de:8080/impressum/` | HTTPS canonical slash URL | **FAIL** |
| `https://datenpflege-nord.de/datenschutz/` | 200 | — | Cloudflare | 200, 0 redirects | same URL, 200 | PASS |
| `https://datenpflege-nord.de/datenschutz` | 301 | `http://datenpflege-nord.de:8080/datenschutz/` | Cloudflare | rc=35 after 1 redirect; effective `https://datenpflege-nord.de:8080/datenschutz/` | HTTPS canonical slash URL | **FAIL** |
| `http://datenpflege-nord.de/datenschutz/` | 301 | `https://datenpflege-nord.de/datenschutz/` | Cloudflare | 200 after 1 redirect | HTTPS canonical slash URL | PASS |
| `http://datenpflege-nord.de/datenschutz` | 301 | `https://datenpflege-nord.de/datenschutz` | Cloudflare | rc=35 after 2 redirects; effective `https://datenpflege-nord.de:8080/datenschutz/` | HTTPS canonical slash URL | **FAIL** |

A representative `https://www.datenpflege-nord.de/softwareentwicklung-luebeck` chain also fails after two redirects at `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/`.

## Origin isolation

The active canonical nginx server listens on `127.0.0.1:8080`, has `server_name datenpflege-nord.de`, `root /srv/datenpflege-nord/current`, and serves the static site with:

```nginx
location / {
    try_files $uri $uri/ $uri.html =404;
}
```

Direct GETs to the origin with `Host: datenpflege-nord.de` reproduce the same defect for all six no-slash paths. Example:

```text
GET http://127.0.0.1:8080/softwareentwicklung-luebeck
Host: datenpflege-nord.de

HTTP/1.1 301 Moved Permanently
Server: nginx
Location: http://datenpflege-nord.de:8080/softwareentwicklung-luebeck/
```

The slash form at the same origin returns 200. Supplying `X-Forwarded-Proto: https`, `X-Forwarded-Port: 443`, and `X-Forwarded-Host: datenpflege-nord.de` still produces the same `http://...:8080/.../` Location.

Configuration search found no active `absolute_redirect`, `port_in_redirect`, `X-Forwarded-Port`, or `X-Forwarded-Host` handling for this static server. `X-Forwarded-Proto` exists only in the generic `/etc/nginx/proxy_params` file and is not used by the static-site server to construct this redirect.

## Proven root cause

**P0 PRODUCTION REDIRECT / CANONICALIZATION DEFECT.**

The defect originates in nginx before Cloudflare. A no-slash URI maps to a real directory under `/srv/datenpflege-nord/current`; nginx normalizes that directory URI to a slash form. Because the origin request is plain HTTP on port 8080 and the server does not override nginx's absolute/port redirect behavior, nginx constructs the absolute redirect from the origin context and emits `http://datenpflege-nord.de:8080/<path>/`.

Cloudflare is present in the public response path and forwards the defective Location externally. The failure is therefore an origin redirect-construction defect exposed through the CDN, not a Cloudflare-only transformation.

Confidence: **high**. The same Location was reproduced directly at the local nginx origin, independent of Cloudflare.
