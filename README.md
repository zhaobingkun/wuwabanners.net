# WuWa Banners

Static SEO site for `wuwabanners.net`, focused on Wuthering Waves banner intent pages:

- current banner
- next banner
- banner history
- banner countdown
- rerun watch
- pull advice pages

## Main rule

For normal banner-cycle updates, start with:

`data/banner-data.csv`

Then rebuild:

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/build_banner_snapshot.py
```

In most cases, this is the only file you need to edit.

Daily maintenance checklist:

- [DAILY-UPDATE-SOP.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/DAILY-UPDATE-SOP.md)
- [POST-LAUNCH-CONTENT-AUDIT.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/POST-LAUNCH-CONTENT-AUDIT.md)
- [AI-HANDOFF.md](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/AI-HANDOFF.md)

## What the build updates

The build script refreshes:

- `data/banner-snapshot.json`
- `assets/img/current-banner-card.svg`
- `assets/img/next-banner-card.svg`
- `assets/img/banner-history-card.svg`
- dynamic blocks inside:
  - `index.html`
  - `wuthering-waves-next-banner/index.html`
  - `wuthering-waves-current-banner/index.html`
  - `wuthering-waves-banner-history/index.html`
  - `wuthering-waves-next-rerun/index.html`
  - `wuthering-waves-banner-countdown/index.html`
  - `pull-advice/index.html`
- generated character pages:
  - `wuthering-waves-should-you-pull-*/index.html`
- generated character support pages:
  - `wuthering-waves-*-materials/`
  - `wuthering-waves-*-build/`
  - `wuthering-waves-*-team-comps/`
- `sitemap.xml`

## Data source rules

Use official sources first:

1. official site news or patch notes
2. official broadcast or official YouTube post
3. in-game Convene confirmation

Use secondary media only for temporary cross-checking when an official page is not yet enough.

## CSV fields that matter most

- `banner_type`
- `version`
- `phase`
- `featured_characters`
- `featured_weapons`
- `start_date`
- `end_date`
- `source_url`
- `status`
- `last_checked`

The current build script detects the active and next banner rows from the dated `character` rows, then matches weapon rows by `version + phase`.

## Normal update workflow

1. Update `data/banner-data.csv` from official sources.
2. Run `python3 scripts/run_banner_update_cycle.py`.
3. Preview locally.
4. Check homepage and these URLs:
   - `/wuthering-waves-next-banner/`
   - `/wuthering-waves-current-banner/`
   - `/wuthering-waves-banner-history/`
   - `/wuthering-waves-next-rerun/`
   - `/wuthering-waves-banner-countdown/`
   - `/pull-advice/`
5. Confirm new or changed character pages were regenerated.

## Local preview

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 -m http.server 4173
```

Open:

- `http://127.0.0.1:4173/`
- `http://127.0.0.1:4173/wuthering-waves-next-banner/`
- `http://127.0.0.1:4173/pull-advice/`

## When manual HTML edits are still needed

You still need to edit HTML manually when:

- adding a new page type
- changing layout
- changing FAQ structure site-wide
- changing hub strategy
- redesigning the site

## One-command maintenance cycle

After you edit banner data, use:

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/run_banner_update_cycle.py
```

This will:

- rebuild reference detail pages
- rebuild banner snapshot pages
- compile-check the Python scripts
- syntax-check `assets/js/site.js`
- verify core hubs, pages, focus character support pages, and key sitemap URLs

## Directory map

- `assets/css/`: site styles
- `assets/img/`: generated cards and static graphics
- `data/`: source CSV and generated JSON snapshot
- `scripts/`: build script
- `banners/`: banner hub
- `guides/`: guides hub
- `pull-advice/`: pull decision hub
- `wuthering-waves-should-you-pull-*/`: generated pull pages
# wuwabanners.net
