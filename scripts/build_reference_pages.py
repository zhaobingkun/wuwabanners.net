#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_JSON = ROOT / "data" / "reference-images.json"
SITEMAP_XML = ROOT / "sitemap.xml"

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

NAV = '<header class="site-header"><div class="container nav"><a class="brand" href="/index.html"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/index.html">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>'


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


def render_detail(kind: str, entry: dict[str, str], entries: list[dict[str, str]]) -> str:
    name = entry["name"]
    slug = entry["slug"]
    src = entry["src"]
    label = get_directory_label(kind)
    path = f"/wuthering-waves-{kind}/{slug}/"
    singular = "Character" if kind == "characters" else label[:-1]
    title = f"Wuthering Waves {name} {singular} | WuWa Banners"
    description = f"Browse the Wuthering Waves {name} {singular.lower()} detail page with a clear image, related planning links, and a clean browser-first layout."
    previous_entry, next_entry = get_neighbor_entries(entries, slug)
    if kind == "characters":
        related = '<li><a href="/pull-advice/">Pull advice</a></li><li><a href="/wuthering-waves-current-banner-characters/">Current banner characters</a></li><li><a href="/wuthering-waves-next-character/">Next character</a></li>'
        why = f"{name} belongs inside the character planning branch, so this page should help users move between banner intent, pull decisions, and the broader character reference structure."
        faq = f'<article class="faq-item"><h3>What should a {name} character page do first?</h3><p>Show the portrait, the exact character name, and the fastest next pages for pull planning or banner context.</p></article>'
    elif kind == "weapons":
        related = '<li><a href="/wuthering-waves-weapon-banner/">Weapon banner</a></li><li><a href="/wuthering-waves-characters/">Characters</a></li><li><a href="/wuthering-waves-items/">Items</a></li>'
        why = f"{name} belongs inside the weapon planning branch, so this page should help users move between weapon banner context, character intent, and upgrade planning."
        faq = f'<article class="faq-item"><h3>What should a {name} weapon page do first?</h3><p>Show the image, the exact weapon name, and the fastest next pages for banner or build planning.</p></article>'
    else:
        related = '<li><a href="/wuthering-waves-items/">Items</a></li><li><a href="/wuthering-waves-characters/">Characters</a></li><li><a href="/wuthering-waves-weapons/">Weapons</a></li>'
        why = f"{name} belongs inside the item planning branch, so this page should help users move between resource intent, character growth, and weapon planning."
        faq = f'<article class="faq-item"><h3>What should a {name} item page do first?</h3><p>Show the item image, the exact item name, and the fastest next pages for materials, characters, or weapons.</p></article>'
    neighbor_links = render_neighbor_links(kind, previous_entry, next_entry)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net{src}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  {NAV}
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/index.html">Home</a> / <a href="/guides/">Guides</a> / <a href="/wuthering-waves-{kind}/">{label}</a> / {name}</div>
    <h1>Wuthering Waves {name}</h1>
    <p class="lead">This is a simple {singular.lower()} detail page that gives the image, the exact name, and the cleanest next links deeper into the site structure.</p>
    <div class="answer-box"><strong>Direct answer:</strong> Use this page as the detail layer for {name}, then move into the related planning pages that match what you are actually trying to decide.</div>
    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art" style="aspect-ratio:1 / 1;">
        <img src="{src}" alt="{name}" width="1200" height="1200" decoding="async">
      </div>
      <div class="card">
        <h2>Why this detail page exists</h2>
        <p>{why}</p>
        <p><a href="/wuthering-waves-{kind}/">Back to {label} list</a></p>
      </div>
    </div>
    <section class="section two-col">
      <div class="card">
        <h2>Best next pages</h2>
        <ul class="list">
          {related}
        </ul>
      </div>
      <div class="card">
        <h2>Reference source</h2>
        <p>This image was downloaded into the local reference gallery and published as part of the site's browser-friendly reference layer.</p>
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
        <h2>How to use this detail layer</h2>
        <p>Use this page as the middle layer in the structure: top navigation to the list page, then open a specific {singular.lower()} detail page, then continue into banners, characters, or materials planning.</p>
      </div>
    </section>
    <section class="section">
      <h2>FAQ</h2>
      <div class="faq-list">
        {faq}
        <article class="faq-item"><h3>Why keep this page lightweight?</h3><p>Because this detail layer is mainly here to support the list-to-detail structure and give gallery clicks a clean destination.</p></article>
      </div>
    </section>
  </div></main>
  <script defer src="/assets/js/site.js"></script>
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
            if kind == "characters" and index_path.exists():
                continue
            page_dir.mkdir(parents=True, exist_ok=True)
            index_path.write_text(render_detail(kind, entry, entries), encoding="utf-8")
    print("Built character, weapon, and item reference detail pages from data/reference-images.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
