# Golden release rules

Detailed deployment mechanics live in `../../ops/deploy/RELEASE-RUNBOOK.md`, `../../P0-DEPLOYMENT-CONTRACT.md` and `../../RELEASE-VERIFICATION.md`.

## Trust chain

Repository truth -> CI truth -> preview truth -> approved release package -> production truth.

Never use an older green CI run as proof for a newer commit. A code-changing final commit requires Hosted CI whose `head_sha` equals that exact commit. If a later documentation-only commit becomes branch HEAD, validate the final HEAD according to the repository's current exact-SHA policy.

## Mandatory local gates when applicable

```bash
git diff --check
python3 scripts/site_audit.py
python3 scripts/golden_audit.py
python3 ops/deploy/check_asset_versions.py --root .
python3 ops/deploy/scan_secrets.py
python3 -m unittest discover -s tests
bash -n ops/deploy/dpn-deploy
node --check assets/home-de.js
node --check assets/home-en.js
node --check assets/service.js
node --check assets/authority.js
```

If a leaf asset changed, run the asset generator, then rerun it and require zero second-pass changes. If public release contents changed, run:

```bash
python3 ops/deploy/verify_release_candidate.py --repo . --commit <full-commit-sha>
```

User-facing changes require real browser QA at 1440, 390 and 320 px, keyboard focus, no-JS readability where relevant and reduced-motion behavior.

## Hard boundary

No production deployment, merge to `main`, release-script installation, `/srv/datenpflege-nord/current` change, production nginx/Cloudflare/systemd change, or Issue #10/#15 activation without explicit authorization.
