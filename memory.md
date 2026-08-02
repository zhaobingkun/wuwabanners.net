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

## 2026-06-29 Notes

- Daily banner check re-run at 2026-06-29T16:23:37. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content change detected.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-06-29.
- Report still lists 8 rows needing review because safe rows are 11 days old; `ww-3.3-phase-1-weapon` is 41 days old, uses a secondary-media source, and the PCGamer source page still does not clearly match expected banner names.
- Feed status: official site and DearPlayers were reachable; DearPlayers now emits only `3.5` as an unconfirmed version signal. The prior `3.0` feed noise is gone today.
- Official YouTube still failed with SSL/curl timeout.

## 2026-06-29 Copy Naturalization

- Reworked generated reference/detail page copy to reduce AI-template phrasing and internal SEO-planning language.
- Updated `scripts/build_banner_snapshot.py` and `scripts/build_reference_pages.py` so regenerated character, weapon, item, and support pages keep the more natural wording.
- Cleaned the weapons/items hub wording where it used phrases like "user wants", "branch", and "users usually need".
- Verification passed with `python3 scripts/run_banner_update_cycle.py` and `python3 scripts/verify_site_build.py`; no banner facts changed.

## 2026-06-30 Notes

- Daily banner check re-run at 2026-06-30T12:16:57. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content change detected.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-06-30.
- Report still lists 8 rows needing review because safe rows are 12 days old; `ww-3.3-phase-1-weapon` is 42 days old, uses a secondary-media source, and the PCGamer source page still does not clearly match expected banner names.
- Feed status: official site and DearPlayers were reachable; DearPlayers emits possible version references `3.5` and `2.7`. Treat `3.5` as unconfirmed and `2.7` as old-version feed noise unless a real banner row changes.
- Official YouTube feed check still failed with SSL/curl timeout; row-level source fetches otherwise completed.

## 2026-07-01 Notes

- Daily banner check re-run at 2026-07-01T17:03:20. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came only from DearPlayers feed version-signal churn: previous possible versions `3.5`, `4.9`, `3.0` changed to `3.5`, `5.4`, `3.0`.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-01; do not publish from this alone.
- Treat `3.5` as unconfirmed, and treat `5.4` / `3.0` as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; PCGamer source still does not clearly match expected banner names.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-02 Notes

- Daily banner check re-run at 2026-07-02T21:39:09. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from DearPlayers feed version-signal churn (`3.5`, `5.3`, `6.3`, `3.0`) and official_site fetch status recovering from failed to `curl-ok`.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-02; do not publish from this alone.
- Treat `3.5` as unconfirmed, and treat `5.3`, `6.3`, and `3.0` as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; PCGamer source still does not clearly match expected banner names.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-03 Notes

- Daily banner check re-run at 2026-07-03T17:12:43. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-03; do not publish from this alone.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; PCGamer source still does not clearly match expected banner names.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-04 Notes

- Daily banner check re-run at 2026-07-04T22:32:34. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source fetch changed from `curl-ok` to `fetch-failed` due to SSL/curl timeout.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-04; do not publish from this alone.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; today it failed to fetch rather than producing a content mismatch.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-05 Notes

- Daily banner check re-run at 2026-07-05T22:43:01. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result again came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source fetch failed with SSL/curl timeout.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-05; do not publish from this alone.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; today it failed to fetch rather than producing a content mismatch.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-06 Notes

- Daily banner check re-run at 2026-07-06T21:01:34. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result again came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source fetch failed with SSL/curl timeout.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-06; do not publish from this alone.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; today it failed to fetch rather than producing a content mismatch.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-07 Notes

- Daily banner check re-run at 2026-07-07T20:17:30. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result again came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source fetch changed from reachable in the previous state to `fetch-failed` today.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-07; do not publish from this alone.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; today it failed to fetch rather than producing a content mismatch.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-08 Notes

- Daily banner check re-run at 2026-07-08T22:34:47. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result again came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source fetch changed from reachable in the previous state to `fetch-failed` today.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-08; do not publish from this alone.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Manual review remains `ww-3.3-phase-1-weapon`; today it failed to fetch rather than producing a content mismatch.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-10 Notes

- Daily banner check re-run at 2026-07-10T09:43:34. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from source-health churn and aging rows: `ww-3.3-phase-1-character` PlayStation Blog source failed today, while `ww-3.3-phase-2-character` recovered from `fetch-failed` to `curl-ok`.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-10; do not publish from this alone.
- Manual review rows today are `ww-3.3-phase-1-character` and `ww-3.3-phase-1-weapon`, both due to source fetch failures rather than content mismatches.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-11 Notes

- Daily banner check re-run at 2026-07-11T18:15:04. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-11; do not publish from this alone.
- Manual review returned to only `ww-3.3-phase-1-weapon`, due to the recurring secondary-media PCGamer source fetch failure.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-13 Notes

