# Static site audit

Run the deterministic repository checks locally with:

```bash
python scripts/site_audit.py
```

The audit intentionally checks only facts that can be verified from the repository. It does not assign SEO scores or guess at search-engine rankings.

It currently verifies:

- exactly one `h1`, meta description and canonical URL per HTML page
- a page title and language declaration per HTML page
- unique page titles, canonical URLs and element IDs across the static site
- JSON-LD syntax
- `alt` attributes on images
- explicit accessible names for form controls; project policy requires an `id` + associated label or an ARIA name
- `rel="noopener"` on links that open a new tab
- internal page links and URL fragments
- existence of local HTML resources referenced by images, scripts, video posters/sources and relevant `<link>` elements
- consistency between canonical pages and `sitemap.xml`
- the sitemap declaration in `robots.txt`

The corresponding GitHub Actions workflow:

- runs for pull requests targeting `main`
- has read-only repository permissions
- pins third-party GitHub Actions to full commit SHAs
- does not persist checkout credentials after the repository has been fetched
