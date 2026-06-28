# Project Instructions

## Project Background

This repository powers `wuwabanners.net`, a static SEO site that tracks Wuthering Waves banner history, current banners, and upcoming banner signals.

## Goals

- Keep banner data accurate against official and high-signal public sources.
- Preserve static, crawlable HTML for SEO.
- Keep homepage, current banner, next banner, history, and supporting pages internally linked and easy to inspect.
- Avoid publishing generated or speculative changes unless banner facts actually changed.

## Boundaries

- Do not treat source-health changes, fetch failures, or `last_checked` churn as content updates.
- Do not update public banner facts from weak or unverified sources.
- Do not commit or publish unless explicitly asked.
- Work with existing user changes in the git tree; never revert unrelated edits.

## Working Rules

- Before project work, read this file and `memory.md`.
- Record useful project context, lessons, and daily outcomes in `memory.md`.
- Prefer the repo's existing scripts and data flow.
- For daily banner checks, run `./scripts/run_daily_official_check.sh`, then inspect the generated report and diff before deciding whether content changed.
- If only generated check files changed, report that no publish is needed.

## SEO Rules

- Important content must be present in raw HTML and not depend on JavaScript.
- Each public page needs a unique title, meta description, canonical URL, Open Graph metadata, and useful internal links.
- Keep pages focused on a clear user question or intent.
- Maintain `robots.txt`, `sitemap.xml`, structured data where appropriate, image alt text, and clean internal navigation.
- Prioritize useful, verifiable information over keyword stuffing.
