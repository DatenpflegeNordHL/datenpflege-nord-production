# P0 Sanitized Deployment Contract

Current update — 2026-09-14: privileged read-only hash verification confirms installed dpn-deploy SHA-256 `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01` and local untracked copy SHA-256 `7e818ca2c76a2767a4b3887d0add25df98e66544e42e989fc16f1ee3e097e2e7`. The files are not byte-identical. The only known difference is ordering of `assets/profile-card.css` and `assets/profile/dustin-zander.webp` in the public allowlist. Allowlist membership is identical; no functional deployment difference has been identified from this ordering change because the allowlist is iterated and manifest validation sorts it. Neither file was modified or overwritten. **Issue #15 remains OPEN: canonical versioned dpn-deploy source of truth is still required.** The separately authorized nginx remediation passed; see `P0-REDIRECT-EVIDENCE.md`. Read-only/no-reload and unproven-hash statements below are historical observations from 2026-09-13.

Historical capture status (2026-09-13): read-only contract capture. No production deployment, nginx reload/restart, webroot replacement, deploy-script edit, Cloudflare change, backend change or main merge was performed.

## Contract chain

`Repository Truth -> Release Artifact -> Server Transfer -> Activation -> Public Webroot -> CDN -> Live Verification -> Rollback`

### 1. Repository Truth

- Repository remote named by the deploy implementation: `git@github.com:DatenpflegeNordHL/datenpflege-nord-production.git`.
- The deploy logic fetches `main` into a root-owned bare cache at `/var/lib/dpn-deploy/repo.git` and requires the supplied 40-character target SHA to equal fetched `origin/main`.
- It does not deploy from the user's working tree.
- Current Phase 1–3 feature commit `f4dde6e345edb6cf78c071a41695cfbd42827320` is therefore not deployable by contract until it is legitimately merged to `main`.

### 2. Release Artifact

The deploy logic uses a closed `ALLOWED_PUBLIC_FILES` list. It creates a release by `git archive` of only selected public files into a new directory under `/srv/datenpflege-nord/releases/`.

Validation requires:

- required HTML/robots/sitemap files exist and are non-empty;
- actual release files equal the selected allowlist exactly;
- every release file hashes to the Git blob from the target commit;
- local HTML/CSS references resolve inside the release manifest;
- suspicious secret-like files (`.env`, key/certificate containers, secret/credential/password names) are rejected;
- symlinks inside the GitHub release are rejected;
- baseline HTML/title/H1 and service sitemap checks pass.

### 3. Server Transfer / source path

There is no rsync/copy from a developer checkout in the inspected deployment design. The server fetches GitHub into the root-owned bare cache and materializes the target through `git archive`.

Sensitive boundaries observed without reading secret values:

- `/etc/dpn-deploy/` is root-owned mode 700.
- Deploy SSH identity path referenced by the implementation: `/etc/dpn-deploy/id_ed25519`.
- Known-hosts path: `/etc/dpn-deploy/known_hosts`.
- `/var/lib/dpn-deploy/` is root-owned mode 700 and stores cache/state/locks/release metadata.
- Cloudflared reads its token from `/etc/cloudflared/token`, root-owned mode 600. Token content was not read.
- Contact backend environment is `/etc/datenpflege-nord-contact.env`, root-owned mode 600. Values were not read.

### 4. Activation and public webroot

- Release root: `/srv/datenpflege-nord/releases` (`root:root`, mode 755).
- Public pointer: `/srv/datenpflege-nord/current` is a root-owned symlink.
- Observed current target: `/srv/datenpflege-nord/releases/20260908-080736-git-65468e875fa0.DM1912`.
- The release name resolves to repository commit `65468e875fa0f4318cc07d7e4cbe843cacb24569` (`fix: refresh WhatsApp/Open Graph preview`).
- Activation is atomic at filesystem level: create `current.new` symlink, then `mv -Tf` over `current`.
- Observed release and sample public files are `root:root`; sample HTML/sitemap file mode is 664.
- nginx serves `root /srv/datenpflege-nord/current` from `127.0.0.1:8080`.

### 5. Contact backend separation

The static release does not deploy the contact backend.

