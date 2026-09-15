# Google Search Console readiness

Detailed measurement and decision workflow: `../../GSC-VALIDATION-PLAN.md`.

## Prepared property data

- Canonical domain: `https://datenpflege-nord.de/`
- Preferred domain property: `datenpflege-nord.de`
- Sitemap: `https://datenpflege-nord.de/sitemap.xml`
- Do not use unrelated `datenpflegenord.de`.

## Initial URL inspection set

1. `https://datenpflege-nord.de/`
2. `https://datenpflege-nord.de/softwareentwicklung-luebeck/`
3. `https://datenpflege-nord.de/webentwicklung-luebeck/`
4. `https://datenpflege-nord.de/ki-automatisierung-luebeck/`
5. `https://datenpflege-nord.de/wissen/individualsoftware-kosten/`
6. `https://datenpflege-nord.de/wissen/website-relaunch-checkliste/`
7. `https://datenpflege-nord.de/wissen/ki-prozessautomatisierung/`

Use the same seven owners as the post-release inspection set, adding any actually changed canonical URL from that release.

## HUMAN ACTION REQUIRED

In Google Search Console, check whether a `datenpflege-nord.de` Domain property already exists. If not, start Domain-property verification and add Google's exact TXT record through the authorized DNS account. Then submit `https://datenpflege-nord.de/sitemap.xml` and inspect the seven URLs above. Do not invent or commit a verification token.

After access exists, use the query/page template in `../../GSC-VALIDATION-PLAN.md`; do not create new owners from third-party volume while first-party query evidence is unavailable.