- Daily banner check re-run at 2026-07-13T20:46:52. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source changed from reachable in the previous state to `fetch-failed` today.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-13; do not publish from this alone.
- Manual review remains only `ww-3.3-phase-1-weapon`, due to the recurring secondary-media PCGamer source fetch failure.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-14 Notes

- Daily banner check re-run at 2026-07-14T21:23:54. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source changed from reachable in the previous state to `fetch-failed` today.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-14; do not publish from this alone.
- Manual review remains only `ww-3.3-phase-1-weapon`, due to the recurring secondary-media PCGamer source fetch failure.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-15 Notes

- Daily banner check re-run at 2026-07-15T17:31:23. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV still only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-15; do not publish from this alone.
- Manual review remains only `ww-3.3-phase-1-weapon`; today the PCGamer secondary source fetched, but the page still did not clearly match expected banner names or version text.
- Failed row-level source fetches dropped to 0, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-15 Search Console Optimization

- Analyzed the 2026-07-15 Search Console 24-hour export from `/Users/zhaobingkun/Desktop/wuwabanners.net-Performance-on-Search-2026-07-15/`.
- Main query opportunities were `wuwa banner history` (60 impressions, 1 click, position 9.6), `wuwa banner countdown` (28 impressions, 0 clicks, position 6.75), `wuwa banners history` (11 impressions, 0 clicks, position 9), and `wuwa rerun tracker` (3 impressions, 0 clicks, position 7).
- Main page opportunity was `/wuthering-waves-banner-history/` with 124 impressions, 2 clicks, CTR 1.61%, position 11.13; homepage had more impressions but weaker average position, so the first optimization focused on tighter page-intent matches.
- Updated `scripts/build_banner_snapshot.py` so regenerated history, countdown, and rerun pages keep GSC-aligned metadata and H1s.
- Updated `/wuthering-waves-banner-history/` toward `WuWa Banner History List & Chart`, `/wuthering-waves-banner-countdown/` toward `WuWa Banner Countdown Timer`, and `/wuthering-waves-next-rerun/` toward `WuWa Rerun Tracker`.
- Exported fresh opportunity files to `data/search-console-query-opportunities.csv` and `data/search-console-page-opportunities.csv`.
- Verification passed with `python3 scripts/run_banner_update_cycle.py`.

## 2026-07-16 Notes

- Daily banner check re-run at 2026-07-16T21:52:01. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from source-health churn: `ww-3.3-phase-1-character` PlayStation Blog source and `ww-3.3-phase-1-weapon` PCGamer secondary source both failed to fetch today.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-16 for 6 rows; do not publish from this alone.
- Manual review rows today are `ww-3.3-phase-1-character` and `ww-3.3-phase-1-weapon`, both due to source fetch failures rather than content mismatches.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-17 Notes

- Daily banner check re-run at 2026-07-17T19:59:53. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from source-health churn: `ww-3.3-phase-1-weapon` PCGamer secondary source changed from `curl-ok` to `fetch-failed`.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-17 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`, due to the recurring secondary-media PCGamer source fetch failure.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.
- Official YouTube feed check still failed with SSL/curl timeout.

## 2026-07-19 Notes

- Daily banner check re-run at 2026-07-19T16:39:00. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-19 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`, because the recurring secondary-media PCGamer page did not clearly expose the current version string.
- Row-level source fetch failures are 0 today, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-20 Notes

- Daily banner check re-run at 2026-07-20T10:11:41. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The `CHANGED` result came from aging rows and candidate `last_checked` churn: reviewed rows moved from 31 days old to 32 days old, and `ww-3.3-phase-1-weapon` moved from 61 days old to 62 days old.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-20 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`, because the recurring secondary-media PCGamer page did not clearly expose the current version string.
- Row-level source fetch failures are 0 today, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-20 Page Expansion Planning

- The site already has 229 `index.html` pages, so low traffic should not be solved by bulk page generation.
- Search Console opportunity files still point to `wuwa banner history`, `wuwa banner countdown`, and `wuwa rerun tracker` as the strongest near-term queries; these existing pages rank around positions 6-12 but need higher CTR and stronger first-answer matching.
- If adding pages, keep the first batch small and high-intent: `wuwa soft pity`, `wuthering waves pity carry over`, `wuwa single pull vs 10 pull`, `wuwa past banners`, and a concise `wuwa maintenance countdown` or `next update countdown` page only if it can stay accurate.
- Do not add speculative future-version banner pages from DearPlayers version-number noise (`3.5`, `5.5`, `6.3`, `3.0`) unless official banner facts change.

## 2026-07-20 Homepage On Page SEO

- Applied homepage SEO improvements for the target keyword `Wuthering Waves Banner`.
- Updated homepage Title, meta description, OG/Twitter metadata, H1, hero lead, current snapshot intro, official video copy, and best-starting-points intro to use the full target phrase naturally.
- Added homepage sections for `How to use this Wuthering Waves banner tracker` and `What counts as a confirmed Wuthering Waves banner update?` to raise visible content from about 723 words to 1213 words while keeping source-verification rules clear.
- Added width and height to the YouTube thumbnail generated by `render_video_embed` to address the missing image dimension warning.
- Persisted generated homepage copy in `scripts/build_banner_snapshot.py`; verification passed with `python3 scripts/run_banner_update_cycle.py` and `python3 scripts/verify_site_build.py`.

## 2026-07-21 Notes

- Daily banner check re-run at 2026-07-21T18:26:31. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-21 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`, because the recurring secondary-media PCGamer page did not clearly expose the current version string.
- Row-level source fetch failures are 0 today, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-22 Notes

