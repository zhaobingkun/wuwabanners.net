# Daily Update SOP

Use this workflow for normal `wuwabanners.net` maintenance.

## What To Check Every Day

On a normal day, do one light pass.

Check these sources first:

1. Official site news / patch notes  
   `https://wutheringwaves.kurogames.com/`

2. Official YouTube / preview broadcast posts  
   `https://www.youtube.com/@WutheringWaves`

3. Official social / launch posts  
   Use the same official source chain already referenced in `data/banner-data.csv`.

4. In-game `Convene` page on banner-switch days  
   This is the best final confirmation for live phase timing and lineup.

## Normal Daily Rhythm

### Normal no-event day

- Check once in the morning.
- If there is no new official post, do not change `data/banner-data.csv`.
- No rebuild needed.

### Pre-preview / pre-banner window

- Check `2-3` times in the day:
  - morning
  - afternoon
  - evening if an official stream or post is expected

### Banner switch day

- Check once before the switch
- Check again after the switch is live in-game
- Confirm:
  - current phase
  - next phase
  - current weapons
  - start / end dates

## What To Update When Something Changes

Main source file:

- [data/banner-data.csv](/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net/data/banner-data.csv)

Fields that usually change:

- `version`
- `phase`
- `featured_characters`
- `featured_weapons`
- `start_date`
- `end_date`
- `source_url`
- `source_type`
- `announcement_date`
- `status`
- `last_checked`

## Rebuild Command

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/run_banner_update_cycle.py
```

This update cycle refreshes:

- `data/banner-snapshot.json`
- homepage dynamic blocks
- `next banner`
- `current banner`
- `banner history`
- `next rerun`
- `banner countdown`
- `pull advice`
- generated `should-you-pull-*` pages
- generated character support pages:
  - `*-materials`
  - `*-build`
  - `*-team-comps`
- `sitemap.xml`

It also:

- rebuilds reference detail pages
- compile-checks the Python scripts
- syntax-checks `assets/js/site.js`
- verifies key pages and sitemap coverage

## Fallback Manual Commands

If you only need part of the chain, the old direct commands still work:

```bash
python3 scripts/build_reference_pages.py
python3 scripts/build_banner_snapshot.py
python3 scripts/verify_site_build.py
```

## Preview Command

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 -m http.server 4173
```

Open and check:

- `http://127.0.0.1:4173/`
- `http://127.0.0.1:4173/wuthering-waves-next-banner/`
- `http://127.0.0.1:4173/wuthering-waves-current-banner/`
- `http://127.0.0.1:4173/pull-advice/`

Also spot-check one current-phase character and one next-phase character:

- `should-you-pull-*`
- `*-materials`
- `*-build`
- `*-team-comps`

## What To Verify After Rebuild

1. Homepage current / next timeline is correct.
2. `next banner` and `current banner` dates are correct.
3. `pull advice` still lists the right current and next characters.
4. Generated character support pages match the current snapshot.
5. `sitemap.xml` includes the generated character support URLs.

## When You Need New Pages

Do **not** add new pages every day.

Add or expand pages when:

- a new current/next phase rotates in
- a new featured character enters the tracked set
- an official reveal creates a new durable search intent

Most days:

- check official sources
- update CSV only if needed
- rebuild only if something actually changed
