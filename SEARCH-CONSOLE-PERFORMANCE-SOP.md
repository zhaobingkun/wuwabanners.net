# Search Console Performance SOP

Use this after Search Console has query or page performance data.

## Export

In Google Search Console, open Performance, set the last 28 days, then export either:

- Queries
- Pages
- Queries filtered to one important page

Save the CSV locally. Coverage exports show indexing status only; this workflow needs clicks, impressions, CTR, and average position.

## Analyze

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/analyze_search_console_performance.py /path/to/search-console-performance.csv
```

The output is:

```text
data/search-console-opportunities.csv
```

## Use The Output

Prioritize rows with:

- high impressions
- low CTR
- average position from 3 to 30
- current, next, countdown, schedule, history, rerun, pity, or pull-advice intent

For each priority row, update the page title, meta description, H1, and first answer box before adding new pages.
