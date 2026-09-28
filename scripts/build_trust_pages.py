#!/usr/bin/env python3
from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CSS_HREF = "/assets/css/site.css?v=20260617-pd"
JS_SRC = "/assets/js/site.js?v=20260617-pd"

GTAG_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-C73K15FD00"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-C73K15FD00');
</script>"""

NAV = '<header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>'

TRUST_LINKS = (
    ("About", "/about/"),
    ("Sources and methodology", "/sources/"),
    ("Update policy", "/update-policy/"),
    ("Contact", "/contact/"),
    ("Privacy", "/privacy/"),
    ("Disclaimer", "/disclaimer/"),
)

PAGES = {
    "about": {
        "title": "About WuWa Banners | Wuthering Waves Banner Tracker",
        "description": "Learn what WuWa Banners tracks, who the site is for, and how banner facts are separated from speculation.",
        "heading": "About WuWa Banners",
        "lead": "WuWa Banners is an independent reference site for Wuthering Waves banner timing, history, pull planning, and account decisions.",
        "answer": "The site exists to make banner decisions easier to check: what is live, what is confirmed next, what happened before, and what still needs an official source.",
        "sections": [
            ("What the site covers", ["The main site tracks current and historical Resonator and weapon Convene information, official update signals, phase dates, pity planning, and practical pull decisions.", "Pages are organized by user intent. Banner pages answer timing questions, history pages preserve confirmed context, and guide pages connect a character or resource to a spending decision."]),
            ("What the site does not claim", ["WuWa Banners is not operated by Kuro Games and does not present leaks, community guesses, or feed version numbers as confirmed banner facts.", "When an official notice confirms only a release or character reveal, the site records that as news and keeps the dated banner dataset unchanged until the missing timing or lineup detail is directly verifiable."]),
            ("Who maintains it", ["The site is maintained as a small static publishing project. Data is reviewed against official notices and high-signal public sources, then rebuilt into crawlable HTML.", "If you find a factual error, a stale date, or a broken source link, please use the contact page with the affected URL and the evidence for the correction."]),
        ],
    },
    "sources": {
        "title": "Sources and Methodology | WuWa Banners",
        "description": "See how WuWa Banners verifies banner dates, lineups, weapons, official news, and uncertain future information.",
        "heading": "Sources and editorial methodology",
        "lead": "The site separates confirmed banner data from official news, source-health signals, and speculation so each page can state what is known.",
        "answer": "A banner row is published as confirmed only when its dates, lineup, or weapon facts can be checked against an official or otherwise high-signal source.",
        "sections": [
            ("Source priority", ["Official Wuthering Waves notices, official livestreams, official videos, and in-game Convene information have the highest priority.", "PlayStation Blog or other first-party platform notices can support version timing when they clearly state the relevant facts. Secondary media is treated as a review lead, not automatic confirmation."]),
            ("How uncertainty is handled", ["Possible version numbers from feeds, old pages, leaks, and community posts are not enough to change the banner CSV. Fetch failures and old last-checked dates are recorded as maintenance signals, not content updates.", "If an official notice confirms a character or update but omits exact phase timing, the site can publish a news note while leaving the dated banner schedule unchanged."]),
            ("Corrections and dates", ["Every important banner page shows the source used for its snapshot. Dates are displayed with the source's timezone or server-time wording when that is what the official notice provides.", "Corrections should include the page URL, the claim that is wrong, and a direct source. Unsupported predictions are not used to fill gaps in confirmed data."]),
        ],
    },
    "update-policy": {
        "title": "Update Policy | WuWa Banners",
        "description": "Read the WuWa Banners update policy for official-source checks, phase rollovers, corrections, and pending banner information.",
        "heading": "WuWa Banners update policy",
        "lead": "The site is updated when there is a meaningful factual change, not simply because a source was checked again.",
        "answer": "A real update means a confirmed date, lineup, weapon, phase transition, or useful official news item changed; source-health noise alone does not trigger a public release.",
        "sections": [
            ("Daily source checks", ["Official and high-signal sources are checked for new notices and possible banner changes. Automated candidates are reviewed before they can affect public pages.", "A fetch failure, an aging row, a changed last_checked date, or an unverified version signal is not treated as a banner update by itself."]),
            ("Phase transitions", ["When a confirmed phase starts or ends, the site rebuilds current and next routes from the existing confirmed dataset even if no new notice was published that day.", "This keeps current-banner pages aligned with the calendar without inventing a future lineup."]),
            ("Corrections", ["If a confirmed source changes or a published fact is shown to be wrong, the affected data and generated pages are corrected together. The correction should preserve the source trail and explain what changed."]),
        ],
    },
    "contact": {
        "title": "Contact WuWa Banners | Report a Correction",
        "description": "Contact WuWa Banners about banner corrections, broken links, source issues, or questions about the site's editorial method.",
        "heading": "Contact WuWa Banners",
        "lead": "Use this page to report a factual error, stale source, broken internal link, or accessibility problem on the site.",
        "answer": "The most useful report includes the page URL, the exact claim that needs attention, and a direct source or reproducible explanation.",
        "sections": [
            ("What to include", ["Please include the full page URL, the section or sentence that is incorrect, and the source that supports the correction. Screenshots can help when the source is in-game or temporarily unavailable in HTML.", "For a broken link, include the link text and the page where it appears. For an accessibility issue, include the device or browser if it affects reproduction."]),
            ("What is not treated as confirmation", ["Leaks, anonymous claims, prediction threads, and unsourced banner lists are welcome as discussion topics only; they are not sufficient evidence for changing confirmed banner data."]),
            ("Response expectations", ["This is an independent project rather than a live support channel. Corrections are reviewed against the source and may be incorporated in a later static rebuild."]),
        ],
    },
    "privacy": {
        "title": "Privacy Policy | WuWa Banners",
        "description": "Read the privacy information for WuWa Banners, including analytics, external media, and contact-related data handling.",
        "heading": "Privacy information",
        "lead": "This page explains the limited information used to understand site performance and how external services may load when you choose to use them.",
        "answer": "WuWa Banners is a static informational site; it does not require an account, login, or form submission to browse its banner pages.",
        "sections": [
            ("Analytics", ["The site may use Google Analytics to understand aggregate page visits, traffic sources, and basic performance. Analytics data is used to improve navigation and content priorities rather than to identify individual visitors."]),
            ("External services", ["Some pages link to official Wuthering Waves websites or YouTube. A video player or external page may load only after you choose to open it, and those services have their own privacy policies."]),
            ("Contact messages", ["If you contact the site through an available channel, the information you provide is used only to review and respond to the question or correction. Do not send passwords, payment details, or other sensitive information."]),
            ("Updates to this page", ["This policy may be updated when the site's analytics, contact, or external-media setup changes. The page should be reviewed alongside the site's update policy."]),
        ],
    },
    "disclaimer": {
        "title": "Disclaimer | WuWa Banners",
        "description": "Read the WuWa Banners independence, accuracy, affiliate, and official-source disclaimer.",
        "heading": "WuWa Banners disclaimer",
        "lead": "WuWa Banners is an independent fan reference site and is not affiliated with or endorsed by Kuro Games.",
        "answer": "Use the site for planning and reference, but confirm live in-game details and official notices before spending resources or money.",
        "sections": [
            ("Accuracy and timing", ["Banner dates, names, and lineups can change. The site aims to publish verifiable information, but no page should be treated as a guarantee of future game content.", "When a page labels information as pending, watch, or unconfirmed, that wording is intentional and should not be read as a prediction."]),
            ("Game and trademark ownership", ["Wuthering Waves, its characters, images, names, and trademarks belong to their respective owners. This site is an independent informational project."]),
            ("Spending decisions", ["Pull advice is editorial guidance, not financial advice. Consider your own account, pity state, budget, and preferences. Never spend money because a page creates urgency."]),
            ("External links", ["Links to official or third-party pages are provided for verification and context. WuWa Banners is not responsible for changes to those external pages."]),
        ],
    },
}


def render_page(slug: str, page: dict[str, object]) -> str:
    path = f"/{slug}/"
    sections = []
    for heading, paragraphs in page["sections"]:
        body = "\n".join(f"        <p>{html.escape(text)}</p>" for text in paragraphs)
        sections.append(f'    <section class="section"><h2>{html.escape(heading)}</h2>{body}</section>')
    trust_links = "<br>".join(f'<a href="{href}">{label}</a>' for label, href in TRUST_LINKS)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page["title"])}</title>
  <meta name="description" content="{html.escape(page["description"])}">
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="{html.escape(page["title"])}">
  <meta property="og:description" content="{html.escape(page["description"])}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(page["title"])}">
  <meta name="twitter:description" content="{html.escape(page["description"])}">
  <meta name="twitter:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{CSS_HREF}">
</head>
<body>
  {NAV}
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / {html.escape(page["heading"])}</div>
    <h1>{html.escape(page["heading"])}</h1>
    <p class="lead">{html.escape(page["lead"])}</p>
    <div class="answer-box"><strong>Direct answer:</strong> {html.escape(page["answer"])}</div>
{chr(10).join(sections)}
    <section class="section"><h2>Site information</h2><p>{trust_links}</p></section>
  </div></main>
  <script defer src="{JS_SRC}"></script>
{GTAG_SNIPPET}
</body>
</html>
'''


def main() -> int:
    for slug, page in PAGES.items():
        directory = ROOT / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(render_page(slug, page), encoding="utf-8")
    print(f"Built {len(PAGES)} trust and transparency pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
