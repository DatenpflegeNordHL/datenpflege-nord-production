# P0 Redirect Evidence

## Production remediation — 2026-09-14 (current evidence)

**Redirect P0: CLOSED (24/24 public variants PASS). Issue #10: OPEN. Issue #15: OPEN.** This supersedes the historical redirect failures below; it does not authorize a website deployment.

Controlled production change: 2026-09-14T09:23:03Z to 2026-09-14T09:25:03Z (11:23–11:25 Europe/Berlin). HTTP matrix window: 2026-09-14T09:24:45.657071+00:00 to 2026-09-14T09:24:53.764275+00:00.

- Active config: `/etc/nginx/sites-available/datenpflege-nord.conf`; enabled symlink unchanged.
- Exact pre-change backup: `/etc/nginx/sites-available/datenpflege-nord.conf.p0-20260914T092303Z.backup`; `cp -p`, matching SHA-256 and `cmp` PASS. Production metadata retained.
- Before / backup SHA-256: `883cdfa48bb8a6f872db01717669c9b258cd4fe524dade03c593a8344c338373`.
- After SHA-256: `56fb8e9b224fb6ce191e9a8911f626a48481650af64d875ea3b9873fc17444f3`.
- Extra pre-fix checkpoint: `/etc/nginx/sites-available/datenpflege-nord.conf.p0-20260914T092449Z.pre-fix.backup` (created 09:23:56Z; same pre-change hash).
- Duplicate moved from `/etc/nginx/sites-enabled/datenpflege-nord.conf.backup-og` to `/etc/nginx/sites-available/datenpflege-nord.conf.backup-og.p0-20260914T092303Z.disabled`; not deleted. Before/after duplicate SHA-256: `1debe37ef7c9e25e0f994feb963439f461d848a623bcb09e977e97e7ee2e2e72`.
- Initial privileged `nginx -t`: syntax OK / test successful, with exactly the known canonical and www conflicting-server-name warnings.
- After duplicate deactivation, before directive edit, after directive edit / pre-reload and final privileged `nginx -t`: syntax OK / test successful, no warnings.
- Pre-change Contact Health: HTTP 200, `{"ok": true}`. Pre-change origin `/softwareentwicklung-luebeck`: 301, `Location: http://datenpflege-nord.de:8080/softwareentwicklung-luebeck/`.
- `sudo systemctl reload nginx`: exit 0, graceful reload only. No restart. Post-reload and final service status: `active`.
- Only the canonical server changed; the www explicit HTTPS redirect and contact proxy configuration are byte-unchanged.

Exact applied config diff:

```diff
--- before/datenpflege-nord.conf
+++ after/datenpflege-nord.conf
@@ -8,6 +8,7 @@
 server {
     listen 127.0.0.1:8080;
     server_name datenpflege-nord.de;
+    absolute_redirect off;

     root /srv/datenpflege-nord/current;
     index index.html;
```

### Origin matrix

GETs to `127.0.0.1:8080`, `Host: datenpflege-nord.de`. Slashless response must be 301 with relative Location; slash response must be 200.

| Path | Without slash | Location | With slash | Result |
| --- | ---: | --- | ---: | --- |
| `softwareentwicklung-luebeck` | 301 | `/softwareentwicklung-luebeck/` | 200 | PASS |
| `webentwicklung-luebeck` | 301 | `/webentwicklung-luebeck/` | 200 | PASS |
| `ki-automatisierung-luebeck` | 301 | `/ki-automatisierung-luebeck/` | 200 | PASS |
| `en` | 301 | `/en/` | 200 | PASS |
| `impressum` | 301 | `/impressum/` | 200 | PASS |
| `datenschutz` | 301 | `/datenschutz/` | 200 | PASS |

### Public matrix

Direct HTTP GETs, no insecure TLS option, each hop inspected and authority validated before following; maximum five redirects. All final URLs are canonical HTTPS slash URLs, HTTP 200. No internal authority/port, loop or TLS error.

