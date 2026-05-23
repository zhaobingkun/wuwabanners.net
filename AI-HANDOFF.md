# AI Handoff

This file is a working handoff for the `wuwabanners.net` project so another AI or engineer can continue without rebuilding context from scratch.

## Project Identity

- Project path: `/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net`
- Site domain: `wuwabanners.net`
- Site name / brand: `WuWa Banners`
- Topic: `Wuthering Waves` banner tracking, planning, reference browsing, and lightweight wiki-style support pages

The site is intentionally built as a static, SEO-friendly, browser-first reference site.

## Core Product Direction

The site is not meant to be a generic news blog. The agreed direction is:

- homepage shows important time-sensitive banner information first
- top navigation leads users into branches
- each branch should follow `nav -> list page -> detail page`
- detail pages can then lead to narrower support pages
- avoid thin, random long-tail pages with no structural role
- prefer evergreen or repeatedly updated pages over one-day hype pages

The homepage should surface:

- timeline
- current banner end timing
- next banner start timing
- fast pull / planning context

## High-Level Site Structure

### Main navigation branches

- `Home`
- `Banners`
- `Guides`
- `Characters`
- `Weapons`
- `Items`

### Home

Current homepage direction:

- hero
- current timeline snapshot
- media block
- `Browse by section`
- `Reference branches at a glance`
- `How the site is structured`
- `Best starting points`
- footer grouped by the same branch language

Homepage language is grouped into:

- `Banner answers first`
- `Planning answers first`
- `Reference browsing first`

Footer mirrors this with:

- `Banner answers`
- `Planning answers`
- `Reference browsing`

### Banners branch

Main list / hub:

- `/banners/`

Primary pages:

- `/wuthering-waves-next-banner/`
- `/wuthering-waves-current-banner/`
- `/wuthering-waves-banner-history/`
- `/wuthering-waves-banner-countdown/`
- `/wuthering-waves-next-rerun/`
- `/wuthering-waves-banner-schedule/`
- `/wuthering-waves-banner-order/`
- `/wuthering-waves-event-calendar/`
- `/wuthering-waves-daily-reset-time/`
- `/wuthering-waves-weekly-reset-time/`
- `/wuthering-waves-next-banner-date/`
- `/wuthering-waves-current-banner-end-date/`
- `/wuthering-waves-next-banner-countdown/`
- `/wuthering-waves-current-banner-characters/`
- `/wuthering-waves-all-banners/`
- `/wuthering-waves-next-character/`
- `/wuthering-waves-timeline/`
- `/wuthering-waves-weapon-banner/`
- `/wuthering-waves-pity-system/`

`Banner history` has already been refactored into:

- list page
- phase detail pages

Examples:

- `/wuthering-waves-banner-history/version-3-2-phase-2/`
- `/wuthering-waves-banner-history/version-3-3-phase-1/`
- `/wuthering-waves-banner-history/version-3-3-phase-2/`

History pages were upgraded from plain text into visual lineup cards with:

- character art when available
- weapon art when available
- placeholder cards when art is missing
- previous / next phase navigation on detail pages

### Guides branch

Main hub:

- `/guides/`

Planning-style pages and support pages live here conceptually, even if some URLs are top-level pages.

There is also:

- `/pull-advice/`
- generated `should-you-pull-*` pages

### Characters branch

Main list / hub:

- `/wuthering-waves-characters/`

This is now a true branch:

- list page
- detail page for each character with downloaded reference image
- deeper guide pages for selected focus characters

Examples:

- `/wuthering-waves-characters/cantarella/`
- `/wuthering-waves-characters/hiyuki/`
- `/wuthering-waves-characters/denia/`

For current and next banner focus characters, the branch also includes support pages:

- `/wuthering-waves-hiyuki-materials/`
- `/wuthering-waves-hiyuki-build/`
- `/wuthering-waves-hiyuki-team-comps/`
- same pattern for `Mornye`, `Iuno`, `Denia`, `Chisa`, `Phrolova`

