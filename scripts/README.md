# Static site audit

Run the deterministic repository checks locally with:

```bash
python scripts/site_audit.py
```

The audit intentionally checks only facts that can be verified from the repository. It does not assign SEO scores or guess at search-engine rankings.

It currently verifies:

- one `h1`, a title, meta description, language and canonical URL per HTML page
- unique page titles, canonical URLs and element IDs
- JSON-LD syntax
- `alt` attributes on images
- accessible names for form controls
- `rel="noopener"` on links that open a new tab
- internal file links and URL fragments
- consistency between canonical pages and `sitemap.xml`
- the sitemap declaration in `robots.txt`

The corresponding GitHub Actions workflow uses read-only repository permissions and runs for pull requests targeting `main`.
