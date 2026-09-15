# Golden source-of-truth index

This directory is the persistent routing layer for future Golden work. It summarizes durable facts and points to the detailed evidence already maintained in the repository.

| Topic | Canonical routing document | Detailed evidence |
| --- | --- | --- |
| Business/legal/service truth | `BUSINESS-TRUTH.md` | `../../MASTER-SITE-EVIDENCE.md`, `../../AUTHORITY-ENTITY-MAP.md` |
| Current frozen/release state | `CURRENT-STATE.md` | `../../VISIBILITY-PHASE-7-REPORT.md`, `../../GOLDEN-VALIDATION-REPORT.md` |
| Query/URL ownership | `SEARCH-OWNERSHIP.md` | `../../GOLDEN-CONTENT-OWNERSHIP-MAP.md`, `../../KEYWORD-INTENT-MAP.md` |
| Release and exact-SHA rules | `RELEASE-RULES.md` | `../../ops/deploy/RELEASE-RUNBOOK.md`, `../../P0-DEPLOYMENT-CONTRACT.md` |
| Authority safety/execution | `AUTHORITY-RULES.md` | `../../AUTHORITY-ACQUISITION-PHASE-7.md`, `AUTHORITY-EXECUTION-QUEUE.md` |
| Search Console readiness | `GSC-READINESS.md` | `../../GSC-VALIDATION-PLAN.md` |
| Verifiable OSS proof | `OSS-PROOF.md` | linked upstream pull requests |
| Reusable workflows | `runbooks/` | repository scripts/tests |

When facts disagree, stop and reconcile the conflict against the strongest current evidence instead of silently copying both versions.