- nginx routes only `/api/contact` to `http://127.0.0.1:8091`.
- `dpn-contact.service` runs separately as `www-data:www-data` from `/opt/dpn-contact/contact_api.py`.
- Backend environment values live outside the webroot in `/etc/datenpflege-nord-contact.env` (root mode 600).
- The deploy script health-checks `dpn-contact` and `127.0.0.1:8091/health`, but the backend executable/configuration is not part of the public-file archive.

### 6. CDN / origin relationship

- nginx listens locally on `127.0.0.1:8080`; the contact backend listens on `127.0.0.1:8091`.
- `cloudflared.service` uses a root-only token file and has no local plaintext tunnel configuration containing the public mapping; routing is therefore at least partly remotely managed.
- Public site responses expose `Server: cloudflare`.
- Direct origin testing on `127.0.0.1:8080` reproduces the defective no-slash redirect seen publicly, proving nginx is the redirect source while Cloudflare is the public delivery path.
- Cloudflare transforms some live output, so CDN HTML byte identity is not a valid sole release-identity check.

### 7. Live verification

The deploy implementation checks active `nginx`, `dpn-contact`, and `cloudflared`, validates the contact health endpoint, probes the local nginx origin with `Host: datenpflege-nord.de`, probes selected public HTTPS URLs, and verifies target/release state around activation.

Production Truth must use layered evidence:

1. **Artifact manifest:** target commit plus allowlisted Git blob identities.
2. **Server-side deployed manifest:** release directory, release metadata and selected file hashes/blobs checked before activation.
3. **Semantic HTTP checks:** status, canonical, robots, sitemap, metadata/schema, body markers, redirect matrix, headers and assets.
4. **Expected CDN transformations:** explicitly account for Cloudflare robots augmentation, email obfuscation/decoder injection and other known transformations.
5. **Browser functional checks:** responsive rendering, navigation, JavaScript/resource errors, contact-path acceptance and CWV/real-user evidence where applicable.

Cloudflare-served HTML is not required to be byte-identical to origin HTML when the transformation is expected and documented.

### 8. Rollback

The static deploy script stores the previous live release/SHA before switching. If validation or the live smoke test fails after switching, cleanup attempts to:

- atomically restore `/srv/datenpflege-nord/current` to the previous release;
- restore the prior deployed SHA state when valid;
- remove a newly created failed release and its state file when it is not active.

`deployed_sha` is written only after the final live smoke test and cross-checks succeed, making it the final transaction marker.

The nginx redirect defect requires a separate configuration rollback plan; the static release symlink cannot roll back nginx configuration.

## dpn-deploy identity and metadata

Installed executable metadata observed:

- path: `/usr/local/sbin/dpn-deploy`
- owner/group: `root:root`
- mode: `750`
- size: `17000` bytes
- mtime: `2026-08-26 19:43:56.669844501 +0200`

Read-only verification on 2026-09-14 confirmed installed executable SHA-256 `d853a8c32c0179b70705d7ea307a038d7f0bc0f23adc4c961f13c193880cec01`. The 2026-09-13 non-interactive sudo authentication failure was a historical evidence limitation; the installed-hash gap is now resolved.

The local operations-checkout candidate at `/home/adminzander/projekte/datenpflege-nord-production/scripts/dpn-deploy` remains **untracked**, with SHA-256 `7e818ca2c76a2767a4b3887d0add25df98e66544e42e989fc16f1ee3e097e2e7`. It is not byte-identical to the installed executable. The supplied audited difference is solely the ordering of `assets/profile-card.css` and `assets/profile/dustin-zander.webp`; allowlist membership is identical and no functional deployment difference has been identified from this ordering change. Neither file was overwritten.

**Issue #15: OPEN.** The canonical version-controlled dpn-deploy source of truth remains unresolved; recording hashes and the known ordering difference does not close the deployment contract or authorize a website deployment.

## Main protection gate

**Issue #10: OPEN.** This evidence finalization does not change repository protection.

GitHub currently reports `main` as unprotected. Branch-protection and repository-ruleset API requests return HTTP 403 with GitHub's explicit limitation: upgrade the account/plan or make the repository public to enable the feature. Making a production repository public is not an acceptable automatic workaround.

A push-triggered audit is not preventive branch protection. Until proper protection is available, the best enforceable fallback is operational only: PR-only policy, required human review, hosted CI evidence tied to exact SHA, no direct-main pushes, and production deployment requiring an explicitly approved main SHA. This remains a P0 blocker because ordinary direct pushes are not technically prevented by GitHub.