### Weapons branch

Main list / hub:

- `/wuthering-waves-weapons/`

This branch now has:

- list page
- detail pages generated from downloaded reference data
- direct image click-through from the gallery to detail pages

Example:

- `/wuthering-waves-weapons/frostburn/`

### Items branch

Main list / hub:

- `/wuthering-waves-items/`

This branch now has:

- list page
- image gallery
- detail pages generated from downloaded reference data

Example:

- `/wuthering-waves-items/abyssal-husk/`

## Major Build Decisions Made During This Project

## Build Timeline Summary

This is the compressed build history of the site.

### Phase 1: domain and site direction

- domain was fixed as `wuwabanners.net`
- site direction moved away from generic SEO/news ideas
- focus settled on `Wuthering Waves` banner tracking + planning + wiki-style browsing

### Phase 2: first launch skeleton

- homepage, core banner pages, hubs, robots, sitemap, favicon, and analytics were added
- site was designed as static HTML with strong crawlable content
- structured data and core metadata were added

### Phase 3: CSV-driven banner maintenance

- `data/banner-data.csv` became the main update source
- `scripts/build_banner_snapshot.py` was built out so routine updates mostly flow from source data
- homepage timing blocks, banner pages, history, pull pages, support pages, and sitemap started rebuilding from script output

### Phase 4: media and performance pass

- local SVG card art was added to reduce visual flatness
- YouTube embeds were converted into click-to-load lightweight placeholders
- thumbnail-first video presentation replaced plain blocks
- performance work reduced unnecessary first-load cost

### Phase 5: branch restructuring

- the site moved from many parallel pages into `nav -> list -> detail -> support`
- homepage was reorganized into grouped entry points
- `banners`, `guides`, `characters`, `weapons`, and `items` became clearer branches

### Phase 6: banner history refactor

- `banner history` became `list page + phase detail pages`
- history visuals were added
- previous / next phase navigation was added

### Phase 7: reference branch build-out

- WuWa Tracker-inspired image reference branches were added for:
  - characters
  - weapons
  - items
- downloader and reference page generation scripts were created
- reference detail pages got their own consistent structure

### Phase 8: character support expansion

- focus characters got:
  - hub pages
  - should-you-pull pages
  - materials pages
  - build pages
  - team comps pages
- support pages were later deepened with stronger branch context and next-step guidance

### 1. Domain choice

`wuwabanners.net` was chosen over `wuwabanners.online`.

Reasoning:

- shorter-trust perception was better
- stronger fit for a long-running wiki / tracker style site
- avoids locking the project to just one page type like `next-banner`

### 2. Content direction

The user explicitly did not want this to become:

- a generic AI-tools SEO site
- a movie / entertainment short-lifecycle trend site

The working direction became:

- game wiki / banner / planning / reference browsing
- mobile and desktop browser friendly
- pages people revisit repeatedly

### 3. Update model

The site should not require daily creation of new pages.

Preferred maintenance model:

- keep core pages alive
- update existing pages on official changes
- expand structure only when a new branch or reusable page type is justified

### 4. Source policy

Primary facts should come from official sources whenever possible:

- official site
- official broadcast
- official patch notes
- official social posts
- in-game `Convene` confirmation on phase switch

Unofficial sources like WuWa Tracker are acceptable for:

- structural inspiration
- image scraping references
- branch ideas

But not as the main fact source for authoritative banner data.

### 5. Structural direction

The site moved away from a flat pile of pages.

Agreed direction:

- top nav
- hub / list pages
- detail pages
- support pages below details when helpful

This became especially important for:

- `banner history`
- `characters`
- `weapons`
- `items`

## Current Technical Architecture

## Key scripts

### `scripts/build_banner_snapshot.py`

Primary site build script for banner-driven pages.

It currently regenerates or refreshes:

- `data/banner-snapshot.json`
- homepage dynamic banner blocks
- current / next banner content blocks
- history pages
- countdown / rerun / timing pages
- character guide hubs
- `materials / build / team comps` pages
- generated visual cards
- `sitemap.xml`