- Daily banner check re-run at 2026-07-22T17:30:57. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-22 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`; the recurring secondary-media PCGamer page fetched but did not clearly match expected banner names or the current version string.
- Row-level source fetch failures are 0 today, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-24 Notes

- Daily banner check re-run at 2026-07-24T20:47:41. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-24 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`; the recurring secondary-media PCGamer page fetched but did not clearly match expected banner names or the current version string.
- Row-level source fetch failures are 0 today, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-25 Notes

- Daily banner check re-run at 2026-07-25T23:18:37. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-25 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`; the recurring secondary-media PCGamer page fetched but did not clearly match expected banner names or the current version string.
- Row-level source fetch failures are 0 today, but official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-27 Notes

- Daily banner check re-run at 2026-07-27T17:47:11. Result: `NO_SIGNIFICANT_CHANGE`; no banner lineup, date, source URL, live CSV, or public page content changed.
- Candidate CSV only refreshes safe-row `last_checked` values from 2026-06-18 to 2026-07-27 for 7 rows; do not publish from this alone.
- Manual review row today is only `ww-3.3-phase-1-weapon`; the recurring secondary-media PCGamer page fetched but did not clearly match expected banner names or the current version string.
- Row-level source fetch failures are 0 today, but the official YouTube feed check still failed with SSL/curl timeout.
- DearPlayers feed still emits possible version references `3.5`, `5.5`, `6.3`, and `3.0`; treat these as feed noise unless an official banner row, date, lineup, or source page changes.

## 2026-07-28 Notes

- Daily script comparison result was `CHANGED`, but that comparison only reflected source-health and row-aging churn: one 3.3 weapon source timed out, the 3.4 preview page stopped matching expected terms, and safe candidate rows refreshed `last_checked`.
- Manual live verification found that the site's public banner facts are materially stale despite the script's prior treatment of `3.5` as feed noise.
- The official Wuthering Waves site currently features Yangyang: Xuanling, and the official App Store release notes identify Version 3.5 with Yangyang: Xuanling, Suisui, Azure Oath, and Firstlight's Herald.
- Official server-time scheduling confirms Version 3.5 Phase 1 as Yangyang: Xuanling, Lynae, and Luuk Herssen from July 10 10:00 to July 30 09:59; Phase 2 is Suisui and Aemeath from July 30 10:00 to August 19 11:59. Some media pages display July 31/August 20 because of timezone conversion; public site data should use server time.
- Updated `data/banner-data.csv` with the four official Version 3.5 character and weapon rows, using the official Wuthering Waves event-calendar post as the primary source.
- Rebuilt the homepage, current/next banner pages, countdown, schedule, history, character hubs, build/material/team pages, SVG cards, snapshot, and sitemap. The generated site now treats 3.5 Phase 1 as current and 3.5 Phase 2 as next.
- Made next-banner metadata, homepage month/version copy, and next-banner countdown metadata data-driven so future update cycles do not retain stale version text.
- Added verified local character art for Yangyang: Xuanling and Suisui, and added official Wuthering Waves X URLs to the trusted source validation list.
- `scripts/run_banner_update_cycle.py` and `scripts/verify_site_build.py` passed after the Version 3.5 rebuild. The 2026-07-28 daily source check still flags the four X source rows for manual review because automated X fetching fails; this is source-health noise, not a contradiction of the manually verified official posts.
- No distinct new July 28 announcement was found; this release corrects the previously missed Version 3.5 update.

## 2026-07-29 Notes

- Daily banner check re-run at 2026-07-29T10:42:50. Script comparison result: `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The reported changes were only row-aging and candidate `last_checked` churn from July 28 to July 29. The same four Version 3.5 X sources remain automated-fetch failures, and the same PCGamer 3.3 weapon row remains manual review.
- Manual inspection of the official Wuthering Waves X profile found a new Suisui `Chapter of Composure` artwork post about 44 minutes before the check. The pinned Suisui Resonator Showcase was about 23 hours old, and the Version 3.5 upcoming-events compilation was about 16 hours old.
- These posts promote the already-recorded Version 3.5 Phase 2 lineup; they do not change the confirmed Suisui/Aemeath lineup, Firstlight's Herald/Everbright Polestar weapons, or July 30 10:00 server-time start.
- No site rebuild or publication is needed today. Recheck after the July 30 phase switch to confirm the live in-game state.

