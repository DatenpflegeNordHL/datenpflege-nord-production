# GOLDEN RELEASE VERIFICATION — DatenpflegeNord

Status: mandatory production evidence runbook
Last checked: 2026-09-10
Canonical repository: `DatenpflegeNordHL/datenpflege-nord-production`
Canonical domain: `https://datenpflege-nord.de/`

This runbook is evidence collection, not a deployment script. Do not paste secrets, environment-file contents, private keys, API tokens or full sensitive server configuration into issues, pull requests or chat transcripts.

## 1. Release identity

Before deployment record:

```bash
git status --short
git rev-parse HEAD
git log -1 --format='%H %cI %s'
```

Acceptance:
- working tree clean;
- SHA equals the reviewed release commit;
- all required PR/CI gates are green.

## 2. Production deploy implementation

The current repository references `/usr/local/sbin/dpn-deploy`, but the implementation is not versioned here. Collect locally on the server:

```bash
sudo stat -c '%U:%G %a %n' /usr/local/sbin/dpn-deploy
sudo sha256sum /usr/local/sbin/dpn-deploy
```

Review the script locally and record a sanitized deployment contract containing:
- source checkout/release path;
- destination webroot;
- include/exclude rules;
- ownership and mode changes;
- atomic/symlink/copy strategy;
- rollback target;
- logging/failure behavior.

Required exclusion checks must cover at least `.git`, `.github`, `tests`, internal Markdown evidence/docs where not intentionally public, backend source/units where not intentionally public, environment files and secrets.

Do not publish the script itself if it embeds infrastructure secrets.

## 3. Pre-deploy nginx evidence

Inspect nginx locally. Avoid posting the entire configuration if unrelated virtual hosts or credentials are present.

Useful local commands:

```bash
sudo nginx -t
sudo nginx -T 2>&1 | grep -nE 'server_name|location = /api/contact|proxy_pass|proxy_set_header|client_max_body_size|proxy_(connect|read|send)_timeout|add_header'
```

For the contact route verify:
- exact public route `/api/contact`;
- loopback proxy target `127.0.0.1:8091`;
- deterministic client-IP header behavior (`X-Real-IP` and/or explicitly trusted Cloudflare handling);
- request body limit no larger than the application contract unless intentionally documented;
- bounded proxy timeouts;
- no accidental proxying of arbitrary paths to the backend.

For static delivery verify current header policy for:
- Content-Security-Policy or Report-Only state;
- Strict-Transport-Security;
- X-Content-Type-Options;
- Referrer-Policy;
- Permissions-Policy where configured;
- caching of immutable assets versus HTML.

## 4. Contact backend pre-deploy evidence

Do not print `/etc/datenpflege-nord-contact.env`.

```bash
sudo stat -c '%U:%G %a %n' /etc/datenpflege-nord-contact.env
sudo systemctl cat dpn-contact.service
sudo systemctl is-active dpn-contact.service
sudo systemctl is-enabled dpn-contact.service
sudo systemd-analyze verify /etc/systemd/system/dpn-contact.service
sudo systemd-analyze security dpn-contact.service --no-pager
sudo sha256sum /opt/dpn-contact/contact_api.py
curl -fsS --max-time 3 http://127.0.0.1:8091/health
```

Acceptance before replacing backend artifacts:
- secret file remains root-owned and mode `0600` or stricter equivalent;
- backend binds loopback only;
- service unit matches the reviewed release target;
- health endpoint succeeds locally;
- current production hash is recorded for rollback comparison.

A real contact-form mail submission is a separate explicitly approved delivery test because it creates external email traffic.

## 5. Dry-run / staged file comparison

Before modifying the live webroot, obtain a deployment dry-run or compare the release tree with a staging directory using the actual include/exclude contract.

Acceptance:
- no secret/internal files enter the public tree;
- all seven canonical routes and required assets are present;
- deleted/template assets intended for removal do not survive by accident;
- file ownership/modes remain compatible with read-only web serving.

## 6. Post-deploy HTTP verification

Run from a resolver/network outside the origin server when possible:

```bash
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/softwareentwicklung-luebeck/
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/webentwicklung-luebeck/
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/ki-automatisierung-luebeck/
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/en/
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/impressum/
curl -fsS -o /dev/null -D - https://datenpflege-nord.de/datenschutz/
curl -fsS https://datenpflege-nord.de/robots.txt
curl -fsS https://datenpflege-nord.de/sitemap.xml
```

Record status codes, redirect chain and relevant security/cache headers. Verify canonical host behavior for `www` and HTTP variants without creating redirect loops.

## 7. Production HTML parity

For each canonical route verify after deployment:
- title and meta description;
- canonical URL;
- robots directive;
- hreflang on DE/EN homepage pair;
- one H1;
- JSON-LD parses;
- internal links/assets resolve;
- removed template client-logo belt is absent after its approved cleanup release;
- static GitHub fallback contains only verified statuses/dates after its approved cleanup release.

Where practical, compare hashes of deterministic static assets between reviewed release and public production. Dynamic edge rewriting/cache-busting must be documented before treating a hash mismatch as failure.

## 8. Browser acceptance pass

Required before CSP enforcement and final release sign-off:
- desktop and mobile widths;
- keyboard navigation/focus;
- contact-form client validation;
- contact API error/success UI without sending real mail unless separately approved;
- GitHub live-data success and fallback behavior;
- reduced-motion mode;
- hero behavior on fine pointer and touch/coarse pointer;
- browser console and network errors;
- CSP Report-Only violations.

Only change CSP from Report-Only to enforcing after this pass is clean against the exact deployed release.

## 9. Performance evidence

Capture a fresh post-deploy lab run and, when available, field data. Record at minimum:
- LCP;
- INP or available interaction proxy;
- CLS;
- TTFB;
- transferred bytes/request count for initial mobile load;
- whether the hero video is fetched on mobile/coarse pointer despite the intended gating.

Do not mark Core Web Vitals passed from repository asset sizes alone.

## 10. Search/index evidence

After production verification:
- submit/verify sitemap in Google Search Console;
- inspect homepage and three primary service URLs;
- record index status and Google-selected canonical;
- record initial query/page impressions, positions and CTR as the post-release baseline;
- watch brand variants carefully because `datenpflegenord.de` is a different entity/domain.

Do not request mass indexing of thin/new URLs that have not passed the keyword/intent gate.

## 11. Release record

A Golden release record must contain:
- reviewed commit SHA;
- deployment timestamp/timezone;
- deploy-contract hash/version;
- previous rollback target;
- CI run/result;
- production parity result;
- nginx/header result;
- backend health/service result where backend changed;
- browser/CSP result;
- performance result;
- Search Console verification status;
- unresolved exceptions with owner and reason.

A release is not `Golden` merely because the files copied successfully. It is Golden only when repository truth, deployment truth and public production truth agree.
