# Runbook: Golden site audit

Use after repository/site changes that do not require production access.

```bash
git diff --check
python3 scripts/site_audit.py
python3 scripts/golden_audit.py
python3 ops/deploy/check_asset_versions.py --root .
python3 ops/deploy/scan_secrets.py
python3 -m unittest discover -s tests
```

For changed JS/shell/YAML, run the relevant syntax/parser checks. For changed user-facing HTML/CSS/JS, run browser QA at 1440/390/320 plus keyboard focus, reduced motion and no-JS readability where applicable.

On failure: diagnose, minimally fix, rerun the failing gate and the gates affected by the repair. Do not weaken validation.
