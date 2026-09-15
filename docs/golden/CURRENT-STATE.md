# Current Golden state

Last reconciled: 2026-09-15.

## Trusted baseline

- Frozen Phase-7 branch: `golden-visibility-phase-7-authority`
- Frozen Phase-7 SHA: `55b4167d68e37341f4ac56dd864734424cc4c51b`
- Exact-SHA Hosted CI run: `35000268647`
- CI head SHA: `55b4167d68e37341f4ac56dd864734424cc4c51b`
- CI conclusion: `success`
- Authority Execution Phase 1 branch: `golden-authority-execution-phase-1`

Do not rewrite Phase-7 work merely for freshness or style. Change frozen content only for independently demonstrated defects or evidence-backed improvements in a later goal.

## Site architecture

The static audit currently expects 10 canonical HTML pages. Search ownership for the commercial and authority pages is defined in `SEARCH-OWNERSHIP.md`. Legal and language-support pages remain part of the canonical set but do not own acquisition clusters.

## Open gates

- Issue #13: **OPEN** — legal/entity reconciliation before broad company-profile activation.
- Issue #10: **parked for this goal** — do not activate production release-control work.
- Issue #15: **parked for this goal** — do not activate production freshness work.
- Google Search Console: first-party data/access gap; repo-side readiness is documented in `GSC-READINESS.md`.

## Production truth

Repository work and Hosted CI do not prove a production release. Production deployment, `main` merge, nginx, Cloudflare and systemd changes require a separate explicit authorization.

Detailed Phase-7 evidence: `../../VISIBILITY-PHASE-7-REPORT.md`.
