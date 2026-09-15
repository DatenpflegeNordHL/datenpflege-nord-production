# DatenpflegeNord Golden agent routing

This repository is evidence-gated. Keep this file short; detailed truth lives under `docs/golden/`.

## Read first

1. `docs/golden/CURRENT-STATE.md`
2. `docs/golden/BUSINESS-TRUTH.md`
3. `docs/golden/SEARCH-OWNERSHIP.md`
4. `docs/golden/RELEASE-RULES.md`
5. `docs/golden/AUTHORITY-RULES.md`
6. `docs/golden/GSC-READINESS.md` when search measurement or expansion is involved

Use the linked legacy evidence files for detail. Do not create a second source of truth for the same fact.

## Hard rules

- Public brand: `DatenpflegeNord / Datenpflege Nord`.
- Current legal organization: `Green Vector Energo GmbH`, Amtsgericht Lübeck HRB 25869 HL.
- Verified service area: Lübeck + Schleswig-Holstein.
- Issue #13 remains the entity gate. Do not claim `NordWerk Digital GmbH` is registered without independent evidence.
- Do not invent customers, cases, reviews, certifications, memberships, offices, services or outcomes.
- Do not add a page because a keyword exists. One intent cluster has one primary owner.
- Prefer strengthening an existing owner over creating another URL. Current HOLD/REJECT decisions are in `docs/golden/SEARCH-OWNERSHIP.md`.
- Repository truth -> CI truth -> preview truth -> approved release package -> production truth.
- Exact-SHA CI matters. Older green CI does not validate a newer HEAD.

## Normal failure policy

For tests, links, schema, asset versions, browser QA, formatting or documentation conflicts: diagnose, minimally repair, rerun the failed gate, then continue. Never weaken a test merely to obtain PASS.

## Human gates

Stop only for credentials/login, DNS ownership, paid membership/purchase, customer permission, legal/entity decisions, production deployment, merge to `main`, signing/private secrets, or destructive/irreversible actions. Record the smallest required human action and continue unrelated safe work.

## Validation

Use `docs/golden/runbooks/SITE-AUDIT.md` for normal repository changes and `docs/golden/runbooks/RELEASE-VERIFICATION.md` when public release contents change. At minimum for relevant changes:

```bash
git diff --check
python3 scripts/site_audit.py
python3 scripts/golden_audit.py
python3 ops/deploy/check_asset_versions.py --root .
python3 ops/deploy/scan_secrets.py
python3 -m unittest discover -s tests
```

User-facing changes also require browser QA at 1440, 390 and 320 px. Release-content changes require exact-archive verification and Hosted CI on the exact final code SHA.

## Production boundary

No deployment, merge to `main`, production nginx/Cloudflare/systemd change, or Issue #10/#15 activation without explicit authorization.
