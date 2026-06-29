#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_JSON = ROOT / "data" / "reference-images.json"
SITEMAP_XML = ROOT / "sitemap.xml"
ASSET_VERSION = "20260617-pd"
CSS_HREF = f"/assets/css/site.css?v={ASSET_VERSION}"
JS_SRC = f"/assets/js/site.js?v={ASSET_VERSION}"

GTAG_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-C73K15FD00"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-C73K15FD00');
</script>"""

FONT_STYLESHEET_URL = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap"
FONT_PRELOAD_BLOCK = f"""  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONT_STYLESHEET_URL}" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="{FONT_STYLESHEET_URL}" rel="stylesheet"></noscript>"""

NAV = '<header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>'


def should_preserve_character_hub(index_path: Path) -> bool:
    if not index_path.exists():
        return False
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    return "Guide Hub" in text


def load_payload() -> dict[str, list[dict[str, str]]]:
    if not DATA_JSON.exists():
        return {"characters": [], "weapons": [], "items": []}
    return json.loads(DATA_JSON.read_text(encoding="utf-8"))


def get_directory_label(kind: str) -> str:
    if kind == "characters":
        return "Characters"
    if kind == "weapons":
        return "Weapons"
    return "Items"


def get_neighbor_entries(entries: list[dict[str, str]], slug: str) -> tuple[dict[str, str] | None, dict[str, str] | None]:
    sorted_entries = sorted(entries, key=lambda item: item["name"].lower())
    for index, item in enumerate(sorted_entries):
        if item["slug"] != slug:
            continue
        previous_entry = sorted_entries[index - 1] if index > 0 else None
        next_entry = sorted_entries[index + 1] if index + 1 < len(sorted_entries) else None
        return previous_entry, next_entry
    return None, None


def render_neighbor_links(kind: str, previous_entry: dict[str, str] | None, next_entry: dict[str, str] | None) -> str:
    links = []
    if previous_entry:
        links.append(
            f'<li><a href="/wuthering-waves-{kind}/{previous_entry["slug"]}/">Previous: {previous_entry["name"]}</a></li>'
        )
    if next_entry:
        links.append(
            f'<li><a href="/wuthering-waves-{kind}/{next_entry["slug"]}/">Next: {next_entry["name"]}</a></li>'
        )
    links.append(f'<li><a href="/wuthering-waves-{kind}/">Back to {get_directory_label(kind)}</a></li>')
    return "".join(links)


def render_neighbor_cards(kind: str, previous_entry: dict[str, str] | None, next_entry: dict[str, str] | None) -> str:
    cards = []
    for label, entry in (("Previous", previous_entry), ("Next", next_entry)):
        if not entry:
            continue
        cards.append(
            f'''<a class="history-phase-nav-card" href="/wuthering-waves-{kind}/{entry["slug"]}/">
  <span class="history-phase-nav-label">{label} {get_directory_label(kind)[:-1]}</span>
  <strong>{entry["name"]}</strong>
  <span class="muted">Check the neighboring {get_directory_label(kind).lower()[:-1]} entry.</span>
</a>'''
        )
    if not cards:
        cards.append(f'<p class="muted">There is no neighboring entry on this side of the {get_directory_label(kind).lower()} list.</p>')
    return "".join(cards)


def get_detail_context(kind: str, name: str) -> tuple[str, str, str]:
    if kind == "characters":
        return (
            "Where to go next",
            f"If you are checking {name} for a banner decision, start with pull advice or the current banner list. If you only need the portrait and spelling, this page is enough.",
            '<a class="directory-link" href="/pull-advice/">Open pull advice</a><a class="directory-link" href="/wuthering-waves-current-banner-characters/">Current banner characters</a><a class="directory-link" href="/wuthering-waves-next-character/">Next character</a>',
        )
    if kind == "weapons":
        return (
            "Where this weapon fits",
            f"Use {name} as a quick weapon reference, then compare it with the live weapon banner or the character list if you are deciding whether it matters for your account.",
            '<a class="directory-link" href="/wuthering-waves-weapon-banner/">Weapon banner</a><a class="directory-link" href="/wuthering-waves-current-banner/">Current banner</a><a class="directory-link" href="/wuthering-waves-characters/">Character list</a>',
        )
    return (
        "Where this item fits",
        f"Use {name} as a quick resource reference. From here, jump back to characters, weapons, or timing pages if you are planning upgrades around a banner.",
        '<a class="directory-link" href="/wuthering-waves-pity-system/">Pity system</a><a class="directory-link" href="/wuthering-waves-characters/">Character list</a><a class="directory-link" href="/wuthering-waves-timeline/">Timeline</a>',
    )