Primary data input:

- `data/banner-data.csv`

This CSV is the main day-to-day maintenance file.

### `scripts/build_reference_pages.py`

Builds reference detail pages for:

- characters
- weapons
- items

Primary input:

- `data/reference-images.json`

This script creates or refreshes detail pages based on downloaded image metadata.

### `scripts/verify_site_build.py`

Lightweight build verifier for the current site structure.

It checks:

- key files exist
- homepage and hub pages still contain expected sections
- current / next banner pages still contain snapshot data
- focus character hubs and support pages still exist
- reference branches still have entries
- key sitemap URLs are still present

It also emits warnings when older history rows still depend on secondary sources.

### `scripts/run_banner_update_cycle.py`

This is now the preferred maintenance entry point after editing banner data.

It runs:

- `build_reference_pages.py`
- `build_banner_snapshot.py`
- Python compile checks
- `node --check assets/js/site.js`
- `verify_site_build.py`

### `scripts/download_wuwatracker_reference_images.py`

Downloads reference image assets from WuWa Tracker pages and updates:

- `assets/img/reference/characters/`
- `assets/img/reference/weapons/`
- `assets/img/reference/items/`
- `data/reference-images.json`

Wrapper:

- `scripts/download_wuwatracker_reference_images.sh`

Notes:

- the script was adjusted to use English source pages
- old directories are cleared before a fresh pull
- parsing was tightened to avoid mixing item art into character / weapon sets

## Frontend assets

### `assets/js/site.js`

Handles:

- active nav highlighting
- reference gallery rendering
- reference directory rendering
- lazy YouTube video loader

### `assets/css/site.css`

Contains:

- global layout styling
- history visual card styling
- reference card styling
- hub section styling
- lightweight video placeholder styling

## Media / Performance Decisions

Several performance and UX passes were already made:

- Google Fonts moved toward non-blocking loading
- first-screen assets got clearer priority treatment
- YouTube embeds were changed to click-to-load lightweight placeholders
- later improved to show real YouTube thumbnail imagery first
- `youtube-nocookie` is used

There is already a planning file for this:

- `PERFORMANCE-OPTIMIZATION-PLAN.md`

## Existing Maintenance Docs

- `README.md`
- `DAILY-UPDATE-SOP.md`
- `LAUNCH-CHECKLIST.md`
- `SEARCH-CONSOLE-SUBMIT-ORDER.md`
- `PERFORMANCE-OPTIMIZATION-PLAN.md`
- `POST-LAUNCH-CONTENT-AUDIT.md`

This handoff file is intended to connect those docs into a single narrative.

## Daily / Routine Update Workflow

The operational rule is:

- do not randomly edit many HTML files first
- update the source data
- rebuild
- preview
- deploy

### Banner update workflow

1. Check official sources.
2. If banner timing / lineup changed, edit:
   - `data/banner-data.csv`
3. Rebuild:

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/run_banner_update_cycle.py
```

4. Preview locally if needed:

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 -m http.server 4173
```

5. Check at minimum:

- homepage
- `next banner`
- `current banner`
- `banner history`
- `pull advice`
- one current character support page
- `sitemap.xml`

### Reference image refresh workflow

When reference branches need refreshed art or new list/detail coverage:

```bash
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
./scripts/download_wuwatracker_reference_images.sh
python3 scripts/build_reference_pages.py
python3 scripts/build_banner_snapshot.py
```

Then inspect:

- `wuthering-waves-characters/`
- `wuthering-waves-weapons/`
- `wuthering-waves-items/`

## Important Current Content State

### Focus characters currently wired into deeper guide support

The main deep-support character set currently includes:

- `Hiyuki`
- `Mornye`
- `Iuno`
- `Denia`
- `Chisa`
- `Phrolova`

For these, there are:

- character hub pages
- `should you pull`
- `materials`
- `build`
- `team comps`

### Banner history coverage

Currently seeded around:

- `Version 3.2 Phase 2`
- `Version 3.3 Phase 1`
- `Version 3.3 Phase 2`

### Reference image coverage

At last successful pull, reference data included roughly:

- `47` character images
- `59` weapon images
- `49` item images

These numbers may change after a future refresh.

## Important Recent Structural Changes

These were the major last-stage improvements before this handoff:

### Hub intros unified

The hub pages now use a more consistent branch explanation style:

- `banners`
- `guides`
- `characters`
- `weapons`
- `items`

Each branch now tries to explain:

- what this branch answers first
- where users should go next
- how hub / detail / support relate

### Character support pages deepened

`materials / build / team comps` pages were improved with:

- breadcrumbs back to the actual character hub
- `Where this page sits`
- `What to compare before locking`
- stronger next-step context

### Character guide hubs deepened

Character hubs were improved with:

- `How to use the X hub`
- branch context
- clearer support page flow

### Reference detail pages unified

Character / weapon / item detail pages now share a more consistent structure:

- breadcrumbs
- branch map
- branch links
- detail snapshot
- visual reference
- previous / next nearby navigation

### Homepage became more of a real front door

Instead of being a loose collection of sections, the homepage now frames the site by:

- showing timing first
- grouping entry points
- explaining structure
- separating banner answers vs planning answers vs reference browsing

## Known Caveats

### 1. Generated pages should usually be changed through scripts

Many pages are generated or semi-generated.

In general:

- if the change affects a branch pattern, edit the build script
- if the change is a one-off homepage / hub wording issue, direct HTML edit may be fine

### 2. Some banner imagery may still be incomplete

History or lineup pages can fall back to placeholders if local reference art is missing.

This is expected behavior.

### 3. Not every page is equally deep

The site has a strong structural skeleton now, but page depth still varies:

- some hubs are well-shaped
- some support pages are still template-forward
- banner core pages are stronger than many long-tail pages

### 4. Source quality still matters

The operating rule remains:

- official source first for banner facts
- secondary source only as support or fallback

## Recommended Next Steps For The Next AI

If another AI continues from here, the best next work is not random expansion.

Priority order should be:

1. Publish the latest local changes if not yet deployed.
2. Check whether current banner data still matches official sources.
3. Strengthen the most important core pages further:
   - `next banner`
   - `current banner`
   - `banner history`
   - `pull advice`
4. Deepen the focus character support pages one layer more:
   - real materials tables
   - clearer build decision logic
   - stronger team archetype explanations
5. Keep hub language aligned whenever new branches are added.
6. Avoid spraying new URLs unless they clearly fit the branch model.

## Recommended Working Rules For The Next AI

- treat this site as a structured static wiki, not a news blog
- prefer improving existing hubs and detail pages over mass-producing thin pages
- keep homepage useful first, decorative second
- preserve `nav -> list -> detail -> support` logic
- update source data first, then regenerate
- do not manually patch dozens of generated pages if a script/template change is more correct

## Conversation-Level Context Summary

These are the most important user preferences established during the project:

- the site should feel usable in browser on both mobile and desktop
- the user wanted images and video where useful, but not a heavy video-first site
- the user preferred clear structural navigation over flat page sprawl
- the user wanted homepage timing information front and center
- the user wanted reference branches similar in spirit to WuWa Tracker, but adapted into a cleaner SEO-friendly site structure
- the user explicitly asked for records so a later AI can continue cleanly

## Quick Start For The Next AI

If you are the next AI picking this up, start here:

1. Read:
   - `README.md`
   - `DAILY-UPDATE-SOP.md`
   - `AI-HANDOFF.md`
2. Check current data sources:
   - `data/banner-data.csv`
   - `data/reference-images.json`
3. Rebuild if needed:

```bash
python3 scripts/build_banner_snapshot.py
python3 scripts/build_reference_pages.py
```

4. Spot-check:

- homepage
- banners hub
- banner history
- one character hub
- one character support page
- one weapon detail page
- one item detail page

That should be enough to regain working context quickly.