| Start URL | Status | Location | Redirect count | Final URL | Final HTTP | Result |
| --- | ---: | --- | ---: | --- | ---: | --- |
| `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | `—` | 0 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | PASS |
| `https://datenpflege-nord.de/softwareentwicklung-luebeck` | 301 | `/softwareentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | PASS |
| `http://datenpflege-nord.de/softwareentwicklung-luebeck/` | 301 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | PASS |
| `http://datenpflege-nord.de/softwareentwicklung-luebeck` | 301 | `https://datenpflege-nord.de/softwareentwicklung-luebeck` | 2 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | PASS |
| `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | `—` | 0 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | PASS |
| `https://datenpflege-nord.de/webentwicklung-luebeck` | 301 | `/webentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | PASS |
| `http://datenpflege-nord.de/webentwicklung-luebeck/` | 301 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | PASS |
| `http://datenpflege-nord.de/webentwicklung-luebeck` | 301 | `https://datenpflege-nord.de/webentwicklung-luebeck` | 2 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | PASS |
| `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | `—` | 0 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | PASS |
| `https://datenpflege-nord.de/ki-automatisierung-luebeck` | 301 | `/ki-automatisierung-luebeck/` | 1 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | PASS |
| `http://datenpflege-nord.de/ki-automatisierung-luebeck/` | 301 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 1 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | PASS |
| `http://datenpflege-nord.de/ki-automatisierung-luebeck` | 301 | `https://datenpflege-nord.de/ki-automatisierung-luebeck` | 2 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | PASS |
| `https://datenpflege-nord.de/en/` | 200 | `—` | 0 | `https://datenpflege-nord.de/en/` | 200 | PASS |
| `https://datenpflege-nord.de/en` | 301 | `/en/` | 1 | `https://datenpflege-nord.de/en/` | 200 | PASS |
| `http://datenpflege-nord.de/en/` | 301 | `https://datenpflege-nord.de/en/` | 1 | `https://datenpflege-nord.de/en/` | 200 | PASS |
| `http://datenpflege-nord.de/en` | 301 | `https://datenpflege-nord.de/en` | 2 | `https://datenpflege-nord.de/en/` | 200 | PASS |
| `https://datenpflege-nord.de/impressum/` | 200 | `—` | 0 | `https://datenpflege-nord.de/impressum/` | 200 | PASS |
| `https://datenpflege-nord.de/impressum` | 301 | `/impressum/` | 1 | `https://datenpflege-nord.de/impressum/` | 200 | PASS |
| `http://datenpflege-nord.de/impressum/` | 301 | `https://datenpflege-nord.de/impressum/` | 1 | `https://datenpflege-nord.de/impressum/` | 200 | PASS |
| `http://datenpflege-nord.de/impressum` | 301 | `https://datenpflege-nord.de/impressum` | 2 | `https://datenpflege-nord.de/impressum/` | 200 | PASS |
| `https://datenpflege-nord.de/datenschutz/` | 200 | `—` | 0 | `https://datenpflege-nord.de/datenschutz/` | 200 | PASS |
| `https://datenpflege-nord.de/datenschutz` | 301 | `/datenschutz/` | 1 | `https://datenpflege-nord.de/datenschutz/` | 200 | PASS |
| `http://datenpflege-nord.de/datenschutz/` | 301 | `https://datenpflege-nord.de/datenschutz/` | 1 | `https://datenpflege-nord.de/datenschutz/` | 200 | PASS |
| `http://datenpflege-nord.de/datenschutz` | 301 | `https://datenpflege-nord.de/datenschutz` | 2 | `https://datenpflege-nord.de/datenschutz/` | 200 | PASS |

### Regression, logs and rollback

Homepage, all six canonical pages, `/robots.txt`, `/sitemap.xml` and `/healthz`: public HTTP 200 without redirects. Contact Backend `http://127.0.0.1:8091/health`: HTTP 200, `{"ok": true}` before and after. No contact submission sent.

Log baseline at 09:23:56Z, final check at 09:25:03Z: `/var/log/nginx/error.log` inode 19280212, 0 → 0 bytes; `/var/log/nginx/datenpflege-nord.error.log` inode 19280210, 177 → 177 bytes. No rotation and no new log entries. Existing site-log content was not treated as a new regression. Final nginx service `active`.

Rollback ready, not required or executed: restore the byte-verified saved site config with preserved metadata; restore the duplicate enabled state only if required to restore the original state; privileged `nginx -t`; graceful reload only after a successful test; recheck contact health and known slashless origin baseline, then STOP. The saved duplicate remains available outside sites-enabled. The original baseline contains the known duplicate warnings and redirect defect.

### Independent deployment contract and remaining gates

Read-only SHA-256 verification on this server confirms:

- Installed `/usr/local/sbin/dpn-deploy`: `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01`.
- Local unversioned `scripts/dpn-deploy`: `7e818ca2c76a2767a4b3887d0add25df98e66544e42e989fc16f1ee3e097e2e7`.

Per the supplied audited difference, only the ordering of `assets/profile-card.css` and `assets/profile/dustin-zander.webp` differs in the public allowlist. Allowlist membership is identical; no functional deployment difference has been identified from this ordering change because the allowlist is iterated and manifest validation sorts it. The files are not byte-identical. The local copy remains untracked in its operations checkout. Neither file was edited, overwritten or copied over the other.

Issue #15 remains OPEN. A byte-identical runtime baseline is now versioned at `ops/deploy/dpn-deploy`; operational adoption, future cache/freshness controls and authorized dry-run/rollback acceptance remain OPEN. See `P0-DEPLOYMENT-CONTRACT.md` for the current acceptance matrix. No GitHub issue state was modified.