def get_branch_map_rows(kind: str) -> str:
    if kind == "characters":
        return (
            '<tr><td>List</td><td><a href="/wuthering-waves-characters/">Characters</a></td><td>Scan the full character set.</td></tr>'
            '<tr><td>Profile</td><td>Character detail page</td><td>Confirm the character and choose the next relevant page.</td></tr>'
            '<tr><td>Decision</td><td><a href="/pull-advice/">Pull advice</a> or character support pages</td><td>Move into pull, materials, build, or team planning.</td></tr>'
        )
    if kind == "weapons":
        return (
            '<tr><td>List</td><td><a href="/wuthering-waves-weapons/">Weapons</a></td><td>Scan weapons by image or name.</td></tr>'
            '<tr><td>Profile</td><td>Weapon detail page</td><td>Confirm the weapon and compare nearby entries.</td></tr>'
            '<tr><td>Decision</td><td><a href="/wuthering-waves-weapon-banner/">Weapon banner</a> or related planning pages</td><td>Check banner context, character fit, or upgrade planning.</td></tr>'
        )
    return (
        '<tr><td>List</td><td><a href="/wuthering-waves-items/">Items</a></td><td>Scan materials and resource names.</td></tr>'
        '<tr><td>Profile</td><td>Item detail page</td><td>Confirm the item image and spelling.</td></tr>'
        '<tr><td>Planning</td><td><a href="/wuthering-waves-pity-system/">Pity system</a> or related planning pages</td><td>Connect the resource check back to banner spending or upgrades.</td></tr>'
    )


def get_branch_links(kind: str) -> str:
    if kind == "characters":
        hrefs = [
            ("/pull-advice/", "Pull advice hub"),
            ("/wuthering-waves-current-banner-characters/", "Current banner characters"),
            ("/wuthering-waves-next-character/", "Next character"),
            ("/wuthering-waves-current-banner/", "Current banner"),
            ("/wuthering-waves-next-banner/", "Next banner"),
        ]
    elif kind == "weapons":
        hrefs = [
            ("/wuthering-waves-weapon-banner/", "Weapon banner"),
            ("/wuthering-waves-current-banner/", "Current banner"),
            ("/wuthering-waves-next-banner/", "Next banner"),
            ("/wuthering-waves-characters/", "Characters"),
            ("/wuthering-waves-items/", "Items"),
        ]
    else:
        hrefs = [
            ("/wuthering-waves-pity-system/", "Pity system"),
            ("/wuthering-waves-characters/", "Characters"),
            ("/wuthering-waves-weapons/", "Weapons"),
            ("/wuthering-waves-current-banner/", "Current banner"),
            ("/wuthering-waves-timeline/", "Timeline"),
        ]
    return "".join(f'<a class="directory-link" href="{href}">{label}</a>' for href, label in hrefs)