## 2026-07-30 Notes

- Daily banner check ran at 2026-07-30T09:56:05, just before the scheduled phase change. Its `CHANGED` result was only row-aging and candidate `last_checked` churn; no new lineup, date, weapon, or source row appeared.
- Manual inspection of the official Wuthering Waves X profile found Aemeath's `Guiding Starlance` Resonator Review, the `Virtual Crisis: Quadrant Trials` July 30 event notice, `The Four Seasons of Suisui`, and the Suisui EP. These support the already-recorded Version 3.5 Phase 2 rollout without changing its banner facts.
- At 2026-07-30 10:00 CST/server time, Version 3.5 Phase 2 became current: Suisui and Aemeath with Firstlight's Herald and Everbright Polestar, scheduled through 2026-08-19 11:59.
- A production check immediately after 10:00 showed that the live current-banner page still described Version 3.5 Phase 1. The site now needs a rebuild so Phase 2 becomes current and the post-Phase-2 next-banner state is recalculated.
- The initial read-only check did not rebuild or publish. After the user authorized a Git submission, the four Version 3.5 rows were manually re-verified and their `last_checked` values advanced to 2026-07-30.
- Fixed `pick_current_and_next` to prefer the banner with the latest start timestamp when two phases share a calendar date. This prevents Phase 1 ending at 09:59 from winning over Phase 2 starting at 10:00.
- Made next-banner and next-banner-countdown metadata switch to an honest “not announced” state when the current phase is also the last known official phase.
- Rebuilt the site successfully: Phase 2 is current, the next banner is pending official reveal, the update cycle and verifier passed, and local HTTP smoke tests returned 200 for the homepage, current/next/countdown/schedule pages, and Suisui/Aemeath hubs.

## 2026-07-31 Notes

- Daily banner check ran at 2026-07-31T10:16:55. The script reported `CHANGED`, but no banner lineup, date, source URL, live CSV, or public page content changed.
- The difference was only row aging and source-health churn: the rotating DearPlayers events page no longer exposed Chisa and Phrolova for the historical Version 3.3 Phase 2 row. The candidate file only refreshes six older safe rows.
- Manual inspection of the official Wuthering Waves X profile found no July 31 post as of about 10:17 CST and no Version 3.6 or next-banner reveal. The latest visible posts were July 30 promotional or event items: August calendar art, Aemeath and Suisui images, and the In Search of Lost Jade web event.
- Current Version 3.5 Phase 2 facts remain Suisui and Aemeath with Firstlight's Herald and Everbright Polestar through August 19 11:59 server time; the next banner remains pending.
- No rebuild or publication is needed today.

## 2026-08-02 Notes

- Daily banner check generated at 2026-08-02T11:00:42. The script reported `CHANGED`, but the diff is still row-aging, source-health churn, and candidate `last_checked` refreshes only; no live CSV, lineup, date, weapon, or source URL changed.
- Manual inspection of the official Wuthering Waves X profile found a new pinned Version 3.6 Preview Special Broadcast announcement posted on August 2. The broadcast is scheduled for August 7, 2026 at 19:00 UTC+8.
- Treat the Version 3.6 broadcast notice as an upcoming-news signal, not a confirmed banner update. It does not yet reveal the next banner lineup, dates, or weapons.
- Current Version 3.5 Phase 2 facts remain Suisui and Aemeath with Firstlight's Herald and Everbright Polestar through August 19 11:59 server time; the next banner remains pending official reveal.
- No rebuild or publication is needed today unless the site later adds a non-banner news module for preview livestream notices.

## 2026-08-02 News Channel

- Added a static official-news channel at `/news/` backed by `data/news.json`, separate from `data/banner-data.csv`.
- First news item covers the official Version 3.6 Preview Special Broadcast scheduled for August 7, 2026 at 19:00 UTC+8, with source URL `https://x.com/Wuthering_Waves/status/2083855332464615710`.
- News pages use `CollectionPage` and `NewsArticle` structured data, canonical URLs, OG/Twitter metadata, and sitemap inclusion.
- Keep official broadcasts, event notices, music posts, and version-news items in `data/news.json` until they confirm banner facts. Only update banner CSV/pages when lineup, weapon, date, phase, or source facts change.
- `python3 scripts/run_banner_update_cycle.py` passed after the news-channel build and verifier update.