Remaining P0 gates from the evidence pack: main branch protection / required checks (#10); versioned deployment contract (#15); production-versus-reviewed-release parity before deployment; full security/cache-header sign-off. Remaining P1 gates: Search Console index/query/CTR/canonical evidence; fresh Lighthouse/CrUX/CWV; local/business entity validation; business/service-area decisions; deterministic sitemap lastmod; post-release browser and CSP enforcement eligibility. These were not closed by this nginx change.

Raw per-hop HTTP evidence: `ops/evidence/p0-nginx-20260914.json`.

No website deployment performed

No merge to main performed

No Cloudflare configuration changed

No contact backend configuration changed

## Historical pre-remediation evidence

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

## Fresh pre-change public baseline — 2026-09-13T21:33:45+02:00

This recheck was captured before any nginx change. `follow rc=35` denotes the known TLS failure after the chain reaches the exposed origin port.

| Path | Variant | Initial | Location | Redirects | Final effective URL | Final | Follow rc | `:8080` | HTTPS→HTTP |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | --- | --- |
| `softwareentwicklung-luebeck` | `https+slash` | 200 | `—` | 0 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | 0 | no | no |
| `softwareentwicklung-luebeck` | `https-noslash` | 301 | `http://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | 301 | 35 | yes | yes |
| `softwareentwicklung-luebeck` | `http+slash` | 301 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de/softwareentwicklung-luebeck/` | 200 | 0 | no | no |
| `softwareentwicklung-luebeck` | `http-noslash` | 301 | `https://datenpflege-nord.de/softwareentwicklung-luebeck` | 2 | `https://datenpflege-nord.de:8080/softwareentwicklung-luebeck/` | 301 | 35 | yes | no |
| `webentwicklung-luebeck` | `https+slash` | 200 | `—` | 0 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | 0 | no | no |
| `webentwicklung-luebeck` | `https-noslash` | 301 | `http://datenpflege-nord.de:8080/webentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de:8080/webentwicklung-luebeck/` | 301 | 35 | yes | yes |
| `webentwicklung-luebeck` | `http+slash` | 301 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 1 | `https://datenpflege-nord.de/webentwicklung-luebeck/` | 200 | 0 | no | no |
| `webentwicklung-luebeck` | `http-noslash` | 301 | `https://datenpflege-nord.de/webentwicklung-luebeck` | 2 | `https://datenpflege-nord.de:8080/webentwicklung-luebeck/` | 301 | 35 | yes | no |
| `ki-automatisierung-luebeck` | `https+slash` | 200 | `—` | 0 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | 0 | no | no |
| `ki-automatisierung-luebeck` | `https-noslash` | 301 | `http://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | 1 | `https://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | 301 | 35 | yes | yes |
| `ki-automatisierung-luebeck` | `http+slash` | 301 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 1 | `https://datenpflege-nord.de/ki-automatisierung-luebeck/` | 200 | 0 | no | no |
| `ki-automatisierung-luebeck` | `http-noslash` | 301 | `https://datenpflege-nord.de/ki-automatisierung-luebeck` | 2 | `https://datenpflege-nord.de:8080/ki-automatisierung-luebeck/` | 301 | 35 | yes | no |
| `en` | `https+slash` | 200 | `—` | 0 | `https://datenpflege-nord.de/en/` | 200 | 0 | no | no |
| `en` | `https-noslash` | 301 | `http://datenpflege-nord.de:8080/en/` | 1 | `https://datenpflege-nord.de:8080/en/` | 301 | 35 | yes | yes |
| `en` | `http+slash` | 301 | `https://datenpflege-nord.de/en/` | 1 | `https://datenpflege-nord.de/en/` | 200 | 0 | no | no |
| `en` | `http-noslash` | 301 | `https://datenpflege-nord.de/en` | 2 | `https://datenpflege-nord.de:8080/en/` | 301 | 35 | yes | no |
| `impressum` | `https+slash` | 200 | `—` | 0 | `https://datenpflege-nord.de/impressum/` | 200 | 0 | no | no |
| `impressum` | `https-noslash` | 301 | `http://datenpflege-nord.de:8080/impressum/` | 1 | `https://datenpflege-nord.de:8080/impressum/` | 301 | 35 | yes | yes |
| `impressum` | `http+slash` | 301 | `https://datenpflege-nord.de/impressum/` | 1 | `https://datenpflege-nord.de/impressum/` | 200 | 0 | no | no |
| `impressum` | `http-noslash` | 301 | `https://datenpflege-nord.de/impressum` | 2 | `https://datenpflege-nord.de:8080/impressum/` | 301 | 35 | yes | no |
| `datenschutz` | `https+slash` | 200 | `—` | 0 | `https://datenpflege-nord.de/datenschutz/` | 200 | 0 | no | no |
| `datenschutz` | `https-noslash` | 301 | `http://datenpflege-nord.de:8080/datenschutz/` | 1 | `https://datenpflege-nord.de:8080/datenschutz/` | 301 | 35 | yes | yes |
| `datenschutz` | `http+slash` | 301 | `https://datenpflege-nord.de/datenschutz/` | 1 | `https://datenpflege-nord.de/datenschutz/` | 200 | 0 | no | no |
| `datenschutz` | `http-noslash` | 301 | `https://datenpflege-nord.de/datenschutz` | 2 | `https://datenpflege-nord.de:8080/datenschutz/` | 301 | 35 | yes | no |

Fresh baseline result: canonical HTTPS slash URLs pass for all six paths; every HTTPS slashless URL fails the invariant by exposing `http://datenpflege-nord.de:8080/.../`. HTTP slashless requests also fail after the HTTPS hop reaches the same origin-port redirect defect.

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