def render_detail(kind: str, entry: dict[str, str], entries: list[dict[str, str]]) -> str:
    name = entry["name"]
    slug = entry["slug"]
    src = entry["src"]
    label = get_directory_label(kind)
    path = f"/wuthering-waves-{kind}/{slug}/"
    singular = "Character" if kind == "characters" else label[:-1]
    title = f"Wuthering Waves {name} {singular} | WuWa Banners"
    description = f"Check the Wuthering Waves {name} {singular.lower()} page for the image, exact name, and related banner planning links."
    robots_meta = ""
    previous_entry, next_entry = get_neighbor_entries(entries, slug)
    neighbor_cards = render_neighbor_cards(kind, previous_entry, next_entry)
    context_title, context_copy, context_links = get_detail_context(kind, name)
    if kind == "characters":
        related = '<li><a href="/pull-advice/">Pull advice</a></li><li><a href="/wuthering-waves-current-banner-characters/">Current banner characters</a></li><li><a href="/wuthering-waves-next-character/">Next character</a></li>'
        why = f"{name} gets a dedicated page so players can confirm the portrait and name without digging through the full character list."
        faq = f'<article class="faq-item"><h3>What is the best next page after {name}?</h3><p>Open pull advice if you are deciding whether to spend, or the current banner page if you need live phase context.</p></article>'
    elif kind == "weapons":
        related = '<li><a href="/wuthering-waves-weapon-banner/">Weapon banner</a></li><li><a href="/wuthering-waves-characters/">Characters</a></li><li><a href="/wuthering-waves-items/">Items</a></li>'
        why = f"{name} gets a dedicated page so players can confirm the weapon image and name before checking banner or character context."
        faq = f'<article class="faq-item"><h3>What is the best next page after {name}?</h3><p>Open the weapon banner page for live banner context, or the character list if you are checking possible character matches.</p></article>'
    else:
        related = '<li><a href="/wuthering-waves-items/">Items</a></li><li><a href="/wuthering-waves-characters/">Characters</a></li><li><a href="/wuthering-waves-weapons/">Weapons</a></li>'
        why = f"{name} gets a dedicated page so players can confirm the resource image and name before returning to character, weapon, or banner planning."
        faq = f'<article class="faq-item"><h3>What is the best next page after {name}?</h3><p>Open the item list to compare resources, or move to characters and weapons if you are planning upgrades.</p></article>'
    neighbor_links = render_neighbor_links(kind, previous_entry, next_entry)
    branch_map_rows = get_branch_map_rows(kind)
    branch_links = get_branch_links(kind)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  {robots_meta.strip()}
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net{src}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="https://wuwabanners.net{src}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="{CSS_HREF}">
</head>
<body>
  {NAV}
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="/wuthering-waves-{kind}/">{label}</a> / {name}</div>
    <h1>Wuthering Waves {name}</h1>
    <p class="lead">A quick reference for {name}: image, exact name, nearby entries, and the most useful banner links from here.</p>
    <div class="answer-box"><strong>Quick answer:</strong> Confirm {name} here, then use the links below if you need banner timing, pull advice, or related references.</div>
    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art" style="aspect-ratio:1 / 1;">
        <img src="{src}" alt="{name}" width="1200" height="1200" decoding="async">
      </div>
      <div class="card">
        <h2>Why this page is here</h2>
        <p>{why}</p>
        <p><a href="/wuthering-waves-{kind}/">Back to {label} list</a></p>
      </div>
    </div>
    <section class="section two-col">
      <div class="card">
        <h2>{context_title}</h2>
        <p>{context_copy}</p>
        <div class="reference-directory">
          {context_links}
        </div>
      </div>
      <div class="card">
        <h2>Visual reference</h2>
        <p>The image is here for quick recognition. If you already know {name}, skip to the related links below.</p>
      </div>
    </section>
    <section class="section two-col">
      <div class="card">
        <h2>Best next pages</h2>
        <ul class="list">
          {related}
        </ul>
      </div>
      <div class="card">
        <h2>Reference source</h2>
        <p>The image is stored locally with the site's reference gallery so the page stays fast and easy to scan.</p>
      </div>
    </section>
    <section class="section two-col">
      <div class="card">
        <h2>Directory navigation</h2>
        <ul class="list">
          {neighbor_links}
        </ul>
      </div>
      <div class="card">
        <h2>How to use this page</h2>
        <p>Start from the list when you are browsing. Open this page when you need one entry, then follow the related links if the question turns into banner or upgrade planning.</p>
      </div>
    </section>
    <section class="section">
      <h2>Browse nearby {label.lower()}</h2>
      <div class="history-phase-nav-grid">
        {neighbor_cards}
      </div>
    </section>
    <section class="section">
      <h2>{singular} page path</h2>
      <p class="section-intro">The page structure is simple: list, profile, then a decision or planning page if needed.</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Layer</th><th>Best page type</th><th>What it is for</th></tr></thead>
          <tbody>
            {branch_map_rows}
          </tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <h2>Related pages</h2>
      <p class="section-intro">These are the pages most likely to answer the next question after this entry.</p>
      <div class="reference-directory">
        {branch_links}
      </div>
    </section>
    <section class="section">
      <h2>FAQ</h2>
      <div class="faq-list">
        {faq}
        <article class="faq-item"><h3>Why is this page short?</h3><p>Most players need the image, the name, and the next useful link. Longer advice belongs on the banner, build, or planning pages.</p></article>
      </div>
    </section>
  </div></main>
  <script defer src="{JS_SRC}"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def main() -> int:
    payload = load_payload()
    for kind in ("characters", "weapons", "items"):
        entries = payload.get(kind, [])
        for entry in entries:
            page_dir = ROOT / f"wuthering-waves-{kind}" / entry["slug"]
            index_path = page_dir / "index.html"
            if kind == "characters" and should_preserve_character_hub(index_path):
                continue
            page_dir.mkdir(parents=True, exist_ok=True)
            index_path.write_text(render_detail(kind, entry, entries), encoding="utf-8")
    print("Built character, weapon, and item reference detail pages from data/reference-images.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
