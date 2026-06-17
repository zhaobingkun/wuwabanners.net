# WuWa Banners Product Design Audit

Date: 2026-06-17

Surface audited:
- Home
- Next banner
- Current banner
- Banner countdown
- Banner schedule
- Pull advice

Viewports:
- Desktop: 1280 x 720
- Mobile: 390 x 844

Evidence screenshots:
- `01-desktop-home.png`
- `01-mobile-home.png`
- `02-desktop-next-banner.png`
- `02-mobile-next-banner.png`
- `03-desktop-current-banner.png`
- `03-mobile-current-banner.png`
- `04-desktop-countdown.png`
- `04-mobile-countdown.png`
- `05-desktop-schedule.png`
- `05-mobile-schedule.png`
- `06-desktop-pull-advice.png`
- `06-mobile-pull-advice.png`

## Step Health

1. Home: mixed.
   The desktop hero is visually strong and makes the site category obvious. On mobile, the sticky header uses about 182px of vertical space and pushes the first real banner state below the fold. The first screen gives navigation and broad SEO copy, but not the actual current/next status card.

2. Next banner: mixed.
   The direct answer is visible above the fold on mobile and desktop, which is good. There are no strong above-fold CTAs, so users who want to compare current, countdown, or pull advice must rely on inline links farther down.

3. Current banner: mixed.
   The title and answer are clear, but the live lineup details sit below a long intro stack. On mobile, the first actionable support content starts far below the first viewport.

4. Countdown: good with a mobile caveat.
   This is the clearest query-answer page. The current end date and next checkpoint are easy to understand. Mobile still inherits the large header and table pattern, which slows scanning after the first answer.

5. Schedule: mixed.
   Desktop shows useful current/next schedule cards quickly. The right card title is close to overflow at desktop width, and mobile relies on wide tables later in the page.

6. Pull advice: mixed.
   The page explains the decision frame well, but the above-fold mobile screen has no fast route buttons to "spend now", "save", "protect pity", or "check reruns". Users must scroll before they can act.

## Findings

1. Mobile header consumes too much first-screen space.
   Evidence: every mobile screenshot shows the logo plus two full rows of nav before content. The header is about 182px tall on a 390 x 844 viewport, so roughly 22 percent of the first screen is navigation.
   Recommendation: collapse secondary nav into a compact menu below 640px, or show only Home, Banners, Guides, and a menu button. Keep the brand row shorter.

2. The homepage does not expose the live banner state early enough on mobile.
   Evidence: `01-mobile-home.png` shows the headline and two CTA buttons, but the current/next state panel begins below the viewport. The measured first panel top is about 1146px.
   Recommendation: move a compact "Current / Next / Ends / Source checked" status strip above or directly under the hero CTAs on mobile.

3. Most intent pages lack above-fold action buttons.
   Evidence: next, current, countdown, schedule, and pull-advice pages show direct-answer copy, but their collected `.btn` / CTA list is empty above the main content. Users have to read or scroll to route themselves.
   Recommendation: add a reusable quick-action row after the direct answer: Current, Next, Countdown, Pull advice. On pull advice, use decision labels: Spend now, Save, Pity, Reruns.

4. Tables are technically scroll-contained but visually read as overflow on mobile.
   Evidence: mobile metrics show 640px tables inside 390px viewports across home, next, current, countdown, schedule, and pull advice. `scrollWidth` remains 390, so the wrapper is likely containing overflow, but the content is hard to parse in screenshots.
   Recommendation: convert the first critical table on each page into stacked mobile rows or compact cards. Keep wide tables for desktop and secondary detail.

5. Desktop card content is close to clipping on schedule.
   Evidence: `05-desktop-schedule.png` shows "Version 3.4 The Dream Not Dreamed" near the edge of the current banner card.
   Recommendation: reduce card heading size in schedule cards, increase internal padding/line-height, or let the card title wrap earlier.

6. "Last updated" dates are visible but not trust-building enough.
   Evidence: pages show `Last updated: June 13, 2026`, while today's check found a 3.5 signal on June 17. Users will not know whether June 13 is stale content or intentionally stable data.
   Recommendation: distinguish data freshness from page rebuild date, for example "Banner data checked June 17, 2026; content last rebuilt June 13, 2026."

7. Visual style is distinctive but slightly heavy for repeated lookup tasks.
   Evidence: the brand grid, large headings, and high-contrast panels work well for a homepage, but repeated intent pages use large hero blocks before the actionable snapshot.
   Recommendation: keep the visual language, but make utility pages denser: shorter hero padding, smaller h1 at mobile, and a first-screen answer card.

## Accessibility Risks From Screenshots

- Sticky navigation takes substantial mobile space and may create extra scrolling for keyboard or switch users.
- Some important links are small inline text links after long copy; touch targets in the nav are acceptable, but deeper content should use larger card/button targets.
- Table content requires horizontal reading inside wrappers. This is not necessarily a compliance failure, but it is a usability and screen-reader comprehension risk if table summaries are not explicit.
- Contrast appears generally strong, but the muted gray body text over patterned backgrounds should be checked with computed contrast, not judged from screenshots alone.

## Recommended Next Pass

Do a focused implementation pass rather than a full redesign:

1. Add a compact status strip component for current, next, end date, and last checked.
2. Replace mobile nav with a compact collapsed pattern.
3. Add quick-action rows to the five intent pages.
4. Convert first critical tables to mobile cards.
5. Tighten utility page hero spacing and mobile h1 sizing.

This should improve task completion without changing the site's SEO structure or visual identity.

## Implementation Pass Completed

Completed on 2026-06-17.

Changes shipped:
- Added a compact current/next status strip with Current, Ends, Next, and Snapshot fields.
- Added quick-action rows for banner intent pages and pull-advice decision routing.
- Reduced mobile navigation to the highest-priority links: Home, Banners, Guides, and Pity.
- Added responsive table labeling so key tables become mobile cards after JavaScript initializes.
- Added asset version parameters to CSS and JS URLs so the new responsive styles do not get stuck behind cached assets.

Post-change evidence screenshots:
- `final-mobile-home.png`
- `final-mobile-next-banner.png`
- `final-mobile-schedule.png`
- `final-mobile-pull-advice.png`
- `final-desktop-schedule.png`

Verification notes:
- Build cycle passed with `python3 scripts/run_banner_update_cycle.py`.
- Core site verification passed with `python3 scripts/verify_site_build.py`.
- Browser DOM verification showed mobile media query active, header height reduced to about 107px, status strip present, quick actions present on schedule, table labels initialized, and no horizontal overflow on the checked schedule page.

## Limits

- This audit used screenshots and read-only DOM inspection only.
- It did not test keyboard navigation, screen-reader output, real network performance, analytics funnels, or Search Console behavior.
- It did not change production HTML/CSS.
