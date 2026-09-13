# P0 Redirect Remediation Design

Status: design only. **No production configuration change has been applied.**

## Proven cause

The canonical nginx server for `datenpflege-nord.de` listens on plain HTTP at `127.0.0.1:8080` behind Cloudflare Tunnel. Static directory routes are resolved through `try_files $uri $uri/ $uri.html =404`. For a real directory requested without its trailing slash, nginx generates the slash-normalization redirect using the origin scheme and listen port. The resulting Location is `http://datenpflege-nord.de:8080/<path>/`.

Direct origin tests reproduce the defect even when standard `X-Forwarded-Proto`, `X-Forwarded-Port`, and `X-Forwarded-Host` headers are supplied, so the current static redirect path does not derive its public redirect from those headers.

## Minimal proposed change

Scope the correction to the canonical `server_name datenpflege-nord.de` server in `/etc/nginx/sites-available/datenpflege-nord.conf`.

Preferred minimal change to validate in a staged copy:

```nginx
server {
    listen 127.0.0.1:8080;
    server_name datenpflege-nord.de;
    absolute_redirect off;
    # existing configuration follows
}
```

This makes nginx-generated redirects relative, so a request that arrived publicly as HTTPS remains on the public HTTPS authority and cannot leak the origin `http` scheme or `:8080` port. The explicit `www` canonicalization block already returns `https://datenpflege-nord.de$request_uri` and should remain explicit.

`port_in_redirect off` alone is not sufficient: it could remove `:8080` while still emitting the origin `http` scheme. No global nginx change is proposed.

## Configuration ownership

The active file is `/etc/nginx/sites-available/datenpflege-nord.conf`, enabled via `/etc/nginx/sites-enabled/datenpflege-nord.conf` symlink. Infrastructure configuration is not currently proven to be version-controlled by the production repository. The locally visible `scripts/dpn-deploy` and `tests/test_dpn_deploy.py` in the older operations checkout are untracked files.

Before applying the fix, version the reviewed nginx site definition in an operations-controlled path, preferably a dedicated infrastructure repository. If kept with this repository, use a non-public path such as `infra/nginx/datenpflege-nord.conf`; the deployment allowlist must continue to exclude it from the webroot.

## Dry-run and regression test

Before any reload:

1. Copy the active site definition to a root-owned staged file.
2. Add only the scoped `absolute_redirect off;` change.
3. Validate syntax with `nginx -t` against the intended configuration.
4. Review the complete diff; no unrelated directive may change.
5. After an explicitly approved reload, test direct origin and public edge matrices separately.

Required post-change matrix for each canonical subpage:

| Request | Expected |
| --- | --- |
| `https://datenpflege-nord.de/path/` | 200 |
| `https://datenpflege-nord.de/path` | bounded redirect to `https://datenpflege-nord.de/path/`, then 200; no `:8080` |
| `http://datenpflege-nord.de/path/` | bounded redirect to HTTPS slash URL, then 200 |
| `http://datenpflege-nord.de/path` | bounded redirects to HTTPS slash URL, then 200; no `:8080` |
| `https://www.datenpflege-nord.de/path` | bounded redirects to canonical host + HTTPS + slash, then 200 |

Also verify `/`, static assets, `/api/contact` routing, 404 behavior, cache/security headers and Cloudflare-served semantics.

## Regression risks

- Other nginx-generated redirects in the canonical server become relative; enumerate them during staging.
- Cloudflare edge rules may add a preceding HTTP-to-HTTPS hop; the final public invariant still must hold.
- Do not alter the `/api/contact` proxy or its backend headers while fixing static redirect behavior.
- Do not introduce an extra redirect loop between Cloudflare and nginx.

## Rollback

Rollback is configuration-level and independent of the static-site release symlink:

1. Preserve a byte-identifiable pre-change nginx site file.
2. If post-reload verification fails, restore that exact reviewed file.
3. Run nginx syntax validation.
4. Reload nginx only after validation.
5. Re-run origin and public redirect matrices to prove restoration.

The static content deployment rollback mechanism must not be used as a substitute for nginx configuration rollback because the defect is outside the release content.

## Cloudflare considerations

Cloudflare is an edge participant, not the proven origin of this defect. Keep public HTTP-to-HTTPS behavior intact. Do not add a compensating Cloudflare redirect rule before the origin fix is reviewed; that would hide the origin contract defect and create two sources of redirect truth.
