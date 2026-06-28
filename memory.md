# Project Memory

## Daily Check Workflow

- Read `AGENTS.md` and this file first.
- Run `./scripts/run_daily_official_check.sh` for current official-source checks.
- Inspect `data/banner-check-record.txt`, `data/banner-update-report.json`, and `data/banner-data.diff.txt`.
- Treat `NO_SIGNIFICANT_CHANGE` as no publish-needed unless a real banner row changed.
- Treat YouTube SSL/curl timeout or source-health changes as a fetch issue, not a content update by itself.
- The recurring manual-review row `ww-3.3-phase-1-weapon` is historical/secondary-media related and does not usually block current pages.

## SEO Experience

- Keep the site static and crawlable.
- Regenerate snapshots when data changes so homepage/current/next copy stays aligned.
- Do not leave stale current-banner copy after CSV updates.
- Prefer narrow, useful page intent and internal links over broad keyword repetition.

## 2026-06-23 Notes

- Added `AGENTS.md` and `memory.md` so future project work has local instructions and experience records.
- Daily banner check generated at 2026-06-23T11:00:33. Result: no significant banner-data change; candidate CSV only refreshed `last_checked` on safe rows from 2026-06-18 to 2026-06-23.
- Manual review still only flags `ww-3.3-phase-1-weapon` because it is old and uses a secondary-media source.
- Feed status: official site and DearPlayers were reachable; DearPlayers still shows possible version `3.5`; official YouTube failed with SSL/curl timeout, which is a fetch issue rather than a content update.

## 2026-06-24 Notes

- Daily banner check generated at 2026-06-24T10:00:58. Result: no real banner-data update; script comparison is `CHANGED` only because safe rows would refresh `last_checked` from 2026-06-18 to 2026-06-24 and the old secondary weapon row aged from 35 to 36 days.
- Manual review remains `ww-3.3-phase-1-weapon` only; no current-page blocker.
- Feed status: official site and DearPlayers were reachable; DearPlayers still shows possible version `3.5`; official YouTube still failed with SSL/curl timeout.
- Rechecked at 2026-06-24T15:47:43. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, or source URL changes. Candidate CSV still only refreshes safe-row `last_checked` values to 2026-06-24.

## 2026-06-25 Notes

- Daily banner check re-run at 2026-06-25T17:10:01. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, or public page content change detected.
- The report now lists 8 rows needing review because safe rows reached the 7-day `last_checked` threshold, and `ww-3.3-phase-1-weapon` is 37 days old with a secondary-media source.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-06-25.
- Feed status: official site and DearPlayers were reachable; DearPlayers still shows possible version `3.5`; official YouTube still failed with SSL/curl timeout.

## 2026-06-26 Notes

- Daily banner check generated at 2026-06-26T11:00:46. Result: no real banner-data update; script comparison is `CHANGED` because safe rows aged from 7 to 8 days, candidate `last_checked` values move from 2026-06-18 to 2026-06-26, and DearPlayers feed now emits `3.0` plus `3.5` version hits.
- Treat `3.0` as a feed/version-history signal, not a new future banner, because it is lower than the currently tracked 3.4 data and did not change any banner row.
- Candidate CSV still only refreshes safe-row `last_checked`; no lineup, date, source URL, or public page content change detected.
- Evening re-run at 2026-06-26T21:00 was interrupted after hanging during Python startup, so the 11:00 completed report is the reliable full report for the day.

## 2026-06-27 Notes

- Daily banner check re-run at 2026-06-27T21:43:45. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, or public page content change detected.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-06-27.
- Report still lists 8 rows needing review because safe rows are 9 days old; `ww-3.3-phase-1-weapon` is 39 days old, uses a secondary-media source, and the PCGamer source page no longer clearly matches expected banner names.
- Feed status: official site and DearPlayers were reachable; DearPlayers still emits `3.0` and `3.5` version hits. Treat `3.0` as feed/history noise and `3.5` as an unconfirmed version signal until a real banner row changes.
- Official YouTube still failed with SSL/curl timeout.

## 2026-06-28 Notes

- Daily banner check re-run at 2026-06-28T22:49:36. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content change detected.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-06-28.
- Report still lists 8 rows needing review because safe rows are 10 days old; `ww-3.3-phase-1-weapon` is 40 days old, uses a secondary-media source, and the PCGamer source page still does not clearly match expected banner names.
- Feed status: official site and DearPlayers were reachable; DearPlayers still emits `3.0` and `3.5` version hits. Treat `3.0` as feed/history noise and `3.5` as an unconfirmed version signal until a real banner row changes.
- Official YouTube still failed with SSL/curl timeout.

## 2026-06-28 SEO Page Expansion Note

- Current site has about 229 `index.html` pages, including 60 weapon pages, 50 item pages, and 52 character pages.
- `sitemap.xml` currently lists about 130 URLs and appears to include only the weapons/items hub pages, not weapon/item detail URLs.
- Before adding many new pages, prioritize sitemap coverage and internal-link discoverability for existing detail pages.
- If adding new pages, keep it small: 3-5 high-intent pages only, preferably exact banner-intent pages such as current version/banner detail pages. Do not publish speculative 3.5 pages until official banner facts exist.

## 2026-06-28 Sitemap Repair

- Updated sitemap generation so `scripts/build_banner_snapshot.py` scans canonical URLs from generated HTML, de-duplicates URLs, and skips `noindex` pages.
- Updated reference detail generation so weapon and item detail pages are indexable instead of `noindex,follow`.
- Rebuilt reference pages and sitemap. Final check: 229 `index.html` pages and 229 sitemap URLs.
- Verification passed with `python3 scripts/run_banner_update_cycle.py` and `python3 scripts/verify_site_build.py`.
