# Performance Optimization Plan

## Target

- Primary target: improve mobile PSI from `54` into the green zone first.
- Secondary target: reduce desktop TBT and remove avoidable best-practice warnings.
- Practical note: a hard `100` is not realistic while live YouTube embeds and live GA loading remain on the page.

## Findings From `item.rtf`

### P0: Safe changes to do first

- Make Google Fonts non-blocking.
- Add explicit `width` and `height` to snapshot images.
- Keep hero image priority on the homepage.
- Switch YouTube embeds to `youtube-nocookie`.
- Preserve image aspect ratio in CSS to avoid avoidable layout work.

### P1: High-impact changes that alter behavior

- Replace live YouTube iframes with click-to-load placeholders.
  - Biggest likely win for mobile.
  - Changes from "player visible immediately" to "load on click".
- Delay analytics script load until `load` or idle.
  - Helps TBT.
  - Changes analytics timing and may miss a small amount of very short visits.
- Reduce or remove Google-hosted web fonts.
  - Helps render blocking and network chain length.
  - Changes visual identity.

### P2: Later refinements

- Self-host font files if typography must stay the same.
- Add a lightweight local poster image for each video block.
- Split homepage media so only one heavy media block is shown above the fold on mobile.

## What Was Implemented In This Pass

- Non-blocking Google Fonts loading with `media="print"` plus `noscript` fallback.
- Explicit image dimensions for banner SVGs.
- `fetchpriority="high"` for the homepage hero card.
- `decoding="async"` on snapshot images.
- `youtube-nocookie` embeds instead of standard YouTube embed URLs.
- CSS aspect-ratio reservation for banner art blocks.
- Template updates in `scripts/build_banner_snapshot.py` so future builds keep these optimizations.

## Recommended Next Decision

If we want the biggest next PSI jump, the next step should be:

1. Replace embedded YouTube iframes with a click-to-load video card.
2. Optionally defer GA until after the main content is interactive.

Both are meaningful behavior changes and should be approved before implementation.
