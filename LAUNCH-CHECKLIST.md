# Launch Checklist

Use this before and after the first public release of `wuwabanners.net`.

## Before launch

1. Point the domain to the hosting platform and confirm both:
   - `https://wuwabanners.net/`
   - `https://www.wuwabanners.net/` or your chosen redirect target
2. Force HTTPS.
3. Upload the full site root as static files.
4. Confirm these files are reachable:
   - `/robots.txt`
   - `/sitemap.xml`
   - `/favicon.svg`
   - `/404.html`
5. Make sure the host serves `404.html` with a real `404` HTTP status.
   - The file alone is not enough.
   - This must be configured at the host level if required by the platform.
6. Rebuild once more before upload:

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/build_banner_snapshot.py
```

## Release-day checks

Open these URLs on desktop and mobile:

- `/`
- `/wuthering-waves-next-banner/`
- `/wuthering-waves-current-banner/`
- `/wuthering-waves-banner-history/`
- `/wuthering-waves-banner-countdown/`
- `/wuthering-waves-next-rerun/`
- `/pull-advice/`
- one current character page
- one next character page
- one broken URL to trigger the 404 page

Check for:

- no broken layout
- no missing CSS
- no obviously stale dates
- working internal links
- visible page titles and intro answers above the fold

## Search Console setup

1. Add the property in Google Search Console.
2. Submit:
   - `https://wuwabanners.net/sitemap.xml`
3. Request indexing for:
   - homepage
   - next banner page
   - current banner page
   - pull advice hub
4. Check that Google can fetch:
   - `robots.txt`
   - `sitemap.xml`

## First 7 days

Watch these reports in Search Console:

- Pages indexing
- Sitemaps
- Enhancements / structured data warnings
- Performance

What to look for:

- homepage gets discovered quickly
- `next banner` and `current banner` enter the crawl queue first
- character pull pages start getting discovered from `pull-advice/`
- no accidental `noindex` outside `404.html`
- no canonical mismatch warnings

## Banner-cycle update SOP

For each banner update:

1. Update `data/banner-data.csv`
2. Run `python3 scripts/build_banner_snapshot.py`
3. Re-upload changed files
4. Spot-check:
   - homepage
   - next banner
   - current banner
   - pull advice
   - one regenerated character page
5. If the phase changed, request reindexing for:
   - next banner
   - current banner
   - pull advice

## Known release caveats

- Some source links in the CSV are still mixed between official and secondary media.
- The site is ready for a soft launch, but the best long-term version should keep replacing secondary sources with stronger official links.
