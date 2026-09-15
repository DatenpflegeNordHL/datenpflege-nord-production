# Verified public OSS proof

Verified through the GitHub API on 2026-09-15. These are public pull requests authored by `DatenpflegeNordHL` with a non-null upstream `merged_at`. They may be described as merged OSS contributions; do not infer adoption, business impact or customer outcomes.

| Upstream project | Pull request | Merged at | Verified contribution |
| --- | --- | --- | --- |
| open-jarvis/OpenJarvis | https://github.com/open-jarvis/OpenJarvis/pull/708 | 2026-08-10T23:32:15Z | preserve Gemini tool calls while streaming |
| open-jarvis/OpenJarvis | https://github.com/open-jarvis/OpenJarvis/pull/921 | 2026-09-04T20:25:03Z | keep desktop install working on Python 3.10 |
| open-jarvis/OpenJarvis | https://github.com/open-jarvis/OpenJarvis/pull/936 | 2026-09-04T20:25:13Z | resolve MLX model IDs before inference |
| ccfos/nightingale | https://github.com/ccfos/nightingale/pull/3367 | 2026-09-04T07:38:36Z | use configured PostgreSQL database in `InitClient` |
| blacklanternsecurity/bbot | https://github.com/blacklanternsecurity/bbot/pull/3415 | 2026-08-31T20:21:58Z | clarify Version Updater workflow name |

Verification method for future additions:

```bash
gh api repos/OWNER/REPO/pulls/NUMBER --jq '{author:.user.login,state,merged_at,html_url,title}'
```

Only add a row when `author` is the expected public account and `merged_at` is present.
