# Runbook: exact-SHA release verification

Use only after public release contents change. This runbook validates source; it does not authorize deployment.

1. Finalize assets and require an idempotent second generator pass.
2. Run the full Golden site audit.
3. Commit the code/release-content change.
4. Verify the exact archive:

```bash
python3 ops/deploy/verify_release_candidate.py --repo . --commit <full-sha>
```

5. Push the feature branch and dispatch `.github/workflows/site-audit.yml` on that branch.
6. Verify the resulting run's workflow path, branch, `head_sha == <full-sha>` and `conclusion == success`.

If later documentation changes create a new branch HEAD, follow the repository's exact-SHA policy for that final HEAD. Never deploy or merge merely because these checks pass.
