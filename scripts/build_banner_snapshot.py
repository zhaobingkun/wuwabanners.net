#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "banner-data.csv"
DATA_JSON = ROOT / "data" / "banner-snapshot.json"
REFERENCE_JSON = ROOT / "data" / "reference-images.json"
IMG_DIR = ROOT / "assets" / "img"
INDEX_HTML = ROOT / "index.html"
NEXT_HTML = ROOT / "wuthering-waves-next-banner" / "index.html"
CURRENT_HTML = ROOT / "wuthering-waves-current-banner" / "index.html"
HISTORY_HTML = ROOT / "wuthering-waves-banner-history" / "index.html"
RERUN_HTML = ROOT / "wuthering-waves-next-rerun" / "index.html"
COUNTDOWN_HTML = ROOT / "wuthering-waves-banner-countdown" / "index.html"
NEXT_COUNTDOWN_HTML = ROOT / "wuthering-waves-next-banner-countdown" / "index.html"
NEXT_DATE_HTML = ROOT / "wuthering-waves-next-banner-date" / "index.html"
CURRENT_END_HTML = ROOT / "wuthering-waves-current-banner-end-date" / "index.html"
CURRENT_CHARACTERS_HTML = ROOT / "wuthering-waves-current-banner-characters" / "index.html"
NEXT_CHARACTER_HTML = ROOT / "wuthering-waves-next-character" / "index.html"
SCHEDULE_HTML = ROOT / "wuthering-waves-banner-schedule" / "index.html"
ORDER_HTML = ROOT / "wuthering-waves-banner-order" / "index.html"
PULL_HUB_HTML = ROOT / "pull-advice" / "index.html"
SITEMAP_XML = ROOT / "sitemap.xml"
BANNERS_HUB_HTML = ROOT / "banners" / "index.html"
GUIDES_HUB_HTML = ROOT / "guides" / "index.html"
CHARACTERS_HUB_HTML = ROOT / "wuthering-waves-characters" / "index.html"

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


def render_video_embed(title: str, video_id: str = "viOkAhoa0k8") -> str:
    safe_title = html.escape(title)
    watch_url = f"https://www.youtube.com/watch?v={video_id}"
    poster_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    return f"""<div class="video-embed">
            <button class="video-lite" type="button" data-video-id="{video_id}" data-video-title="{safe_title}" aria-label="Load video: {safe_title}">
              <img src="{poster_url}" alt="{safe_title}" loading="lazy" decoding="async">
              <span class="video-lite-badge">YouTube</span>
              <span class="video-lite-play" aria-hidden="true"></span>
              <span class="video-lite-title">{safe_title}</span>
              <span class="video-lite-note">Click to load the YouTube player.</span>
            </button>
            <noscript><p class="muted" style="padding:1rem;">JavaScript is off. <a href="{watch_url}">Watch this video on YouTube</a>.</p></noscript>
          </div>"""


def render_reference_video_embed() -> str:
    return render_video_embed("Official Wuthering Waves update reference")

BASE_URLS = [
    "https://wuwabanners.net/",
    "https://wuwabanners.net/banners/",
    "https://wuwabanners.net/guides/",
    "https://wuwabanners.net/wuthering-waves-next-banner/",
    "https://wuwabanners.net/wuthering-waves-current-banner/",
    "https://wuwabanners.net/wuthering-waves-banner-history/",
    "https://wuwabanners.net/wuthering-waves-pity-system/",
    "https://wuwabanners.net/wuthering-waves-next-rerun/",
    "https://wuwabanners.net/wuthering-waves-banner-countdown/",
    "https://wuwabanners.net/wuthering-waves-banner-schedule/",
    "https://wuwabanners.net/wuthering-waves-weapon-banner/",
    "https://wuwabanners.net/wuthering-waves-all-banners/",
    "https://wuwabanners.net/wuthering-waves-next-character/",
    "https://wuwabanners.net/wuthering-waves-timeline/",
    "https://wuwabanners.net/wuthering-waves-daily-reset-time/",
    "https://wuwabanners.net/wuthering-waves-weekly-reset-time/",
    "https://wuwabanners.net/wuthering-waves-event-calendar/",
    "https://wuwabanners.net/wuthering-waves-banner-order/",
    "https://wuwabanners.net/wuthering-waves-current-banner-characters/",
    "https://wuwabanners.net/wuthering-waves-next-banner-date/",
    "https://wuwabanners.net/wuthering-waves-current-banner-end-date/",
    "https://wuwabanners.net/wuthering-waves-next-banner-countdown/",
    "https://wuwabanners.net/wuthering-waves-items/",
    "https://wuwabanners.net/wuthering-waves-weapons/",
    "https://wuwabanners.net/wuthering-waves-characters/",
    "https://wuwabanners.net/pull-advice/",
]


def load_rows() -> list[dict[str, str]]:
    with DATA_CSV.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def split_field(value: str) -> list[str]:
    return [part.strip() for part in value.split("|") if part.strip()]


def load_reference_payload() -> dict[str, list[dict[str, str]]]:
    if not REFERENCE_JSON.exists():
        return {"characters": [], "weapons": [], "items": []}
    return json.loads(REFERENCE_JSON.read_text(encoding="utf-8"))


REFERENCE_PAYLOAD = load_reference_payload()


def slugify_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-")


def get_reference_src(kind: str, name: str) -> str | None:
    for entry in REFERENCE_PAYLOAD.get(kind, []):
        if entry.get("name") == name:
            return entry.get("src")
    wanted = slugify_name(name)
    for entry in REFERENCE_PAYLOAD.get(kind, []):
        if entry.get("slug") == wanted:
            return entry.get("src")
    return None


DEFAULT_VISUALS = {
    "characters": "/assets/img/reference/characters/cantarella.webp",
    "weapons": "/assets/img/reference/weapons/frostburn.png",
    "items": "/assets/img/reference/items/platinum-core.webp",
}


def get_visual_src(kind: str, names: list[str]) -> str:
    for name in names:
        if not name:
            continue
        src = get_reference_src(kind, name)
        if src:
            return src
    return DEFAULT_VISUALS[kind]


def render_phase_collage(main_src: str, main_label: str, side_tiles: list[tuple[str, str, bool]]) -> str:
    side_html = []
    for src, label, is_artifact in side_tiles:
        artifact_class = " hub-hero-tile--artifact" if is_artifact else ""
        side_html.append(
            f'''          <figure class="hub-hero-tile hub-hero-tile--wide{artifact_class}">
            <img src="{src}" alt="" width="512" height="512" decoding="async">
            <span class="hub-hero-label">{html.escape(label)}</span>
          </figure>'''
        )
    return f"""<div class="phase-collage" aria-hidden="true">
          <figure class="hub-hero-tile hub-hero-tile--major">
            <img src="{main_src}" alt="" width="512" height="512" decoding="async">
            <span class="hub-hero-label">{html.escape(main_label)}</span>
          </figure>
          <div class="phase-collage-stack">
{chr(10).join(side_html)}
          </div>
        </div>"""


def render_history_entity_strip(kind: str, names: list[str]) -> str:
    cards = []
    variant = "weapon" if kind == "weapons" else "character"
    for name in names:
        src = get_reference_src(kind, name)
        if src:
            cards.append(
                f'<figure class="history-entity {variant}"><div class="history-thumb"><img src="{src}" alt="{html.escape(name)}" loading="lazy" decoding="async"></div><figcaption>{html.escape(name)}</figcaption></figure>'
            )
        else:
            cards.append(
                f'''<figure class="history-entity {variant} history-entity-placeholder">
  <div class="history-thumb"><span class="history-placeholder-label">{html.escape("Art pending")}</span></div>
  <figcaption>{html.escape(name)}</figcaption>
</figure>'''
            )
    return "".join(cards)


def parse_date(value: str) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value.split(" ")[0])


def latest_checked(rows: list[dict[str, str]]) -> date:
    values = [parse_date(row["last_checked"]) for row in rows if row.get("last_checked")]
    picked = max((value for value in values if value is not None), default=None)
    if picked is None:
        raise RuntimeError("No valid last_checked values found in banner-data.csv")
    return picked


def version_sort_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def phase_sort_key(phase: str) -> int:
    match = re.search(r"\d+", phase)
    return int(match.group(0)) if match else 0


def row_sort_key(row: dict[str, str]) -> tuple[tuple[int, ...], int]:
    return version_sort_key(row["version"]), phase_sort_key(row["phase"])


def pick_current_and_next(rows: list[dict[str, str]], updated: date) -> tuple[dict[str, str], dict[str, str], list[dict[str, str]]]:
    char_rows = [
        row
        for row in rows
        if row["banner_type"] == "character" and row["start_date"] and row["end_date"] and row["status"] in {"official", "expected"}
    ]
    char_rows.sort(key=lambda row: parse_date(row["start_date"]) or date.max)
    if not char_rows:
        raise RuntimeError("No character banner rows with dates found in banner-data.csv")
    preview_rows = [
        row
        for row in rows
        if row["banner_type"] == "preview" and row["status"] in {"official", "expected"}
    ]
    preview_rows.sort(key=row_sort_key)

    current_row = next(
        (
            row
            for row in char_rows
            if (parse_date(row["start_date"]) or date.min) <= updated <= (parse_date(row["end_date"]) or date.max)
        ),
        None,
    )
    if current_row is None:
        past = [row for row in char_rows if (parse_date(row["start_date"]) or date.min) <= updated]
        current_row = past[-1] if past else char_rows[0]

    current_index = char_rows.index(current_row)
    next_row = char_rows[current_index + 1] if current_index + 1 < len(char_rows) else None
    if next_row is None:
        current_key = row_sort_key(current_row)
        next_row = next((row for row in preview_rows if row_sort_key(row) > current_key), None)
    if next_row is None:
        next_row = current_row
    if current_index + 1 < len(char_rows):
        history_rows = char_rows[max(0, current_index - 1) : min(len(char_rows), current_index + 2)]
    else:
        history_rows = char_rows[max(0, len(char_rows) - 3) :]
    return current_row, next_row, history_rows


def find_weapon_row(rows: list[dict[str, str]], version: str, phase: str) -> dict[str, str] | None:
    for row in rows:
        if row["banner_type"] == "weapon" and row["version"] == version and row["phase"] == phase:
            return row
    return None


def build_snapshot(rows: list[dict[str, str]]) -> dict[str, object]:
    updated = latest_checked(rows)
    current_char, next_char, history_rows = pick_current_and_next(rows, updated)
    current_weapon = find_weapon_row(rows, current_char["version"], current_char["phase"])
    next_weapon = find_weapon_row(rows, next_char["version"], next_char["phase"])

    return {
        "updated": updated.isoformat(),
        "current": {
            "version": current_char["version"],
            "phase": current_char["phase"],
            "banner_type": current_char["banner_type"],
            "banner_name": current_char["banner_name"],
            "featured_characters": split_field(current_char["featured_characters"]),
            "featured_weapons": split_field(current_weapon["featured_weapons"]) if current_weapon else [],
            "start_date": current_char["start_date"],
            "end_date": current_char["end_date"],
            "source_url": current_char["source_url"],
            "announcement_date": current_char["announcement_date"],
            "status": current_char["status"],
        },
        "next": {
            "version": next_char["version"],
            "phase": next_char["phase"],
            "banner_type": next_char["banner_type"],
            "banner_name": next_char["banner_name"],
            "featured_characters": split_field(next_char["featured_characters"]),
            "featured_weapons": split_field(next_weapon["featured_weapons"]) if next_weapon else [],
            "start_date": next_char["start_date"],
            "end_date": next_char["end_date"],
            "source_url": next_char["source_url"],
            "announcement_date": next_char["announcement_date"],
            "status": next_char["status"],
        },
        "history": [
            {
                "version": row["version"],
                "phase": row["phase"],
                "banner_name": row["banner_name"],
                "featured_characters": split_field(row["featured_characters"]),
                "featured_weapons": split_field(find_weapon_row(rows, row["version"], row["phase"])["featured_weapons"]) if find_weapon_row(rows, row["version"], row["phase"]) else [],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "source_url": row["source_url"],
            }
            for row in history_rows
        ],
    }


def write_json(snapshot: dict[str, object]) -> None:
    DATA_JSON.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_svg(path: Path, title: str, desc: str, gradient_start: str, gradient_end: str, lines: list[str], footer: str) -> None:
    safe_lines = [html.escape(line) for line in lines]
    line_y = 325
    text_lines = []
    for line in safe_lines[1:]:
        text_lines.append(
            f'  <text x="95" y="{line_y}" fill="#ffffff" font-family="IBM Plex Sans, Arial, sans-serif" font-size="34">{line}</text>'
        )
        line_y += 55
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc">
  <title id="title">{html.escape(title)}</title>
  <desc id="desc">{html.escape(desc)}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gradient_start}"/>
      <stop offset="100%" stop-color="{gradient_end}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="#f5f1e8"/>
  <rect x="50" y="50" width="1100" height="575" rx="34" fill="url(#bg)"/>
  <text x="95" y="150" fill="#dff5f1" font-family="Space Grotesk, Arial, sans-serif" font-size="34" font-weight="700">{html.escape(title.upper())}</text>
  <text x="95" y="245" fill="#ffffff" font-family="Space Grotesk, Arial, sans-serif" font-size="64" font-weight="700">{safe_lines[0]}</text>
{chr(10).join(text_lines)}
  <text x="95" y="585" fill="#dff5f1" font-family="IBM Plex Sans, Arial, sans-serif" font-size="24">{html.escape(footer)}</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def write_cards(snapshot: dict[str, object]) -> None:
    current = snapshot["current"]
    next_item = snapshot["next"]
    recent = snapshot["history"]

    write_svg(
        IMG_DIR / "current-banner-card.svg",
        "Current Banner",
        "Current Wuthering Waves banner snapshot generated from CSV.",
        "#0f9b8e",
        "#15504c",
        [
            current["banner_name"],
            ", ".join(current["featured_characters"]),
            "Weapons: " + ", ".join(current["featured_weapons"]),
            fmt_human_date(current["end_date"]) + " end date",
        ],
        "Refresh from banner-data.csv before publishing banner updates.",
    )
    write_svg(
        IMG_DIR / "next-banner-card.svg",
        "Next Banner",
        "Next Wuthering Waves banner snapshot generated from CSV.",
        "#db6c57",
        "#66352c",
        [
            next_item["banner_name"],
            next_character_copy(next_item),
            "Weapons: " + next_weapon_copy(next_item),
            phase_window_label(next_item),
        ],
        "Keep next banner pages tied to official preview or in-game Convene updates.",
    )
    write_svg(
        IMG_DIR / "banner-history-card.svg",
        "Banner History",
        "Recent Wuthering Waves banner flow generated from CSV.",
        "#5667d8",
        "#242b65",
        [
            "Recent Version Flow",
            f'{recent[0]["version"]} {recent[0]["phase"]}: ' + ", ".join(recent[0]["featured_characters"]),
            f'{recent[-2]["version"]} {recent[-2]["phase"]}: ' + ", ".join(recent[-2]["featured_characters"]) if len(recent) > 1 else "",
            f'{recent[-1]["version"]} {recent[-1]["phase"]}: ' + ", ".join(recent[-1]["featured_characters"]),
        ],
        "Use the full table on-site for rerun timing and phase spacing.",
    )


def fmt_human_date(value: str) -> str:
    year, month, day = value.split(" ")[0].split("-")
    month_names = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    return f"{month_names[month]} {int(day)}, {year}"


def join_or_fallback(values: list[str], fallback: str) -> str:
    return ", ".join(values) if values else fallback


def is_preview_phase(phase: dict[str, object]) -> bool:
    return str(phase.get("banner_type") or "") == "preview"


def phase_event_date(phase: dict[str, object]) -> str:
    start_date = str(phase.get("start_date") or "")
    if start_date:
        return start_date
    announcement_date = str(phase.get("announcement_date") or "")
    return f"{announcement_date} 00:00" if announcement_date else ""


def phase_event_label(phase: dict[str, object]) -> str:
    event_date = phase_event_date(phase)
    return fmt_human_date(event_date) if event_date else "TBA"


def phase_window_label(phase: dict[str, object]) -> str:
    if is_preview_phase(phase):
        event_label = phase_event_label(phase)
        return f"Preview broadcast on {event_label}" if event_label != "TBA" else "Preview timing pending"
    start_date = str(phase.get("start_date") or "")
    end_date = str(phase.get("end_date") or "")
    if start_date and end_date:
        return f"{fmt_human_date(start_date)} to {fmt_human_date(end_date)}"
    if start_date:
        return f"Starts {fmt_human_date(start_date)}"
    return "TBA"


def next_character_copy(next_item: dict[str, object]) -> str:
    return join_or_fallback(
        list(next_item["featured_characters"]),
        "full featured characters are still unconfirmed before the next official preview",
    )


def next_weapon_copy(next_item: dict[str, object]) -> str:
    return join_or_fallback(
        list(next_item["featured_weapons"]),
        "weapon details are still unconfirmed before the next official preview",
    )


def next_event_copy(next_item: dict[str, object]) -> str:
    if is_preview_phase(next_item):
        event_label = phase_event_label(next_item)
        if event_label == "TBA":
            return f"The next tracked official update is {next_item['banner_name']}, but its broadcast timing has not been posted yet."
        return f"The next tracked official update is {next_item['banner_name']} on {event_label}."
    return f"{next_item['banner_name']} is scheduled to begin on {fmt_human_date(str(next_item['start_date']))}."


def next_focus_name(next_item: dict[str, object]) -> str:
    if next_item["featured_characters"]:
        return str(next_item["featured_characters"][0])
    return "the first officially revealed 3.4 featured unit"


def replace_block_exact(text: str, name: str, inner: str) -> str:
    pattern = re.compile(rf"(<!-- AUTO:{name} -->)(.*?)(<!-- /AUTO:{name} -->)", re.S)
    new_text, count = pattern.subn(f"<!-- AUTO:{name} -->\n{inner}\n<!-- /AUTO:{name} -->", text, count=1)
    if count != 1:
        raise RuntimeError(f"Failed to replace block {name}")
    return new_text


def slugify_character(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise RuntimeError(f"Unable to slugify character name: {name}")
    return slug


def build_home_media(updated: str) -> str:
    return f"""      <div class="container media-grid">
        <div class="banner-art">
          <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves banner snapshot generated from the latest CSV build." width="1200" height="675" decoding="async" fetchpriority="high">
        </div>
        <div class="video-card">
          <h2>Official update video slot</h2>
          <p class="section-intro">Use one official broadcast or trailer on the homepage. This keeps the front page visually stronger without turning the site into a video-first layout.</p>
          {render_reference_video_embed()}
        </div>
      </div>"""


def build_home_update(updated: str) -> str:
    return f'        <p class="update-stamp">Snapshot updated for {fmt_human_date(updated + " 00:00")}. Current and next banner values should be rechecked against official notices and in-game Convene at every phase change.</p>'


def build_home_timeline(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    history = snapshot["history"]
    recent = history[0]
    next_card_title = "Next banner starts" if not is_preview_phase(next_item) else "Next official preview"
    next_card_body = (
        f"{next_character_copy(next_item)} are the next tracked featured characters."
        if next_item["featured_characters"]
        else "The next full lineup is still pending the next official preview reveal."
    )
    next_row_type = "Next banner phase" if not is_preview_phase(next_item) else "Next official preview"
    return f"""      <div class="container">
        <h2>Current timeline snapshot</h2>
        <p class="section-intro">Start with the live phase, the next phase, and the most important pull timing details first. This gives homepage visitors the fastest way to understand what is live now, what ends next, and when the next saving or pull decision matters.</p>
        <div class="card-grid" style="margin-bottom:1.25rem;">
          <article class="card"><h3>Current banner ends</h3><p><strong>{fmt_human_date(current["end_date"])}</strong></p><p>{", ".join(current["featured_characters"])} stay live through the current tracked phase.</p><p><a href="/wuthering-waves-current-banner-end-date/">Open current banner end date</a></p></article>
          <article class="card"><h3>{next_card_title}</h3><p><strong>{phase_event_label(next_item)}</strong></p><p>{next_card_body}</p><p><a href="/wuthering-waves-next-banner-date/">Open next banner date</a></p></article>
          <article class="card"><h3>Fastest pull path</h3><p><strong>{current["banner_name"]} vs {next_item["banner_name"]}</strong></p><p>Use the live phase if you need to spend now. Use the next phase if you are deciding whether to save.</p><p><a href="/pull-advice/">Open pull advice</a></p></article>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Type</th><th>Name</th><th>Window</th><th>Best next page</th></tr></thead>
            <tbody>
              <tr><td>Live banner phase</td><td>{current["banner_name"]}</td><td>{fmt_human_date(current["start_date"])} to {fmt_human_date(current["end_date"])}</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td></tr>
              <tr><td>{next_row_type}</td><td>{next_item["banner_name"]}</td><td>{phase_window_label(next_item)}</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
              <tr><td>Recent reference</td><td>{recent["banner_name"]}</td><td>{fmt_human_date(recent["start_date"])} to {fmt_human_date(recent["end_date"])}</td><td><a href="/wuthering-waves-banner-history/">Banner history</a></td></tr>
            </tbody>
          </table>
        </div>
      </div>"""


def build_next_intro(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    updated = snapshot["updated"]
    if is_preview_phase(next_item):
        answer = (
            f"""      <p class="lead">As of {fmt_human_date(updated + " 00:00")}, the active Wuthering Waves banners are in {current["banner_name"]}. The next tracked official banner-related update is {next_item["banner_name"]}, which is the best placeholder until the next full phase is officially announced.</p>
      <div class="answer-box"><strong>Direct answer:</strong> The current {current["banner_name"]} banners feature {", ".join(current["featured_characters"])} through {fmt_human_date(current["end_date"])}. {next_event_copy(next_item)} The full next featured-character lineup is still unconfirmed.</div>"""
        )
    else:
        answer = (
            f"""      <p class="lead">As of {fmt_human_date(updated + " 00:00")}, the active Wuthering Waves banners are in {current["banner_name"]}, while the next banner rotation is {next_item["banner_name"]} scheduled to begin on {fmt_human_date(next_item["start_date"])}. This page combines a live-style snapshot with the structure needed for long-term updates: current banner, next banner, countdown logic, and pull-or-save context.</p>
      <div class="answer-box"><strong>Direct answer:</strong> The current {current["banner_name"]} banners feature {", ".join(current["featured_characters"])} through {fmt_human_date(current["end_date"])}. The next {next_item["banner_name"]} banners are {", ".join(next_item["featured_characters"])}, with the next phase expected to begin on {fmt_human_date(next_item["start_date"])}.</div>"""
        )
    return f"""{answer}
      <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_next_media(snapshot: dict[str, object]) -> str:
    next_item = snapshot["next"]
    return f"""      <div class="media-grid" style="margin-top:1.25rem;">
        <div class="banner-art">
          <img src="/assets/img/next-banner-card.svg" alt="Next Wuthering Waves banner snapshot for {next_item["banner_name"]}." width="1200" height="675" decoding="async">
        </div>
        <div class="video-card">
          <h2>Official preview media</h2>
          <p class="muted">Keep one official preview video on the page and let the text carry the primary answer.</p>
          {render_reference_video_embed()}
        </div>
      </div>"""


def build_next_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    next_snapshot = (
        f"The next phase is {next_item['banner_name']}. The featured five-stars are {', '.join(next_item['featured_characters'])}, and the weapon focus is {', '.join(next_item['featured_weapons'])}."
        if not is_preview_phase(next_item)
        else f"{next_event_copy(next_item)} The full character and weapon lineup is still pending official confirmation."
    )
    return f"""      <div class="card-grid">
        <article class="card"><h2>Current live phase</h2><p>{current["banner_name"]} is live right now. The featured five-stars are {", ".join(current["featured_characters"])}, and the weapon focus is {", ".join(current["featured_weapons"])}.</p></article>
        <article class="card"><h2>Next phase snapshot</h2><p>{next_snapshot}</p></article>
        <article class="card"><h2>What users want first</h2><p>Users usually want four facts first: the live banner, the next banner, the end date, and whether the next phase is already official. If those four are missing, the page feels slow even when it has more words.</p></article>
      </div>"""


def build_next_table(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""        <h2>Current and next banner snapshot</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Status</th><th>Banner group</th><th>5-star focus</th><th>Weapon focus</th><th>Dates</th></tr></thead>
            <tbody>
              <tr><td>Current</td><td>{current["banner_name"]}</td><td>{", ".join(current["featured_characters"])}</td><td>{", ".join(current["featured_weapons"])}</td><td>{fmt_human_date(current["start_date"])} to {fmt_human_date(current["end_date"])}</td></tr>
              <tr><td>Next</td><td>{next_item["banner_name"]}</td><td>{next_character_copy(next_item)}</td><td>{next_weapon_copy(next_item)}</td><td>{phase_window_label(next_item)}</td></tr>
            </tbody>
          </table>
        </div>"""


def build_next_pull(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    if is_preview_phase(next_item):
        wait_copy = f"wait for {next_item['banner_name']} before locking the next save target"
        weapon_copy = "The next weapon group is still unconfirmed until the next official preview reveals more detail."
    else:
        wait_copy = f"consider waiting if {', '.join(next_item['featured_characters'])} better matches your roster direction"
        weapon_copy = f"The next weapon group is {', '.join(next_item['featured_weapons'])} in the next phase."
    return f"""        <div class="card">
          <h2>Should you pull now or wait?</h2>
          <p>For a new or lightly built account, the key question is whether {", ".join(current["featured_characters"])} fills an urgent team hole before {current["banner_name"]} ends. For users already saving for {next_focus_name(next_item)} or a later rerun, the page should say that clearly instead of forcing them to infer it from the table.</p>
          <ul class="list">
            <li><strong>Pull now:</strong> if the current phase solves an immediate roster need.</li>
            <li><strong>Consider waiting:</strong> if {wait_copy}.</li>
            <li><strong>Save harder:</strong> if your main goal is a future rerun or a later patch target.</li>
          </ul>
        </div>
        <div class="card">
          <h2>Weapon banner snapshot</h2>
          <p>The current weapon focus is {", ".join(current["featured_weapons"])} through {fmt_human_date(current["end_date"])}. {weapon_copy}</p>
          <ul class="list">
            <li><strong>Character-first accounts:</strong> compare roster gain before comparing weapon upside.</li>
            <li><strong>Weapon-first accounts:</strong> check whether the current or next weapon set creates the bigger pity trap.</li>
            <li><strong>Do not skip this check:</strong> one character plan can still fail if the weapon side is too expensive.</li>
          </ul>
          <p><a href="/wuthering-waves-pity-system/">Check pity carry-over before spending more tides</a></p>
        </div>"""


def build_next_compare_matrix(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    save_watch = next_character_copy(next_item) if next_item["featured_characters"] else next_item["banner_name"]
    weapon_watch = (
        f"{', '.join(current['featured_weapons'])} vs {', '.join(next_item['featured_weapons'])}"
        if next_item["featured_weapons"]
        else f"{', '.join(current['featured_weapons'])} vs next-phase weapon reveal"
    )
    return f"""        <h2>Current versus next banner decision matrix</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Decision path</th><th>When it wins</th><th>Watch first</th><th>Best next page</th></tr></thead>
            <tbody>
              <tr><td>Spend in {current["banner_name"]}</td><td>The live phase solves an immediate account hole faster than waiting.</td><td>{", ".join(current["featured_characters"])}</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td></tr>
              <tr><td>Save for {next_item["banner_name"]}</td><td>The next tracked update matches your planned roster better than the current rotation.</td><td>{save_watch}</td><td><a href="/pull-advice/">Pull advice</a></td></tr>
              <tr><td>Spend only after checking weapon risk</td><td>Your character choice looks clear, but the weapon side could still make the full plan too expensive.</td><td>{weapon_watch}</td><td><a href="/wuthering-waves-weapon-banner/">Weapon banner</a></td></tr>
              <tr><td>Delay both phases</td><td>Your real target is a rerun or your pity state is too valuable to force a spend now.</td><td>History spacing and pity carry-over</td><td><a href="/wuthering-waves-next-rerun/">Next rerun</a></td></tr>
            </tbody>
          </table>
        </div>"""


def build_next_sources(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""        <div class="sources">
          <strong>Sources used for this {fmt_human_date(updated + " 00:00")} snapshot</strong><br>
          Current phase source: {current["source_url"]}<br>
          Next phase source: {next_item["source_url"]}<br>
          Official video archive: https://www.youtube.com/@WutheringWaves
        </div>"""


def build_current_intro(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = snapshot["updated"]
    return f"""    <p class="lead">As of {fmt_human_date(updated + " 00:00")}, Wuthering Waves is in {current["banner_name"]}. The live featured five-stars are {", ".join(current["featured_characters"])}, with the phase ending on {fmt_human_date(current["end_date"])}.</p>
    <div class="answer-box"><strong>Direct answer:</strong> The current {current["banner_name"]} banners feature {", ".join(current["featured_characters"])} through {fmt_human_date(current["end_date"])}.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_current_media(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    return f"""    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves banner snapshot for {current["banner_name"]}." width="1200" height="675" decoding="async">
      </div>
      <div class="video-card">
        <h2>Official update media slot</h2>
        <p class="muted">Use the preview broadcast or official trailer to support the page visually, but keep the live answer in text above it.</p>
        {render_reference_video_embed()}
      </div>
    </div>"""


def build_current_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    return f"""    <div class="card-grid">
      <article class="card"><h2>Live status matters more than speculation</h2><p>Users on the current banner page care more about what is active now than what might happen later. That means the live box, dates, and role summary should stay at the top.</p></article>
      <article class="card"><h2>Current phase snapshot</h2><p>The featured five-star lineup is {", ".join(current["featured_characters"])}. The companion weapon focus is {", ".join(current["featured_weapons"])} through {fmt_human_date(current["end_date"])}.</p></article>
      <article class="card"><h2>Do not judge current value in isolation</h2><p>The live phase only makes sense after you compare pity protection, weapon pressure, and whether the next tracked phase solves the same job with lower resource strain.</p></article>
      <article class="card"><h2>What to link next</h2><p>After checking the current banner, users usually need the next banner, pity system, or a pull advice page. Those are the highest-value internal links.</p></article>
    </div>"""


def build_current_table(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    return f"""      <h2>Current banner snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Banner type</th><th>Featured 5-stars</th><th>Featured 5-star weapons</th><th>Dates</th></tr></thead>
          <tbody>
            <tr><td>{current["banner_name"]}</td><td>{", ".join(current["featured_characters"])}</td><td>{", ".join(current["featured_weapons"])}</td><td>{fmt_human_date(current["start_date"])} to {fmt_human_date(current["end_date"])}</td></tr>
          </tbody>
        </table>
      </div>"""


def build_current_decision_matrix(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    why_copy = (
        "The next official preview may change your longer plan, so compare before locking a live spend."
        if is_preview_phase(next_item)
        else "The next phase may match your longer plan better than the live one."
    )
    return f"""        <h2>Spend-now versus save-now matrix</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Account state</th><th>Safer choice</th><th>Why</th><th>Best next page</th></tr></thead>
            <tbody>
              <tr><td>You need immediate value</td><td>Spend in {current["banner_name"]}</td><td>The live phase is already confirmed and usable right now.</td><td><a href="/wuthering-waves-current-banner-characters/">Current banner characters</a></td></tr>
              <tr><td>You are planning the next roster step</td><td>Compare against {next_item["banner_name"]}</td><td>{why_copy}</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
              <tr><td>You are protecting pity</td><td>Save</td><td>Pity and weapon pressure matter more than forcing a live spend.</td><td><a href="/wuthering-waves-pity-system/">Pity system</a></td></tr>
            </tbody>
          </table>
        </div>"""


def build_current_account_routes(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    return f"""      <div class="card">
        <h2>If you want the fastest live answer</h2>
        <p>Start with the current phase if you only care about what is usable right now. This is the best route for accounts that need immediate value from {", ".join(current["featured_characters"])} before the phase ends.</p>
        <ul class="list">
          <li><strong>Best for:</strong> accounts that need a live fix more than they need long-range planning.</li>
          <li><strong>Check after this:</strong> current banner characters, then the pity page.</li>
          <li><strong>Skip this route:</strong> if your real blocker is weapon cost, not character value.</li>
        </ul>
      </div>
      <div class="card">
        <h2>If you are comparing before spending</h2>
        <p>Use the current banner page as the live baseline, then jump to next banner and pity. This route is stronger than deciding from one character page without phase context.</p>
        <ul class="list">
          <li><strong>Best for:</strong> single-pity or low-Astrite accounts that cannot afford a wrong turn.</li>
          <li><strong>Check after this:</strong> next banner, next rerun, then weapon banner if pressure is split.</li>
          <li><strong>Do not stop here:</strong> comparison-only users still need a final pity and weapon pass.</li>
        </ul>
      </div>"""


def build_current_character_links(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    cards = []
    for name in current["featured_characters"]:
        slug = slugify_character(name)
        cards.append(
            f'        <article class="card"><h2>{name}</h2><p>Open the guide hub, pull page, and support pages for the live character before committing resources.</p><p><a href="/wuthering-waves-characters/{slug}/">Open {name} hub</a></p></article>'
        )
    return f"""      <h2>Live character starting points</h2>
      <div class="card-grid">
{chr(10).join(cards)}
      </div>"""


def build_current_sources(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = snapshot["updated"]
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} snapshot</strong><br>
        Current phase source: {current["source_url"]}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>"""


def build_history_intro(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    next_item = snapshot["next"]
    return f"""    <p class="lead">This banner history page now works as a real list page. Users can scan recent version phases first, then open the matching phase detail page for lineup, timing, and rerun context. The history structure is generated from the site CSV so future updates stay consistent.</p>
    <div class="answer-box"><strong>Direct answer:</strong> The best Wuthering Waves banner history page shows version, phase, featured characters, featured weapons, dates, and a clear route into a dedicated detail page for each tracked phase. The next tracked banner-related checkpoint after this recent list is {next_item["banner_name"]}.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_history_media(snapshot: dict[str, object]) -> str:
    return """    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/banner-history-card.svg" alt="Wuthering Waves banner history snapshot generated from the latest CSV build." width="1200" height="675" decoding="async">
      </div>
      <div class="card">
        <h2>Use the list page first</h2>
        <p>Start with the history list to compare phases quickly. Then open the matching detail page when you need the exact lineup, weapons, dates, or rerun context for one banner cycle.</p>
        <p><a href="/wuthering-waves-next-banner/">Compare history against the next banner page</a></p>
      </div>
    </div>"""


def history_row_slug(item: dict[str, object]) -> str:
    phase_slug = str(item["phase"]).lower().replace(" ", "-")
    version_slug = str(item["version"]).replace(".", "-")
    return f"version-{version_slug}-{phase_slug}"


def history_row_path(item: dict[str, object]) -> str:
    return f"/wuthering-waves-banner-history/{history_row_slug(item)}/"


def build_history_table(snapshot: dict[str, object]) -> str:
    rows = []
    for item in snapshot["history"]:
        rows.append(
            f'            <tr><td>{item["version"]}</td><td>{item["phase"]}</td><td>{item["banner_name"]}</td><td>{", ".join(item["featured_characters"])}</td><td>{", ".join(item["featured_weapons"]) if item["featured_weapons"] else "Not tracked"}</td><td>{fmt_human_date(item["start_date"])} to {fmt_human_date(item["end_date"])}</td><td><a href="{history_row_path(item)}">Open detail</a></td></tr>'
        )
    rows_html = "\n".join(rows)
    cards = []
    for item in snapshot["history"]:
        character_strip = render_history_entity_strip("characters", item["featured_characters"])
        weapon_strip = render_history_entity_strip("weapons", item["featured_weapons"]) if item["featured_weapons"] else '<span class="history-name-chip">Weapons not tracked</span>'
        cards.append(
            f'''        <article class="card history-phase-card">
          <div class="history-phase-top">
            <div>
              <h3>{item["banner_name"]}</h3>
              <p class="muted">{fmt_human_date(item["start_date"])} to {fmt_human_date(item["end_date"])}</p>
            </div>
            <a class="directory-link" href="{history_row_path(item)}">Open phase detail</a>
          </div>
          <div class="history-entity-block">
            <strong>Featured characters</strong>
            <div class="history-entity-row">{character_strip}</div>
          </div>
          <div class="history-entity-block">
            <strong>Featured weapons</strong>
            <div class="history-entity-row">{weapon_strip}</div>
          </div>
        </article>'''
        )
    cards_html = "\n".join(cards)
    return f"""      <h2>Recent banner history list</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Version</th><th>Phase</th><th>Banner</th><th>Featured characters</th><th>Featured weapons</th><th>Dates</th><th>Detail page</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
      <div class="card-grid" style="margin-top:1.25rem;">
{cards_html}
      </div>"""


def build_history_sources(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    urls = [item["source_url"] for item in snapshot["history"]]
    lines = "<br>\n".join([f"        Timeline source: {url}" for url in urls])
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} history snapshot</strong><br>
{lines}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>"""


def get_history_detail_pages(snapshot: dict[str, object]) -> list[dict[str, object]]:
    pages = []
    for item in snapshot["history"]:
        pages.append(
            {
                "version": item["version"],
                "phase": item["phase"],
                "banner_name": item["banner_name"],
                "featured_characters": item["featured_characters"],
                "featured_weapons": item["featured_weapons"],
                "start_date": item["start_date"],
                "end_date": item["end_date"],
                "source_url": item["source_url"],
                "slug": history_row_slug(item),
                "path": history_row_path(item),
            }
        )
    return pages


def get_history_neighbors(pages: list[dict[str, object]], current_slug: str) -> tuple[dict[str, object] | None, dict[str, object] | None]:
    for index, item in enumerate(pages):
        if item["slug"] != current_slug:
            continue
        previous_item = pages[index - 1] if index > 0 else None
        next_item = pages[index + 1] if index + 1 < len(pages) else None
        return previous_item, next_item
    return None, None


def render_history_detail_page(page: dict[str, object], snapshot: dict[str, object]) -> str:
    banner_name = str(page["banner_name"])
    version = str(page["version"])
    phase = str(page["phase"])
    path = str(page["path"])
    characters_text = ", ".join(str(name) for name in page["featured_characters"])
    weapons_text = ", ".join(str(name) for name in page["featured_weapons"]) if page["featured_weapons"] else "No weapon row tracked for this phase."
    character_strip = render_history_entity_strip("characters", list(page["featured_characters"]))
    weapon_strip = render_history_entity_strip("weapons", list(page["featured_weapons"])) if page["featured_weapons"] else '<span class="history-name-chip">Weapons not tracked</span>'
    history_pages = get_history_detail_pages(snapshot)
    previous_page, next_page = get_history_neighbors(history_pages, str(page["slug"]))
    history_nav_cards = []
    if previous_page:
        history_nav_cards.append(
            f'''      <a class="history-phase-nav-card" href="{previous_page["path"]}">
        <span class="history-phase-nav-label">Previous phase</span>
        <strong>{html.escape(str(previous_page["banner_name"]))}</strong>
        <span class="muted">{fmt_human_date(str(previous_page["start_date"]))} to {fmt_human_date(str(previous_page["end_date"]))}</span>
      </a>'''
        )
    if next_page:
        history_nav_cards.append(
            f'''      <a class="history-phase-nav-card" href="{next_page["path"]}">
        <span class="history-phase-nav-label">Next phase</span>
        <strong>{html.escape(str(next_page["banner_name"]))}</strong>
        <span class="muted">{fmt_human_date(str(next_page["start_date"]))} to {fmt_human_date(str(next_page["end_date"]))}</span>
      </a>'''
        )
    history_nav_html = "\n".join(history_nav_cards) if history_nav_cards else '      <p class="muted">This is the only tracked phase in the current history window.</p>'
    title = f"Wuthering Waves {banner_name} Banner History | WuWa Banners"
    description = f"View the {banner_name} banner history detail page with featured characters, featured weapons, dates, and rerun context."
    faq_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": f"Wuthering Waves {banner_name} Banner History",
                    "description": description,
                    "author": {"@type": "Organization", "name": "WuWa Banners"},
                    "publisher": {"@type": "Organization", "name": "WuWa Banners"},
                    "mainEntityOfPage": f"https://wuwabanners.net{path}",
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": f"What does the {banner_name} history detail page show?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": f"It shows the banner window, featured characters, featured weapons, and why {banner_name} matters inside the broader rerun and history timeline."
                            },
                        },
                        {
                            "@type": "Question",
                            "name": "Why use a detail page instead of one giant history table?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Because the list page should stay fast to scan, while the detail page can hold the exact lineup and timing for one tracked phase."
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="Wuthering Waves {html.escape(banner_name)} Banner History">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="/banners/">Banners</a> / <a href="/wuthering-waves-banner-history/">Banner history</a> / {html.escape(banner_name)}</div>
    <h1>Wuthering Waves {html.escape(banner_name)} Banner History</h1>
    <p class="lead">This detail page isolates one tracked banner phase so users can see the lineup, timing, and rerun context without scanning a larger history table first.</p>
    <div class="answer-box"><strong>Direct answer:</strong> {html.escape(banner_name)} ran from {fmt_human_date(str(page["start_date"]))} to {fmt_human_date(str(page["end_date"]))}, featuring {html.escape(characters_text)}. The tracked weapons for this phase are {html.escape(weapons_text)}</div>
    <p class="update-stamp">Last updated: {fmt_human_date(snapshot["updated"] + " 00:00")}.</p>
{build_history_detail_media(page)}
    <section class="section">
      <h2>{html.escape(banner_name)} lineup cards</h2>
      <div class="card history-phase-card">
        <div class="history-entity-block">
          <strong>Featured characters</strong>
          <div class="history-entity-row">{character_strip}</div>
        </div>
        <div class="history-entity-block">
          <strong>Featured weapons</strong>
          <div class="history-entity-row">{weapon_strip}</div>
        </div>
      </div>
    </section>
    <section class="section">
      <h2>{html.escape(banner_name)} detail snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Field</th><th>Value</th></tr></thead>
          <tbody>
            <tr><td>Version</td><td>{html.escape(version)}</td></tr>
            <tr><td>Phase</td><td>{html.escape(phase)}</td></tr>
            <tr><td>Banner name</td><td>{html.escape(banner_name)}</td></tr>
            <tr><td>Featured characters</td><td>{html.escape(characters_text)}</td></tr>
            <tr><td>Featured weapons</td><td>{html.escape(weapons_text)}</td></tr>
            <tr><td>Banner window</td><td>{fmt_human_date(str(page["start_date"]))} to {fmt_human_date(str(page["end_date"]))}</td></tr>
          </tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <h2>Browse nearby history phases</h2>
      <div class="history-phase-nav-grid">
{history_nav_html}
      </div>
    </section>
    <section class="section two-col">
      <div class="card">
        <h2>Best next pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-banner-history/">Back to banner history list</a></li>
          <li><a href="/wuthering-waves-next-rerun/">Next rerun</a></li>
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>How to use this detail page</h2>
        <p>Use the list page for scanning. Use this detail page when you want the exact phase lineup, window, and source in one place before comparing it against current or future banner decisions.</p>
      </div>
    </section>
    <section class="section">
      <h2>FAQ</h2>
      <div class="faq-list">
        <article class="faq-item"><h3>What does the {html.escape(banner_name)} history detail page show?</h3><p>It shows the banner window, featured characters, featured weapons, and why this phase matters inside the broader banner timeline.</p></article>
        <article class="faq-item"><h3>Why use a detail page instead of one giant history table?</h3><p>Because the list page should stay fast to scan, while a detail page can hold the exact lineup and timing for one tracked phase.</p></article>
      </div>
      <div class="sources">
        <strong>Source used for this {html.escape(banner_name)} detail page</strong><br>
        Timeline source: {html.escape(str(page["source_url"]))}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>
    </section>
  </div></main>
  <script defer src="/assets/js/site.js"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def build_rerun_intro(snapshot: dict[str, object]) -> str:
    history = snapshot["history"]
    updated = snapshot["updated"]
    oldest = history[0]
    return f"""    <p class="lead">Rerun intent is different from next banner intent. Based on the tracked recent cycle, the oldest featured five-stars in the current snapshot are {", ".join(oldest["featured_characters"])}, which makes them the first names users will compare when asking whether to spend now or hold longer.</p>
    <div class="answer-box"><strong>Direct answer:</strong> No rerun page can promise a date without official confirmation, but a good rerun guide can show which older featured units are furthest from their last phase and therefore most likely to be searched next.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_rerun_media() -> str:
    return """    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/banner-history-card.svg" alt="Wuthering Waves rerun watch image based on recent banner history." width="1200" height="675" decoding="async">
      </div>
      <div class="card">
        <h2>Use history, not guesswork</h2>
        <p>Rerun pages work when they show why a character is being watched, not when they pretend to know a date that has not been announced.</p>
      </div>
    </div>"""


def build_rerun_cards(snapshot: dict[str, object]) -> str:
    oldest = snapshot["history"][0]
    return f"""    <div class="card-grid">
      <article class="card"><h2>Earliest tracked phase in view</h2><p>{oldest["banner_name"]} is the oldest tracked phase in the current snapshot, featuring {", ".join(oldest["featured_characters"])}.</p></article>
      <article class="card"><h2>Why users search reruns</h2><p>Most users are not asking for a rumor. They are asking whether saving now makes sense, which means this page should connect history, pity, and current banner timing.</p></article>
      <article class="card"><h2>Best internal links</h2><p>Send rerun readers to banner history, the current banner page, and character-specific pull pages.</p></article>
    </div>"""


def build_rerun_table(snapshot: dict[str, object]) -> str:
    rows = []
    for item in snapshot["history"]:
        rows.append(
            f'            <tr><td>{item["banner_name"]}</td><td>{", ".join(item["featured_characters"])}</td><td>{fmt_human_date(item["start_date"])} to {fmt_human_date(item["end_date"])}</td></tr>'
        )
    rows_html = "\n".join(rows)
    return f"""      <h2>Rerun watchlist context</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Tracked phase</th><th>Featured 5-stars</th><th>Dates</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>"""


def build_rerun_sources(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} rerun watch snapshot</strong><br>
        History and phase timing come from the banner-data.csv source URLs used across the banner history page.
      </div>"""


def build_countdown_intro(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    updated = snapshot["updated"]
    answer_copy = (
        f"{current['banner_name']} ends on {fmt_human_date(current['end_date'])}, and the next tracked official update is {next_item['banner_name']} on {phase_event_label(next_item)}."
        if is_preview_phase(next_item)
        else f"{current['banner_name']} ends on {fmt_human_date(current['end_date'])}, and {next_item['banner_name']} begins on {fmt_human_date(next_item['start_date'])}."
    )
    return f"""    <p class="lead">Countdown intent is mostly practical. Users want the current phase end date and the next phase start date without needing to decode a long article first.</p>
    <div class="answer-box"><strong>Direct answer:</strong> {answer_copy}</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_countdown_media(snapshot: dict[str, object]) -> str:
    return """    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves countdown context card." width="1200" height="675" decoding="async">
      </div>
      <div class="banner-art">
        <img src="/assets/img/next-banner-card.svg" alt="Next Wuthering Waves countdown context card." width="1200" height="675" decoding="async">
      </div>
    </div>"""


def build_countdown_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    next_title = "Next phase start" if not is_preview_phase(next_item) else "Next official preview"
    next_copy = (
        f"{next_item['banner_name']} is scheduled to start on {fmt_human_date(next_item['start_date'])}."
        if not is_preview_phase(next_item)
        else next_event_copy(next_item)
    )
    return f"""    <div class="card-grid">
      <article class="card"><h2>Current phase end</h2><p>{current["banner_name"]} is scheduled to end on {fmt_human_date(current["end_date"])}.</p></article>
      <article class="card"><h2>{next_title}</h2><p>{next_copy}</p></article>
      <article class="card"><h2>Why clarity matters</h2><p>Users often search countdown pages from mobile. Put the dates in plain text first, then support them with tables and related links.</p></article>
    </div>"""


def build_countdown_table(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    next_event = "Next phase starts" if not is_preview_phase(next_item) else "Next official preview"
    return f"""      <h2>Banner timing snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>Event</th><th>Date</th></tr></thead>
          <tbody>
            <tr><td>{current["banner_name"]}</td><td>Current phase ends</td><td>{fmt_human_date(current["end_date"])}</td></tr>
            <tr><td>{next_item["banner_name"]}</td><td>{next_event}</td><td>{phase_event_label(next_item)}</td></tr>
          </tbody>
        </table>
      </div>"""


def build_countdown_sources(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = snapshot["updated"]
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} countdown snapshot</strong><br>
        Current phase source: {current["source_url"]}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>"""


def get_pull_pages(snapshot: dict[str, object]) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for mode, key, card_name in (("current", "current", "current-banner-card.svg"), ("next", "next", "next-banner-card.svg")):
        phase = snapshot[key]
        if not phase["featured_characters"]:
            continue
        compare_phase = snapshot["next"] if key == "current" else snapshot["current"]
        for character in phase["featured_characters"]:
            slug = slugify_character(character)
            if slug in seen:
                continue
            seen.add(slug)
            pages.append(
                {
                    "character": character,
                    "slug": slug,
                    "mode": mode,
                    "source_url": phase["source_url"],
                    "banner_name": phase["banner_name"],
                    "phase_label": phase["banner_name"],
                    "start_date": phase["start_date"],
                    "end_date": phase["end_date"],
                    "card_name": card_name,
                    "phase_featured_characters": "|".join(phase["featured_characters"]),
                    "phase_featured_weapons": "|".join(phase["featured_weapons"]),
                    "compare_featured_characters": "|".join(compare_phase["featured_characters"]),
                    "compare_featured_weapons": "|".join(compare_phase["featured_weapons"]),
                }
            )
    return pages


def character_overview_path(slug: str) -> str:
    return f"/wuthering-waves-characters/{slug}/"


def get_character_overview_pages(pull_pages: list[dict[str, str]]) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    for page in pull_pages:
        pages.append(
            {
                "character": page["character"],
                "slug": page["slug"],
                "mode": page["mode"],
                "phase_label": page["phase_label"],
                "source_url": page["source_url"],
                "start_date": page["start_date"],
                "end_date": page["end_date"],
                "path": character_overview_path(page["slug"]),
            }
        )
    return pages


def support_page_path(slug: str, kind: str) -> str:
    return f"/wuthering-waves-{slug}-{kind}/"


def get_support_pages(pull_pages: list[dict[str, str]]) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    for page in pull_pages:
        for kind, label in (
            ("materials", "Materials"),
            ("build", "Build"),
            ("team-comps", "Team Comps"),
        ):
            pages.append(
                {
                    **page,
                    "kind": kind,
                    "kind_label": label,
                    "path": support_page_path(page["slug"], kind),
                }
            )
    return pages


def build_pull_intro(snapshot: dict[str, object], pull_pages: list[dict[str, str]]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    updated = snapshot["updated"]
    next_copy = (
        f"and the upcoming {next_item['banner_name']} phase"
        if next_item["featured_characters"]
        else f"while {next_item['banner_name']} remains the next official checkpoint before the next full lineup is confirmed"
    )
    answer_copy = (
        "Start with a current-phase page if you are deciding whether to spend now. Start with the next-banner page if you are deciding whether to save."
        if not next_item["featured_characters"]
        else "Start with a current-phase page if you are deciding whether to spend now. Start with a next-phase page if you are deciding whether to save."
    )
    return f"""    <p class="lead">This hub is where banner facts turn into player decisions. Right now the tracked pull set covers {len(pull_pages)} featured characters across the live {current["banner_name"]} phase {next_copy}.</p>
    <div class="answer-box"><strong>Direct answer:</strong> {answer_copy}</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_pull_grid(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    next_pool = (
        f"The next phase pages cover {', '.join(next_item['featured_characters'])} and should answer whether saving beats the current live banner."
        if next_item["featured_characters"]
        else f"The next full lineup is still pending. Until {next_item['banner_name']} lands, the best next-step page is the banner comparison view rather than a character-specific save page."
    )
    return f"""    <div class="card-grid">
      <article class="card"><h2>Account-need framing</h2><p>Good pull advice starts with user context: missing DPS, missing sustain, saving for a rerun, or targeting a specific team role.</p></article>
      <article class="card"><h2>Current phase pool</h2><p>The live phase pages cover {", ".join(current["featured_characters"])} and should answer whether spending now is worth the pity and Astrite cost.</p></article>
      <article class="card"><h2>Next phase pool</h2><p>{next_pool}</p></article>
      <article class="card"><h2>Weapon and pity pressure</h2><p>Do not compare characters in isolation. If the real account question is weapon dependence, pity carry-over, or whether one banner demands too many tides at once, route the user to weapon and pity pages before locking a pull plan.</p></article>
    </div>"""


def build_pull_links(pull_pages: list[dict[str, str]]) -> str:
    current_cards = []
    next_cards = []
    for page in pull_pages:
        bucket = current_cards if page["mode"] == "current" else next_cards
        phase_label = "current live phase" if page["mode"] == "current" else "next tracked phase"
        bucket.append(
            f'        <article class="card"><h2>Should you pull {page["character"]}?</h2><p>Decision page for {page["character"]} in the {phase_label}.</p><p><a href="/wuthering-waves-should-you-pull-{page["slug"]}/">Open page</a></p></article>'
        )
    if not next_cards:
        next_cards.append(
            """        <article class="card"><h2>Next phase pages pending</h2><p>The next full featured lineup is still waiting on the next official preview, so there are no new next-phase character pull pages yet.</p><p><a href="/wuthering-waves-next-banner/">Open next banner</a></p></article>"""
        )
    return f"""      <h2>Current phase pull pages</h2>
      <div class="card-grid">
{chr(10).join(current_cards)}
      </div>
      <h2 style="margin-top:1.5rem;">Next phase pull pages</h2>
      <div class="card-grid">
{chr(10).join(next_cards)}
      </div>"""


def build_pull_decision_routes(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    next_route = join_or_fallback(list(next_item["featured_characters"]), next_item["banner_name"])
    next_route_reason = (
        "The next phase should be compared against current pity, not against hype alone."
        if next_item["featured_characters"]
        else "Use the next official preview checkpoint before assuming the next phase is worth saving for."
    )
    return f"""      <h2>Fast decision routes by account state</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>If this sounds like you</th><th>Start here</th><th>Why</th><th>Then open</th></tr></thead>
          <tbody>
            <tr><td>You want to spend now and need the safest live answer</td><td>{", ".join(current["featured_characters"])}</td><td>The current phase can be judged against a real live timer and weapon set.</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td></tr>
            <tr><td>You already expect to save for the next rotation</td><td>{next_route}</td><td>{next_route_reason}</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
            <tr><td>You only have one real pity window left</td><td>Open the phase comparison first</td><td>Single-pity accounts should compare current value, next value, and rerun spacing before committing to any one featured unit.</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
            <tr><td>Your real pressure is the weapon side, not the character side</td><td>Open weapon and pity pages before character pages</td><td>Weapon pressure changes the true cost of a pull plan and can flip a yes into a save call.</td><td><a href="/wuthering-waves-weapon-banner/">Weapon banner</a></td></tr>
            <tr><td>You are unsure whether to spend at all</td><td>Open the comparison path first</td><td>A comparison pass is better than jumping straight into one character page.</td><td><a href="/wuthering-waves-next-rerun/">Next rerun</a></td></tr>
          </tbody>
        </table>
      </div>"""


def build_pull_compare_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    next_compare = (
        f"Use the next phase when {', '.join(next_item['featured_characters'])} better matches your long-plan roster direction, and when protecting pity matters more than immediate live-banner pressure."
        if next_item["featured_characters"]
        else f"Use the preview checkpoint when you are mainly trying to avoid locking a save target before {next_item['banner_name']} clarifies the next full lineup."
    )
    return f"""      <div class="card">
        <h2>When the current phase wins</h2>
        <p>Use the current phase when {", ".join(current["featured_characters"])} fixes a live roster problem now, not later. This is the path for accounts that need immediate value from active banners.</p>
        <ul class="list">
          <li><strong>Best fit:</strong> accounts with an urgent hole that the live banner solves immediately.</li>
          <li><strong>Safer timing:</strong> players who prefer a confirmed live lineup over future speculation.</li>
          <li><strong>Check next:</strong> current banner, current banner characters, then pity.</li>
        </ul>
      </div>
      <div class="card">
        <h2>When the next phase or rerun path wins</h2>
        <p>{next_compare}</p>
        <ul class="list">
          <li><strong>Best fit:</strong> accounts already aiming at the next roster step or a later rerun lane.</li>
          <li><strong>Resource logic:</strong> saving wins when pity protection matters more than solving a short-term live problem.</li>
          <li><strong>Check next:</strong> next banner, next rerun, then pity system.</li>
        </ul>
      </div>"""


def build_character_intro(page: dict[str, str], snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    character = page["character"]
    if page["mode"] == "current":
        return f"""    <p class="lead">Use this page to decide whether {character} is worth pulling during the live {page["banner_name"]} phase or whether saving is still the better call for your account.</p>
    <div class="answer-box"><strong>Quick verdict:</strong> Pull {character} if the live phase solves an immediate account need. Wait if your roster direction lines up more strongly with the next phase or a rerun target.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""
    return f"""    <p class="lead">Use this page to decide whether {character} is worth saving for in the upcoming {page["banner_name"]} phase instead of spending on the current live banner.</p>
    <div class="answer-box"><strong>Quick verdict:</strong> Save for {character} if the next phase fits your roster plan better than the current banner. Spend now only if the live banner solves a more urgent account need.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_character_media(page: dict[str, str]) -> str:
    phase_src = get_visual_src("characters", [page["character"]])
    compare_names = page["compare_featured_characters"].split("|")
    side_character = get_visual_src("characters", compare_names)
    weapon_names = page["phase_featured_weapons"].split("|")
    phase_weapon = get_visual_src("weapons", weapon_names)
    support_item = get_visual_src("items", ["platinum core", "coriolus", "redbell"])
    return f"""    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        {render_phase_collage(phase_src, page["character"], [(side_character, "Compare phase", False), (phase_weapon, "Weapon pressure", True), (support_item, "Farm context", True)])}
      </div>
      <div class="video-card">
        <h2>Phase reference video</h2>
        {render_reference_video_embed()}
      </div>
    </div>"""


def build_character_blocks(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    if page["mode"] == "current":
        next_names = next_character_copy(snapshot["next"])
        current_weapons = ", ".join(snapshot["current"]["featured_weapons"])
        return f"""    <div class="card-grid">
      <article class="card"><h2>Best for who</h2><p>Best for accounts that want to invest in the current live phase instead of waiting for the next banner rotation.</p></article>
      <article class="card"><h2>Reasons to pull</h2><p>Pull when {character} is the clearest answer to your current roster gap and you are not preserving pity for the next phase lineup: {next_names}.</p></article>
      <article class="card"><h2>Reasons to skip</h2><p>Skip if you are already aiming at the next phase or holding resources for a rerun target that matters more.</p></article>
      <article class="card"><h2>Weapon and pity pressure</h2><p>Do not rate {character} only on character appeal. If the real cost question is whether the live weapon set {current_weapons} stretches your pity too far, compare the full phase plan before spending.</p></article>
    </div>"""
    current_names = ", ".join(snapshot["current"]["featured_characters"])
    next_weapons = ", ".join(snapshot["next"]["featured_weapons"])
    return f"""    <div class="card-grid">
      <article class="card"><h2>Best for who</h2><p>Best for accounts planning around the next phase rather than using resources immediately in the current rotation.</p></article>
      <article class="card"><h2>Reasons to save</h2><p>Save for {character} if your pity position and account plan already point toward the next phase instead of the current lineup: {current_names}.</p></article>
      <article class="card"><h2>Reasons to wait longer</h2><p>Wait even beyond {character} if your real target is a rerun unit and the next phase still does not match your account needs.</p></article>
      <article class="card"><h2>Weapon and pity pressure</h2><p>Saving for {character} only wins if the next phase weapon set {next_weapons} does not turn the plan into a worse pity trap than the live banner.</p></article>
    </div>"""


def build_character_decision_matrix(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    current = snapshot["current"]
    next_item = snapshot["next"]
    if page["mode"] == "current":
        next_watch = join_or_fallback(list(next_item["featured_characters"]), next_item["banner_name"])
        return f"""    <section class="section">
      <h2>{character} decision matrix</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>If this is true</th><th>Decision</th><th>Why</th></tr></thead>
          <tbody>
            <tr><td>{character} fixes your biggest immediate roster issue</td><td>Pull now</td><td>The live phase is real, active, and easier to judge than waiting on a later solve.</td></tr>
            <tr><td>You already prefer {next_watch}</td><td>Save</td><td>The next phase is a better direction fit than forcing a live spend.</td></tr>
            <tr><td>You only have one real pity window left</td><td>Compare current versus next before spending</td><td>Single-pity accounts should treat {character} as one option inside a bigger phase choice, not as an automatic yes.</td></tr>
            <tr><td>Your real concern is the weapon side</td><td>Check weapon banner first</td><td>If the live weapon set is the expensive part, a strong character answer can still become a bad full-banner plan.</td></tr>
            <tr><td>You mainly care about pity efficiency</td><td>Delay</td><td>Checking pity and rerun timing first is safer than impulse spending.</td></tr>
          </tbody>
        </table>
      </div>
    </section>"""
    return f"""    <section class="section">
      <h2>{character} decision matrix</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>If this is true</th><th>Decision</th><th>Why</th></tr></thead>
          <tbody>
            <tr><td>{character} is already your planned next target</td><td>Save</td><td>The next phase should win if your roster path is already pointing there.</td></tr>
            <tr><td>{", ".join(current["featured_characters"])} solves a bigger live problem</td><td>Spend now instead</td><td>Current utility can beat a future preference when the account need is urgent.</td></tr>
            <tr><td>You only have one pity cycle left</td><td>Keep comparing phases</td><td>Single-pity accounts should test whether {character} beats the full live-to-next comparison, not just the current banner in isolation.</td></tr>
            <tr><td>The next weapon set is the real issue</td><td>Check weapon risk before saving</td><td>Saving for a character is weaker if the next-phase weapon pressure makes the whole plan too expensive.</td></tr>
            <tr><td>You are also holding for reruns</td><td>Delay both</td><td>Phase comparison and rerun timing matter more than forcing one banner cycle.</td></tr>
          </tbody>
        </table>
      </div>
    </section>"""


def build_character_support_links(page: dict[str, str]) -> str:
    slug = page["slug"]
    character = page["character"]
    return f"""    <section class="section">
      <h2>{character} support pages</h2>
      <div class="card-grid">
        <article class="card"><h3>{character} materials</h3><p>Track ascension, forte, boss, and pre-farm planning without leaving the banner cluster.</p><p><a href="{support_page_path(slug, "materials")}">Open materials page</a></p></article>
        <article class="card"><h3>{character} build</h3><p>Use a build planning page to keep weapon path, upgrade order, and stat decisions in one place.</p><p><a href="{support_page_path(slug, "build")}">Open build page</a></p></article>
        <article class="card"><h3>{character} team comps</h3><p>Keep team-role questions tied to the same pull decision instead of sending users into disconnected posts.</p><p><a href="{support_page_path(slug, "team-comps")}">Open team comps page</a></p></article>
      </div>
    </section>"""


def build_history_detail_media(page: dict[str, object]) -> str:
    character_names = list(page["featured_characters"])
    weapon_names = list(page["featured_weapons"])
    main_src = get_visual_src("characters", character_names)
    secondary_src = get_visual_src("characters", character_names[1:] or character_names)
    weapon_src = get_visual_src("weapons", weapon_names)
    compare_src = get_visual_src("characters", ["cantarella", "jinhsi", "camellya"])
    return f"""    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        {render_phase_collage(main_src, str(page["banner_name"]), [(secondary_src, "Featured lineup", False), (weapon_src, "Phase weapon", True), (compare_src, "Timeline context", False)])}
      </div>
      <div class="card">
        <h2>Why this phase matters</h2>
        <p>{html.escape(str(page["banner_name"]))} sits inside the broader version flow of {html.escape(str(page["version"]))} {html.escape(str(page["phase"]))}. Use this page when you need one phase in isolation instead of a compressed list view.</p>
        <p><a href="/wuthering-waves-next-rerun/">Compare this phase against rerun watch</a></p>
      </div>
    </div>"""


def build_character_overview_media(page: dict[str, str], snapshot: dict[str, object]) -> str:
    primary = snapshot["current"] if page["mode"] == "current" else snapshot["next"]
    compare = snapshot["next"] if page["mode"] == "current" else snapshot["current"]
    main_src = get_visual_src("characters", [page["character"]])
    branch_mate = get_visual_src(
        "characters",
        [name for name in primary["featured_characters"] if name != page["character"]],
    )
    compare_src = get_visual_src("characters", list(compare["featured_characters"]))
    weapon_src = get_visual_src("weapons", list(primary["featured_weapons"]))
    item_src = get_visual_src("items", ["platinum core", "coriolus", "redbell"])
    return f"""    <div class="hub-hero">
      <div class="hub-hero-media" aria-hidden="true">
        <figure class="hub-hero-tile hub-hero-tile--major">
          <img src="{main_src}" alt="" width="512" height="512" decoding="async">
          <span class="hub-hero-label">{html.escape(page["character"])}</span>
        </figure>
        <div class="hub-hero-stack">
          <figure class="hub-hero-tile hub-hero-tile--wide">
            <img src="{branch_mate}" alt="" width="512" height="512" decoding="async">
            <span class="hub-hero-label">Same phase</span>
          </figure>
          <figure class="hub-hero-tile hub-hero-tile--wide hub-hero-tile--artifact">
            <img src="{weapon_src}" alt="" width="512" height="512" decoding="async">
            <span class="hub-hero-label">Weapon route</span>
          </figure>
        </div>
        <div class="hub-hero-stack">
          <figure class="hub-hero-tile hub-hero-tile--wide">
            <img src="{compare_src}" alt="" width="512" height="512" decoding="async">
            <span class="hub-hero-label">Compare phase</span>
          </figure>
          <figure class="hub-hero-tile hub-hero-tile--wide hub-hero-tile--artifact">
            <img src="{item_src}" alt="" width="512" height="512" decoding="async">
            <span class="hub-hero-label">Farm path</span>
          </figure>
        </div>
      </div>
      <div class="hub-hero-copy">
        <span class="eyebrow">Character hub</span>
        <strong>{html.escape(page["character"])} should route users into one clean next step, not force them to guess.</strong>
        <p>Use the hub when the character name is already clear and the real question is whether the next click should be pull advice, materials, build, or team comps.</p>
      </div>
    </div>"""


def build_character_faq(page: dict[str, str]) -> str:
    if page["mode"] == "current":
        return """      <div class="faq-list">
        <article class="faq-item"><h3>Should you pull this current featured character now?</h3><p>Pull only if the live phase matches your roster needs better than saving for the next banner or your rerun watchlist.</p></article>
        <article class="faq-item"><h3>What should you check before pulling?</h3><p>Check your pity state, the current banner end date, and whether your next target is close enough to justify saving.</p></article>
        <article class="faq-item"><h3>What if the weapon cost is the real problem?</h3><p>Open the weapon banner and pity pages before deciding. A current character can still be the wrong spend if the full character-plus-weapon plan is too expensive.</p></article>
      </div>"""
    return """      <div class="faq-list">
        <article class="faq-item"><h3>Should you save for this next featured character?</h3><p>Save when the upcoming phase fits your planned roster better than the current one and your pity state supports waiting.</p></article>
        <article class="faq-item"><h3>What should you compare before deciding?</h3><p>Compare the current banner end date, your pity progress, your rerun watchlist, and whether the upcoming phase solves a bigger problem for your account.</p></article>
        <article class="faq-item"><h3>Can the next-phase weapon pressure change the answer?</h3><p>Yes. A save decision is weaker if the next-phase weapon side makes the full plan less efficient than spending in the live phase or delaying for a rerun.</p></article>
      </div>"""


def build_character_sources(page: dict[str, str], updated: str) -> str:
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} pull snapshot</strong><br>
        Character phase source: {page["source_url"]}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>"""


def build_support_intro(page: dict[str, str], snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    character = page["character"]
    kind = page["kind"]
    if kind == "materials":
        lead = (
            f"Use this {character} materials page to keep ascension, forte, boss-drop, and pre-farm planning tied to the same banner decision."
        )
        answer = (
            f"Farm only the stable and broadly confirmed {character} material routes first. Save heavy stamina spending on uncertain drops until official or in-game confirmation is live."
        )
    elif kind == "build":
        lead = (
            f"Use this {character} build page to keep weapon path, upgrade order, and role framing connected to the same current-versus-next banner choice."
        )
        answer = (
            f"Lock the cheap and flexible parts of a {character} build first, then wait for final role and live-testing confirmation before overcommitting to expensive refinements."
        )
    else:
        lead = (
            f"Use this {character} team comps page to connect pull decisions with actual party-slot planning, not just abstract banner hype."
        )
        answer = (
            f"Plan {character} teams around role fit, sustain slot pressure, and rotation comfort first. Treat final meta pairings as something to confirm after official or live-game evidence settles."
        )
    return f"""    <p class="lead">{lead}</p>
    <div class="answer-box"><strong>Direct answer:</strong> {answer}</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_support_media(page: dict[str, str]) -> str:
    character = page["character"]
    return f"""    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/{page["card_name"]}" alt="{character} support snapshot tied to the tracked phase card." width="1200" height="675" decoding="async">
      </div>
      <div class="video-card">
        <h2>Official reference video</h2>
        {render_reference_video_embed()}
      </div>
    </div>"""


def support_phase_context(page: dict[str, str], snapshot: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    primary = snapshot["current"] if page["mode"] == "current" else snapshot["next"]
    compare = snapshot["next"] if page["mode"] == "current" else snapshot["current"]
    return primary, compare


def character_hub_path(slug: str) -> str:
    return f"/wuthering-waves-characters/{slug}/"


def build_support_cards(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        return f"""    <div class="card-grid">
      <article class="card"><h2>What to farm first</h2><p>Start with the stable {character} routes that are least likely to change between preview, official post, and live in-game confirmation.</p></article>
      <article class="card"><h2>What to verify</h2><p>Before heavy pre-farm, confirm the exact boss-drop and shared-upgrade path that matters most for {character} in {primary["banner_name"]}.</p></article>
      <article class="card"><h2>Why this matters now</h2><p>This page should keep your material plan aligned with {primary["banner_name"]}, while still protecting resources you may need for {compare["banner_name"]}.</p></article>
    </div>"""
    if page["kind"] == "build":
        return f"""    <div class="card-grid">
      <article class="card"><h2>Role framing first</h2><p>Decide whether {character} is your main on-field investment, quick-swap slot, or flexible utility piece before you lock a build route.</p></article>
      <article class="card"><h2>Cheap decisions first</h2><p>Lock the weapon and upgrade-order decisions that stay useful even if live testing later shifts the ideal final setup in {primary["banner_name"]}.</p></article>
      <article class="card"><h2>What not to rush</h2><p>Do not over-invest in niche stat tuning until official details and actual in-game usage confirm the most efficient build direction, especially if you may pivot into {compare["banner_name"]}.</p></article>
    </div>"""
    return f"""    <div class="card-grid">
      <article class="card"><h2>Role slot</h2><p>Start by asking what team slot {character} is supposed to solve for your account, not just who looks strongest on paper.</p></article>
      <article class="card"><h2>Rotation comfort</h2><p>Team comps should stay realistic about setup speed, sustain needs, and how much field time {character} wants in {primary["banner_name"]} testing.</p></article>
      <article class="card"><h2>Future-proofing</h2><p>Keep one flexible team shell ready so {character} can be tested with future reruns or later phase additions without rebuilding from zero.</p></article>
    </div>"""


def build_support_strategy(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    primary_weapons = ", ".join(primary["featured_weapons"]) if primary["featured_weapons"] else "the tracked phase weapon set"
    compare_characters = ", ".join(compare["featured_characters"])
    if page["kind"] == "materials":
        left_title = "What you can safely do now"
        left_body = f"Use this page to pre-plan stamina around {primary['banner_name']}. Safe work usually means shared credits, common field drops, and broad upgrade routes that still help even if {character} changes slightly at live confirmation."
        right_title = "What should wait"
        right_body = f"Leave rare boss routing, weekly lock-ins, and one-character-only farming until {character} is fully confirmed in-game. That matters even more if you may switch resources toward {compare_characters} in {compare['banner_name']}."
    elif page["kind"] == "build":
        left_title = "Build decisions to lock early"
        left_body = f"Lock the role, a fallback weapon route, and a practical first upgrade order. If the tracked weapon set is {primary_weapons}, this page should help you decide whether that path is realistic for your account before you commit."
        right_title = "Build decisions to leave flexible"
        right_body = f"Final stat tuning, niche set choices, and premium-only assumptions should stay flexible until live play confirms how {character} actually feels. This is where many users decide to save for {compare['banner_name']} instead."
    else:
        left_title = "Best first team question"
        left_body = f"Ask what problem {character} solves first: field time, burst window, sustain pressure, or slot efficiency. Good team comps pages help users choose a shell that works now, not just an idealized future roster."
        right_title = "Fallback shell matters"
        right_body = f"Every {character} team page should also give one realistic fallback shell in case the best-looking pairing is tied to weapons, units, or resources better spent on {compare['banner_name']}."
    return f"""    <section class="section two-col">
      <div class="card">
        <h2>{left_title}</h2>
        <p>{left_body}</p>
      </div>
      <div class="card">
        <h2>{right_title}</h2>
        <p>{right_body}</p>
      </div>
    </section>"""


def build_support_branch_context(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    slug = page["slug"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        compare_copy = f"Before heavy stamina spending, compare {character} against the still competing needs of {', '.join(compare['featured_characters'])}. Materials pages are strongest when they tell users what is safe now and what should wait."
    elif page["kind"] == "build":
        compare_copy = f"Before locking premium gear assumptions, compare {character} against the other tracked phase. Build pages should protect users from over-committing before {primary['banner_name']} or {compare['banner_name']} settles fully."
    else:
        compare_copy = f"Before chasing idealized pairings, compare {character} against your current roster pressure and the other tracked phase. Team comps pages should keep one realistic shell ready even if premium partners are delayed."
    return f"""    <section class="section two-col">
      <div class="card">
        <h2>Where this page sits</h2>
        <p>Use this support page as the narrow layer after the {character} guide hub. The clean route is character list, then {character} hub, then this page, then the sibling support page you need next.</p>
        <div class="reference-directory">
          <a class="directory-link" href="{character_hub_path(slug)}">{character} guide hub</a>
          <a class="directory-link" href="/wuthering-waves-should-you-pull-{slug}/">Should you pull {character}?</a>
          <a class="directory-link" href="{support_page_path(slug, "materials")}">Materials</a>
          <a class="directory-link" href="{support_page_path(slug, "build")}">Build</a>
          <a class="directory-link" href="{support_page_path(slug, "team-comps")}">Team comps</a>
        </div>
      </div>
      <div class="card">
        <h2>What to compare before locking</h2>
        <p>{compare_copy}</p>
      </div>
    </section>"""


def build_support_table(page: dict[str, str]) -> str:
    character = page["character"]
    kind = page["kind"]
    if kind == "materials":
        rows = [
            ("Ascension materials", f"List the exact level-up materials for {character} once official or in-game confirmation is locked.", "Confirm on official post or in-game page"),
            ("Forte / skill materials", f"Track the shared talent route for {character} and note where it overlaps with your other planned units.", "Keep this route pre-farm friendly"),
            ("Weekly boss items", f"Do not hard-commit until {character} is live or directly confirmed by official sources.", "High-risk pre-farm item"),
            ("Weapon overlap", f"Check whether the likely weapon path for {character} shares farm routes with other current or next banner units.", "Saves stamina if aligned"),
        ]
    elif kind == "build":
        rows = [
            ("Role shape", f"Define whether {character} is being planned as an on-field carry, a swap-heavy slot, or a supportive flex.", "Decide before finalizing gear"),
            ("Weapon path", f"Keep one safe fallback weapon route for {character} even if the signature option is still undecided.", "Avoid build dead-ends"),
            ("Upgrade order", f"Prioritize the upgrade path that keeps {character} usable quickly before chasing expensive refinements.", "Fast early value"),
            ("Stat / gear notes", f"Only lock deep min-max decisions for {character} after official details and live testing settle.", "Late-stage optimization"),
        ]
    else:
        rows = [
            ("Core slot", f"Write down what job {character} must solve in the team before choosing partners.", "Defines team direction"),
            ("Sustain slot", f"Reserve a realistic sustain option so {character} teams are practical, not just theoretical.", "Stability before hype"),
            ("Flex partner", f"Keep one flexible partner slot open while {character} synergy details are still being tested.", "Best for evolving patches"),
            ("Fallback team", f"Plan one lower-cost team shell for {character} in case the premium pairing does not fit your account.", "Useful for broader audiences"),
        ]
    rows_html = "\n".join(
        f"            <tr><td>{label}</td><td>{plan}</td><td>{note}</td></tr>" for label, plan, note in rows
    )
    return f"""    <section class="section">
      <h2>{character} {page["kind_label"].lower()} planning table</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Focus area</th><th>What this page should answer</th><th>Why it matters</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_support_priority_lanes(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        rows = [
            ("Step 1", "Farm low-risk shared routes", f"Do this before locking one-character-only routes for {character}."),
            ("Step 2", "Confirm rare material paths", f"Use official or in-game confirmation before hard-committing to {primary['banner_name']}."),
            ("Step 3", "Compare against the other phase", f"Make sure {compare['banner_name']} is not the better resource destination."),
        ]
    elif page["kind"] == "build":
        rows = [
            ("Step 1", "Choose a realistic role", f"Decide whether {character} is solving an immediate job or a future optimization job."),
            ("Step 2", "Lock a fallback weapon route", "Keep one route that does not depend on ideal conditions."),
            ("Step 3", "Delay premium tuning", f"Only commit to deeper tuning after {primary['banner_name']} evidence settles."),
        ]
    else:
        rows = [
            ("Step 1", "Define the slot first", f"Choose the job {character} fills before naming partners."),
            ("Step 2", "Build one practical shell", "Use a team that works with real roster limits, not only ideal pairings."),
            ("Step 3", "Protect flexibility", f"Leave room to pivot if {compare['banner_name']} changes your best path."),
        ]
    rows_html = "\n".join(
        f"            <tr><td>{step}</td><td>{action}</td><td>{note}</td></tr>" for step, action, note in rows
    )
    return f"""    <section class="section">
      <h2>{character} {page["kind_label"].lower()} priority lanes</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Step</th><th>Action</th><th>Why now</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_character_module(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["mode"] == "current":
        heading = f"{character}-specific planning notes"
        left_title = f"If {character} is your immediate target"
        left_body = f"Treat {character} as a live-banner decision. If {character} is the reason to spend in {primary['banner_name']}, this page should keep you focused on low-risk prep and immediate usability instead of overbuilding for hypothetical later shifts."
        right_title = f"If {character} is only a side option"
        right_body = f"If {character} is not the main reason you are spending, compare this route against {compare['banner_name']} before locking too much stamina, gear, or pity pressure into one live cycle."
    else:
        heading = f"{character}-specific planning notes"
        left_title = f"If {character} is your planned save target"
        left_body = f"Use {character} pages to prep in layers before {primary['banner_name']} goes live. This is the right moment to decide role, fallback weapon path, and what can safely be prepared before final live confirmation."
        right_title = f"If {character} is competing with the live phase"
        right_body = f"If {character} is only one option among several, this page should keep comparing that route against the immediate pull value in {compare['banner_name']} instead of assuming the next phase automatically wins."
    return f"""    <section class="section two-col">
      <div class="card">
        <h2>{heading}</h2>
        <p>{left_body}</p>
      </div>
      <div class="card">
        <h2>{right_title}</h2>
        <p>{right_body}</p>
      </div>
    </section>"""


def build_focus_support_cases(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["mode"] == "current" and page["kind"] == "build":
        rows = [
            ("You want immediate live value", "Lock a practical build now", f"{character} is already inside {primary['banner_name']}, so a usable early build matters more than future-perfect tuning."),
            ("You may still pivot to the next phase", "Keep the build flexible", f"Do not over-tune gear if {compare['banner_name']} can still redirect your spending plan."),
            ("You are pity-sensitive", "Use fallback options first", "A lower-risk weapon and upgrade route protects your account from expensive overcommitment."),
        ]
    elif page["mode"] == "current" and page["kind"] == "team-comps":
        rows = [
            ("You need one safe live team", "Build a stable shell first", f"Because {character} is live now, the first team should be easy to field, not dependent on ideal future partners."),
            ("You only want to test before committing", "Use a fallback partner slot", "Leave room to swap one slot later instead of assuming the first shell is final."),
            ("You may save for the next phase", "Avoid over-specialized teammates", f"Keep the team broad enough that {compare['banner_name']} can still change your direction."),
        ]
    elif page["mode"] == "next" and page["kind"] == "materials":
        rows = [
            (f"You are definitely saving for {character}", "Pre-farm safe shared routes", f"{character} is in {primary['banner_name']}, so this is the right time to collect low-risk materials."),
            ("You still may spend on the live phase", "Delay rare material lock-in", f"Keep room for {compare['banner_name']} until {character} is fully live or fully confirmed in-game."),
            ("You want the safest prep path", "Split farming into low-risk and high-risk buckets", "That keeps your stamina plan useful even if your pull decision changes."),
        ]
    elif page["mode"] == "next" and page["kind"] == "team-comps":
        rows = [
            ("You are pre-planning before release", "Start with role-first shells", f"{character} team planning is strongest when it starts with job-to-fill, not hype around unreleased pairings."),
            ("You may skip if the live phase wins", "Keep one comparison shell", f"Make it easy to compare {character} against the immediate value of {compare['banner_name']}."),
            ("You want a publishable browser answer", "Show one practical and one ambitious shell", "That serves both conservative and premium-planning users."),
        ]
    else:
        if page["kind"] == "materials":
            rows = [
                ("You want the safest prep path", "Split farming into low-risk and high-risk buckets", "That keeps your stamina plan useful even if your pull decision changes."),
                ("You do not want to waste stamina", "Start with shared stock first", "Broadly reusable prep gives you a safer landing than locking rare routes too early."),
                ("You are comparing across phases", "Delay route-locked farming", f"Keep comparing against {compare['banner_name']} before converting soft prep into a full commitment."),
            ]
        elif page["kind"] == "build":
            rows = [
                ("You want one usable route first", "Lock a practical build now", "A good build page should make the first workable route clear before deeper optimization."),
                ("You may still redirect later", "Keep the build flexible", f"Do not over-tune gear if {compare['banner_name']} can still change your final account direction."),
                ("You care about resource safety", "Use fallback options first", "A lower-risk weapon and upgrade route protects your account from expensive overcommitment."),
            ]
        else:
            rows = [
                ("You want one practical team first", "Build a stable shell first", "The first shell should be easy to field and not depend on ideal future partners."),
                ("You only want to test before committing", "Use a fallback partner slot", "Leave room to swap one slot later instead of assuming the first shell is final."),
                ("You still need comparison room", "Avoid over-specialized teammates", f"Keep the team broad enough that {compare['banner_name']} can still change your direction."),
            ]
    rows_html = "\n".join(
        f"            <tr><td>{case}</td><td>{move}</td><td>{note}</td></tr>" for case, move, note in rows
    )
    return f"""    <section class="section">
      <h2>{character} scenario guide</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>If this is you</th><th>Best move</th><th>Why</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_playbook(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        if page["mode"] == "current":
            rows = [
                ("Safe bucket", "Credits, common drops, broad upgrade stock", f"These are the least risky ways to prep while {character} is already relevant in the live phase."),
                ("Confirm-at-live bucket", "Rare boss and weekly-locked items", f"These should wait for final in-game confirmation, especially if {compare['banner_name']} is still competing for your resources."),
                ("Do-not-overfarm bucket", "One-character-only routes with no overlap", "These are the first places where players waste stamina if they force the decision too early."),
            ]
        else:
            rows = [
                ("Safe bucket", "Shared materials and reusable stock", f"These are the right pre-farm targets while {character} is still part of {primary['banner_name']} planning rather than a confirmed live spend."),
                ("Wait-for-live bucket", "Rare locked drops and route-specific items", f"These should stay flexible until {character} is fully live or fully confirmed in-game."),
                ("Compare-first bucket", "Anything that competes directly with live-banner spending", f"If the live phase still matters, compare against {compare['banner_name']} before locking stamina."),
            ]
        section_title = f"{character} materials playbook"
    elif page["kind"] == "build":
        if page["mode"] == "current":
            rows = [
                ("Starter route", "Usable live build with fallback weapon logic", f"Best for accounts that need {character} working fast before worrying about perfect tuning."),
                ("Balanced route", "Role-first build with flexible stat expectations", f"Best when {character} matters but you still want room to pivot later."),
                ("High-commit route", "Premium path only after testing settles", f"This should wait until you are sure {character} beats the pull value in {compare['banner_name']}."),
            ]
        else:
            rows = [
                ("Preview route", "Role and fallback weapon path before release", f"Best for pre-planning {character} without pretending every detail is locked already."),
                ("Balanced route", "One safe build path that does not require ideal conditions", f"Best for accounts saving for {character} but still protecting pity and flexibility."),
                ("Release-day route", "Deep tuning after live confirmation", f"Only use this after {primary['banner_name']} goes fully live and {character} has real in-game evidence."),
            ]
        section_title = f"{character} build playbook"
    else:
        if page["mode"] == "current":
            rows = [
                ("Safe shell", "On-field core + sustain + broad support/flex", "Best for users who want one live team that works without perfect partners."),
                ("Test shell", f"{character} core + one flex partner left movable", f"Best for users who want to try {character} without freezing the whole roster around them."),
                ("Premium shell", "High-commit version after comfort is proven", f"Only push here if {character} still clearly beats redirecting toward {compare['banner_name']}."),
            ]
        else:
            rows = [
                ("Preview shell", "Role-first shell before final release testing", f"Best for planning {character} as a concept instead of locking one fragile lineup too early."),
                ("Comparison shell", f"One {character} shell versus one live-phase shell", f"Best for users deciding whether {character} really beats the immediate value in {compare['banner_name']}."),
                ("Premium shell", "Higher-commit version once live play confirms the role", f"Use this only after {character} has a clear live identity and the shell still feels worth the spend."),
            ]
        section_title = f"{character} team shell playbook"
    rows_html = "\n".join(
        f"            <tr><td>{lane}</td><td>{move}</td><td>{why}</td></tr>" for lane, move, why in rows
    )
    return f"""    <section class="section">
      <h2>{section_title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Lane</th><th>Best move</th><th>Why it exists</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_reference(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        rows = [
            ("Reusable stock", "Credits, common field drops, broad upgrade stock", "These are the safest materials to gather before any final lock-in."),
            ("Semi-locked stock", "Forte and route-specific farm planning", f"Useful if {character} remains the likely target, but still worth comparing against {compare['banner_name']}."),
            ("Live-confirm stock", "Rare boss, weekly, or route-locked items", f"Best confirmed after {character} is fully live in {primary['banner_name']}."),
        ]
        title = f"{character} materials reference layers"
    elif page["kind"] == "build":
        rows = [
            ("Role layer", "What job the character is filling", "This should be locked before any stat or weapon assumptions."),
            ("Weapon layer", "Fallback route and premium route", "A good build page should separate safe gear from aspirational gear."),
            ("Optimization layer", "Fine tuning after live feel", f"This is the part to delay until {primary['banner_name']} evidence settles."),
        ]
        title = f"{character} build reference layers"
    else:
        rows = [
            ("Core shell", "Main role plus sustain", "This is the first version a player should be able to use in practice."),
            ("Flexible shell", "One open slot for testing", "This keeps the page useful before perfect partner assumptions are proven."),
            ("High-commit shell", "Premium or narrow pairing route", "This should only be pushed once the broader shell already works."),
        ]
        title = f"{character} team shell reference layers"
    rows_html = "\n".join(
        f"            <tr><td>{layer}</td><td>{content}</td><td>{note}</td></tr>" for layer, content, note in rows
    )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Layer</th><th>What belongs here</th><th>Why it matters</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_checklist(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        items = [
            f"Check whether {character} is still your first resource target compared with {compare['banner_name']}.",
            "Separate low-risk shared farming from rare locked farming.",
            "Do not treat weekly or rare drops as mandatory until live confirmation.",
        ]
        title = f"{character} materials checklist before heavy farming"
    elif page["kind"] == "build":
        items = [
            f"Lock the role first, then choose the fallback weapon route for {character}.",
            "Keep one version of the build that does not depend on premium assumptions.",
            f"Delay deep optimization until {primary['banner_name']} live testing confirms the real feel.",
        ]
        title = f"{character} build checklist before full commitment"
    else:
        items = [
            f"Define what job {character} must solve before naming ideal partners.",
            "Keep one practical shell with sustain and one open testing slot.",
            f"Compare your first shell against the pull value still available in {compare['banner_name']}.",
        ]
        title = f"{character} team checklist before locking a shell"
    items_html = "\n".join(f"          <li>{item}</li>" for item in items)
    return f"""    <section class="section">
      <div class="card">
        <h2>{title}</h2>
        <ul class="list">
{items_html}
        </ul>
      </div>
    </section>"""


def build_focus_support_archetypes(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        if page["mode"] == "current":
            title = f"{character} material buckets"
            rows = [
                ("Always-safe stock", "Credits, broad shared drops, reusable upgrade stock", "Best for players who want to prepare without risking waste during the live phase."),
                ("Likely-safe stock", "Planned forte routes and shared progression routes", f"Best when {character} is already close to becoming your real spend target."),
                ("Live-confirm stock", "Rare or route-locked items", f"Best delayed until {character} is fully confirmed and still beats the pull direction in {compare['banner_name']}."),
            ]
        else:
            title = f"{character} material buckets"
            rows = [
                ("Pre-save stock", "Shared and reusable materials", f"Best for players already leaning toward {character} without overcommitting too early."),
                ("Soft-commit stock", f"Routes that matter if {character} stays your likely target", f"Useful while {character} is a strong candidate, but still compare against {compare['banner_name']}."),
                ("Release-lock stock", "Rare locked items and final route commitments", f"Best delayed until {primary['banner_name']} is live and {character} still looks worth the full spend."),
            ]
    elif page["kind"] == "build":
        if page["mode"] == "current":
            title = f"{character} build route names"
            rows = [
                ("Live-starter route", "Fast usable setup with fallback weapon logic", f"Best for getting {character} on the field quickly inside the current live phase."),
                ("Balanced route", "Role-first setup with flexible stat pressure", f"Best for players who want {character} usable without freezing every later decision."),
                ("High-commit route", "Premium path after comfort is proven", f"Best only after {character} still looks stronger than pivoting into {compare['banner_name']}."),
            ]
        else:
            title = f"{character} build route names"
            rows = [
                ("Preview route", "Plan role and fallback weapon before release", f"Best for pre-release planning {character} without pretending final testing is already done."),
                ("Balanced save route", "One dependable path that protects flexibility", f"Best for players saving for {character} while still guarding pity and live-banner options."),
                ("Release-day optimization route", "Full tuning only after live evidence", f"Best after {primary['banner_name']} goes live and {character} still looks like the correct spend."),
            ]
    else:
        if page["mode"] == "current":
            title = f"{character} shell archetypes"
            rows = [
                ("Safe live shell", "On-field core plus sustain plus one broad support", "Best for players who need one reliable live team now."),
                ("Testing shell", "Core plus one movable slot", f"Best for players who want to test {character} without rebuilding the whole roster."),
                ("Premium shell", "High-commit pairing after confidence is proven", f"Best only if {character} still wins over redirecting resources into {compare['banner_name']}."),
            ]
        else:
            title = f"{character} shell archetypes"
            rows = [
                ("Preview shell", "Role-first shell before full release testing", f"Best for players planning {character} conceptually rather than locking one fragile lineup too early."),
                ("Comparison shell", f"One {character} shell versus one live-phase shell", f"Best for deciding whether {character} really beats the immediate value still sitting in {compare['banner_name']}."),
                ("Premium live shell", "High-commit shell after release confidence", f"Best once {character} has a clear role and the shell still justifies the spend."),
            ]
    rows_html = "\n".join(
        f"            <tr><td>{name}</td><td>{setup}</td><td>{why}</td></tr>" for name, setup, why in rows
    )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Name</th><th>What it means</th><th>Best for</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_taxonomy(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        if page["mode"] == "current":
            title = f"{character} resource type breakdown"
            rows = [
                ("General account stock", "Credits, broad reusable stock, common drops", f"Safe to gather even if you later reduce {character} commitment."),
                ("Character-leaning stock", "Talent-route planning and likely overlap materials", f"Best for players who already think {character} will beat redirecting to {compare['banner_name']}."),
                ("Lock-after-live stock", "Boss, weekly, or route-locked items", f"Best confirmed only after {character} remains the preferred spend during {primary['banner_name']}."),
            ]
        else:
            title = f"{character} resource type breakdown"
            rows = [
                ("General save stock", "Credits, broad reusable stock, common drops", f"Good for players who are leaning toward {character} without forcing a final decision too early."),
                ("Targeted prep stock", "Character-specific route planning with some overlap value", f"Best when {character} is your likely save target but {compare['banner_name']} still matters."),
                ("Release-lock stock", "Final rare mats and strict route commitments", f"Best gathered after {primary['banner_name']} goes live and {character} still looks correct."),
            ]
    elif page["kind"] == "team-comps":
        if page["mode"] == "current":
            title = f"{character} role shell types"
            rows = [
                ("Safe live core", "Main damage slot plus sustain plus broad utility support", "Best for players who want one stable team right now."),
                ("Testing flex core", "Main role plus one moveable synergy slot", f"Best for players who want to test {character} without locking every teammate."),
                ("High-commit core", "Premium pairing around a narrower payoff", f"Best only if {character} still clearly beats the alternative value in {compare['banner_name']}."),
            ]
        else:
            title = f"{character} role shell types"
            rows = [
                ("Preview core", "Role-first shell before exact live strengths settle", "Best for early planning without overclaiming finished team data."),
                ("Comparison core", f"One {character}-first shell and one live-banner alternative shell", f"Best for players deciding whether {character} is really better than the value in {compare['banner_name']}."),
                ("Premium live core", "Narrower shell that assumes strong confidence after release", f"Best after {primary['banner_name']} is live and {character} still justifies the premium route."),
            ]
    else:
        return ""
    rows_html = "\n".join(
        f"            <tr><td>{kind}</td><td>{meaning}</td><td>{best_for}</td></tr>" for kind, meaning, best_for in rows
    )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Type</th><th>Meaning</th><th>Best use</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_execution(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        if page["mode"] == "current":
            title = f"{character} material ladder"
            rows = [
                ("Step 1", "Account-safe stock", "Credits, broad drops, reusable stock", f"Do this before deciding whether {character} gets the full live-phase resource share."),
                ("Step 2", "Character-leaning stock", "Likely forte overlap and route planning", f"Do this once {character} still looks stronger than redirecting into {compare['banner_name']}."),
                ("Step 3", "Locked stock", "Rare boss, weekly, and route-locked items", f"Do this only after {primary['banner_name']} live confirmation still keeps {character} as the priority."),
            ]
        else:
            title = f"{character} material ladder"
            rows = [
                ("Step 1", "Save-friendly stock", "Credits, broad reusable stock, common drops", f"Do this while {character} is a serious save target but not yet a finished live commitment."),
                ("Step 2", "Targeted prep stock", f"{character}-leaning prep with some overlap value", f"Do this once {character} still beats spending harder into {compare['banner_name']}."),
                ("Step 3", "Release-lock stock", "Rare and route-locked items", f"Do this only after {primary['banner_name']} goes live and {character} still holds the better spend case."),
            ]
        headers = "<th>Step</th><th>Bucket</th><th>What goes here</th><th>When to unlock it</th>"
        rows_html = "\n".join(
            f"            <tr><td>{step}</td><td>{bucket}</td><td>{content}</td><td>{when}</td></tr>"
            for step, bucket, content, when in rows
        )
    elif page["kind"] == "build":
        if page["mode"] == "current":
            title = f"{character} build fit matrix"
            rows = [
                ("You need a live answer now", "Live-starter route", f"{character} is already active inside the tracked phase, so fast usability matters more than perfect optimization."),
                ("You may still pivot later", "Balanced route", f"Use this when {character} matters but {compare['banner_name']} can still change your final account direction."),
                ("You only invest after comfort is proven", "High-commit route", "Use this only after the role, field time, and fallback weapon route all feel settled."),
            ]
        else:
            title = f"{character} build fit matrix"
            rows = [
                ("You are saving before release", "Preview route", f"Use this when you need a planning path before {character} has full live confirmation."),
                ("You want one safe route only", "Balanced save route", f"Use this when {character} still leads, but {compare['banner_name']} remains close enough to matter."),
                ("You commit only after release proof", "Release-day optimization route", f"Use this after {primary['banner_name']} goes live and {character} still clears the final spend check."),
            ]
        headers = "<th>Account state</th><th>Best route</th><th>Why it fits</th>"
        rows_html = "\n".join(
            f"            <tr><td>{state}</td><td>{route}</td><td>{why}</td></tr>"
            for state, route, why in rows
        )
    else:
        if page["mode"] == "current":
            title = f"{character} shell activation rules"
            rows = [
                ("Safe live shell", f"Use when you need one stable {character} team now", "Skip if the shell only works with narrow or unproven premium partners."),
                ("Testing shell", f"Use when you want {character} online with one moveable slot", "Skip if you already know the shell has to be fully locked today."),
                ("Premium shell", f"Use only if {character} still beats redirecting into {compare['banner_name']}", "Skip if live comfort is still shaky or the premium partner cost is too high."),
            ]
        else:
            title = f"{character} shell activation rules"
            rows = [
                ("Preview shell", f"Use when {character} is still a save-and-plan target", "Skip if you are treating pre-release theory as finished team proof."),
                ("Comparison shell", f"Use when you are actively comparing {character} against {compare['banner_name']}", f"Skip if you already know {character} is either a full skip or full commit."),
                ("Premium live shell", f"Use after {primary['banner_name']} goes live and {character} still wins the roster check", "Skip if the practical shell is not stable yet."),
            ]
        headers = "<th>Shell</th><th>Use it when</th><th>Do not use it when</th>"
        rows_html = "\n".join(
            f"            <tr><td>{shell}</td><td>{good}</td><td>{bad}</td></tr>"
            for shell, good, bad in rows
        )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr>{headers}</tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_sourcesplit(page: dict[str, str], snapshot: dict[str, object]) -> str:
    if page["kind"] != "materials":
        return ""
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["mode"] == "current":
        title = f"{character} material source groups"
        rows = [
            ("Open-world stock", "Common drops, broad reusable stock", f"Best gathered first because it stays useful even if {character} becomes a lower-priority spend."),
            ("Domain-style stock", "Planned forte and progression routes", f"Best gathered once {character} still clearly leads over saving harder for {compare['banner_name']}."),
            ("Boss and weekly stock", "Rare locked items with low flexibility", f"Best gathered only after {primary['banner_name']} live confirmation keeps {character} as the correct target."),
        ]
    else:
        title = f"{character} material source groups"
        rows = [
            ("Pre-release safe stock", "Credits, common drops, shared reusable stock", f"Best for saving toward {character} without converting soft prep into a hard commitment."),
            ("Targeted route stock", f"{character}-leaning prep with some overlap value", f"Best once {character} still beats spending more into {compare['banner_name']}."),
            ("Release-locked stock", "Rare boss and weekly route items", f"Best after {primary['banner_name']} goes live and {character} still wins the final spend comparison."),
        ]
    rows_html = "\n".join(
        f"            <tr><td>{group}</td><td>{content}</td><td>{note}</td></tr>" for group, content, note in rows
    )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Source group</th><th>What belongs here</th><th>Why it matters</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_fit_rules(page: dict[str, str], snapshot: dict[str, object]) -> str:
    if page["kind"] != "build":
        return ""
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["mode"] == "current":
        title = f"{character} build use and avoid cases"
        rows = [
            ("Live-starter route", f"Use when you need {character} field-ready quickly in the current phase.", "Avoid if you are actually saving most resources for a likely Phase 2 pivot."),
            ("Balanced route", f"Use when {character} matters but later redirects are still possible.", f"Avoid if you already know {character} clearly beats every option in {compare['banner_name']} and you want the higher-commit route."),
            ("High-commit route", "Use after role feel and fallback weapon logic are stable.", "Avoid if your account still depends on fragile premium assumptions."),
        ]
    else:
        title = f"{character} build use and avoid cases"
        rows = [
            ("Preview route", f"Use while {character} is still a planning target before release.", "Avoid if you are treating preview assumptions as final live proof."),
            ("Balanced save route", f"Use when you want one safe {character} path without losing flexibility.", f"Avoid if {compare['banner_name']} is obviously the better immediate spend and {character} is slipping into backup status."),
            ("Release-day optimization route", f"Use after {primary['banner_name']} goes live and {character} still wins the account check.", "Avoid if release-day testing still leaves major uncertainty about role or weapon path."),
        ]
    rows_html = "\n".join(
        f"            <tr><td>{route}</td><td>{use_case}</td><td>{avoid_case}</td></tr>"
        for route, use_case, avoid_case in rows
    )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Route</th><th>Use it when</th><th>Avoid it when</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_replacements(page: dict[str, str], snapshot: dict[str, object]) -> str:
    if page["kind"] != "team-comps":
        return ""
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["mode"] == "current":
        title = f"{character} shell replacement logic"
        rows = [
            ("Core slot", character, f"This slot should only move if the whole {character} pull decision changes."),
            ("Sustain slot", "Broad sustain option", "Replace this first if the shell works but comfort is poor."),
            ("Flex support slot", "Utility or synergy support", f"Replace this when {compare['banner_name']} or another roster need changes the best partner choice."),
        ]
    else:
        title = f"{character} shell replacement logic"
        rows = [
            ("Core slot", character, f"This slot only changes if {character} loses the bigger pull comparison entirely."),
            ("Practical sustain slot", "Stable sustain option", "Replace this before forcing a narrower premium shell."),
            ("Comparison flex slot", "One open roster-dependent slot", f"Replace this when release testing or {compare['banner_name']} changes the best practical shell."),
        ]
    rows_html = "\n".join(
        f"            <tr><td>{slot}</td><td>{default}</td><td>{replace_when}</td></tr>"
        for slot, default, replace_when in rows
    )
    return f"""    <section class="section">
      <h2>{title}</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Slot</th><th>Default idea</th><th>When to replace it</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def build_focus_support_usage_rules(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        good_title = f"When this {character} materials route is right"
        bad_title = f"When this {character} materials route is too early"
        good_body = f"Use this route when {character} is already your leading target and you want to separate reusable stock from risky locked farming before spending more stamina."
        bad_body = f"Do not use this as a full green light to hard-farm every route if {compare['banner_name']} is still competing for your resources or if rare drops are not fully confirmed in-game."
    elif page["kind"] == "build":
        good_title = f"When this {character} build route is right"
        bad_title = f"When this {character} build route is too early"
        good_body = f"Use this route when you need one workable version of {character} first, and you want to avoid overcommitting to premium tuning before the role is fully proven."
        bad_body = f"Do not treat the high-commit route as mandatory if the role is still unclear, if premium assumptions are fragile, or if {compare['banner_name']} still offers a better use of your pity and resources."
    else:
        good_title = f"When this {character} shell logic is right"
        bad_title = f"When this {character} shell logic is too early"
        good_body = f"Use these shell types when you want one practical team frame, one flexible test frame, and one higher-commit option instead of pretending every account needs the same lineup."
        bad_body = f"Do not lock a narrow premium shell too early if {character} still needs live testing or if the live or competing phase can still change your best team direction."
    return f"""    <section class="section two-col">
      <div class="card">
        <h2>{good_title}</h2>
        <p>{good_body}</p>
      </div>
      <div class="card">
        <h2>{bad_title}</h2>
        <p>{bad_body}</p>
      </div>
    </section>"""


def build_focus_support_live_checks(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    primary, compare = support_phase_context(page, snapshot)
    if page["kind"] == "materials":
        items = [
            f"Confirm {character} is still your main target once {primary['banner_name']} status is fully settled.",
            "Confirm rare and weekly-locked routes before converting soft prep into full commitment.",
            f"Re-check whether the competing value in {compare['banner_name']} still changes your farming priority.",
        ]
        title = f"{character} live confirmation checks for materials"
    elif page["kind"] == "build":
        items = [
            f"Confirm the real role feel of {character} before moving from balanced route to high-commit route.",
            "Confirm that the fallback weapon route still feels acceptable before investing into narrow premium assumptions.",
            f"Re-check whether your best live value still comes from {character} instead of redirecting into {compare['banner_name']}.",
        ]
        title = f"{character} live confirmation checks for build"
    else:
        items = [
            f"Confirm the first practical shell feels stable before upgrading into a narrower {character} shell.",
            "Confirm whether the flexible slot actually needs to be locked or should stay open longer.",
            f"Re-check whether the shell still beats the most practical alternative tied to {compare['banner_name']}.",
        ]
        title = f"{character} live confirmation checks for team shells"
    items_html = "\n".join(f"          <li>{item}</li>" for item in items)
    return f"""    <section class="section">
      <div class="card">
        <h2>{title}</h2>
        <ul class="list">
{items_html}
        </ul>
      </div>
    </section>"""


def build_support_related(page: dict[str, str]) -> str:
    character = page["character"]
    slug = page["slug"]
    context_copy = (
        f"{character} is part of the live tracked phase, so the best path is to keep this page connected to current-banner timing, current weapons, and immediate pull decisions."
        if page["mode"] == "current"
        else f"{character} is part of the next tracked phase, so this page should help users compare pre-farm and save decisions against the still-live current banner."
    )
    return f"""    <section class="section two-col">
      <div class="card">
        <h2>Related pages</h2>
        <ul class="list">
          <li><a href="{character_hub_path(slug)}">{character} guide hub</a></li>
          <li><a href="/wuthering-waves-should-you-pull-{slug}/">Should you pull {character}?</a></li>
          <li><a href="{support_page_path(slug, "materials")}">{character} materials</a></li>
          <li><a href="{support_page_path(slug, "build")}">{character} build</a></li>
          <li><a href="{support_page_path(slug, "team-comps")}">{character} team comps</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>How this page should be used</h2>
        <p>{context_copy}</p>
      </div>
    </section>"""


def build_support_faq(page: dict[str, str]) -> str:
    character = page["character"]
    if page["kind"] == "materials":
        return f"""      <div class="faq-list">
        <article class="faq-item"><h3>Should you pre-farm {character} materials before final confirmation?</h3><p>Pre-farm only the low-risk routes first, then wait for official or in-game confirmation before overcommitting to rare or weekly materials.</p></article>
        <article class="faq-item"><h3>What should a good {character} materials page show?</h3><p>It should show ascension, forte, boss, and overlap planning in one place, plus clear notes on what is safe to farm early.</p></article>
      </div>"""
    if page["kind"] == "build":
        return f"""      <div class="faq-list">
        <article class="faq-item"><h3>What should you lock first on a {character} build page?</h3><p>Lock the role, fallback weapon route, and broad upgrade order first. Save fine-tuned optimization for after official and live confirmation settles.</p></article>
        <article class="faq-item"><h3>Why should a {character} build page stay connected to banner pages?</h3><p>Because users usually move from pull intent into build planning, not into a disconnected guide tree.</p></article>
      </div>"""
    return f"""      <div class="faq-list">
        <article class="faq-item"><h3>What should you decide first on a {character} team comps page?</h3><p>Decide the role slot {character} must fill for your account before chasing idealized partner lists.</p></article>
        <article class="faq-item"><h3>Why should {character} team comps stay in the banner cluster?</h3><p>Because team planning is one of the main reasons users move from “should I pull” into deeper character pages.</p></article>
      </div>"""


def build_support_sources(page: dict[str, str], updated: str) -> str:
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} {page["kind_label"].lower()} snapshot</strong><br>
        Character phase source: {page["source_url"]}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>"""


def render_support_page(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = html.escape(page["character"])
    kind = page["kind"]
    kind_label = page["kind_label"]
    path = page["path"]
    title = f"Wuthering Waves {page['character']} {kind_label} | WuWa Banners"
    description = f"Use this {page['character']} {kind_label.lower()} page for banner-linked planning, fast internal links, and a cleaner update path as official details settle."
    og_description = f"A focused {page['character']} {kind_label.lower()} support page connected to banner timing, pull advice, and account planning."
    faq_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": f"Wuthering Waves {page['character']} {kind_label}",
                    "description": description,
                    "author": {"@type": "Organization", "name": "WuWa Banners"},
                    "publisher": {"@type": "Organization", "name": "WuWa Banners"},
                    "mainEntityOfPage": f"https://wuwabanners.net{path}",
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": f"What should a {page['character']} {kind_label.lower()} page answer first?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": f"It should answer the fastest account-planning question first, then link back to banner timing, pity, and pull advice for {page['character']}."
                            },
                        },
                        {
                            "@type": "Question",
                            "name": f"Why keep {page['character']} {kind_label.lower()} inside the banner site structure?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Because users usually reach these pages from a current-banner or next-banner decision, not from a standalone character database query."
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="Wuthering Waves {character} {kind_label}">
  <meta property="og:description" content="{html.escape(og_description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="/guides/">Guides</a> / <a href="{character_hub_path(page["slug"])}">{character}</a> / {kind_label}</div>
    <h1>Wuthering Waves {character} {kind_label}</h1>
{build_support_intro(page, snapshot)}
{build_support_media(page)}
{build_support_cards(page, snapshot)}
{build_support_strategy(page, snapshot)}
{build_support_branch_context(page, snapshot)}
{build_focus_character_module(page, snapshot)}
{build_focus_support_cases(page, snapshot)}
{build_focus_support_playbook(page, snapshot)}
{build_focus_support_archetypes(page, snapshot)}
{build_focus_support_taxonomy(page, snapshot)}
{build_focus_support_execution(page, snapshot)}
{build_focus_support_sourcesplit(page, snapshot)}
{build_focus_support_fit_rules(page, snapshot)}
{build_focus_support_replacements(page, snapshot)}
{build_focus_support_usage_rules(page, snapshot)}
{build_focus_support_reference(page, snapshot)}
{build_support_table(page)}
{build_support_priority_lanes(page, snapshot)}
{build_focus_support_checklist(page, snapshot)}
{build_focus_support_live_checks(page, snapshot)}
{build_support_related(page)}
    <section class="section">
      <h2>FAQ</h2>
{build_support_faq(page)}
{build_support_sources(page, snapshot["updated"])}
    </section>
  </div></main>
  <script defer src="/assets/js/site.js"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def render_character_page(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = html.escape(page["character"])
    slug = page["slug"]
    description = (
        f"Use this {page['character']} pull advice page to decide whether the current phase is worth your resources."
        if page["mode"] == "current"
        else f"Use this {page['character']} pull advice page to decide whether saving for the next phase is better than spending on the current banner."
    )
    og_description = (
        f"A focused pull-decision page for {page['character']} connected to current banner, pity, and rerun planning."
        if page["mode"] == "current"
        else f"A focused pull-decision page for {page['character']} connected to next banner, pity, and rerun planning."
    )
    title = f"Should You Pull {page['character']} in Wuthering Waves? | WuWa Banners"
    page_url = f"https://wuwabanners.net/wuthering-waves-should-you-pull-{slug}/"
    faq_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": f"Should You Pull {page['character']} in Wuthering Waves?",
                    "description": description,
                    "author": {"@type": "Organization", "name": "WuWa Banners"},
                    "publisher": {"@type": "Organization", "name": "WuWa Banners"},
                    "mainEntityOfPage": page_url,
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": "Should you pull this character now?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Compare your current roster needs, pity progress, the live banner end date, and whether saving for the next phase or a rerun is more efficient."
                            },
                        },
                        {
                            "@type": "Question",
                            "name": "What should you check before deciding?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Check pity carry-over, current and next phase timing, and whether this character solves a bigger account problem than your alternatives."
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{page_url}">
  <meta property="og:title" content="Should You Pull {character} in Wuthering Waves?">
  <meta property="og:description" content="{html.escape(og_description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{page_url}">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="/pull-advice/">Pull advice</a> / {character}</div>
    <h1>Should You Pull {character} in Wuthering Waves?</h1>
{build_character_intro(page, snapshot)}
{build_character_media(page)}
{build_character_blocks(page, snapshot)}
{build_character_decision_matrix(page, snapshot)}
{build_character_support_links(page)}
    <section class="section">
      <h2>FAQ</h2>
{build_character_faq(page)}
{build_character_sources(page, snapshot["updated"])}
    </section>
  </div></main>
  <script defer src="/assets/js/site.js"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def build_character_overview_entry_routes(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    slug = page["slug"]
    compare = snapshot["next"] if page["mode"] == "current" else snapshot["current"]
    if page["mode"] == "current":
        rows = [
            (
                "You still do not know whether to spend now",
                f"Should you pull {character}?",
                f"Start here if the main question is whether {character} beats saving for {compare['banner_name']}.",
                f"/wuthering-waves-should-you-pull-{slug}/",
            ),
            (
                "You already want the character and need safe prep",
                f"{character} materials",
                "Start here if you want to separate low-risk farming from route-locked farming before spending more stamina.",
                support_page_path(slug, "materials"),
            ),
            (
                "You need one usable setup fast",
                f"{character} build",
                "Start here if your next question is weapon route, role framing, or what to lock before deeper optimization.",
                support_page_path(slug, "build"),
            ),
            (
                "You want one practical team first",
                f"{character} team comps",
                "Start here if you need a workable shell before testing premium or narrower lineups.",
                support_page_path(slug, "team-comps"),
            ),
        ]
    else:
        rows = [
            (
                "You are still comparing save versus spend-now",
                f"Should you pull {character}?",
                f"Start here if the main question is whether {character} is worth saving for instead of spending into {compare['banner_name']}.",
                f"/wuthering-waves-should-you-pull-{slug}/",
            ),
            (
                "You want a pre-farm plan without overcommitting",
                f"{character} materials",
                "Start here if you want to split safe stock, targeted prep, and release-locked farming before the phase is fully live.",
                support_page_path(slug, "materials"),
            ),
            (
                "You want a pre-release build path",
                f"{character} build",
                "Start here if you need a preview route, fallback weapon logic, and a safe way to avoid premature optimization.",
                support_page_path(slug, "build"),
            ),
            (
                "You want one realistic shell to compare",
                f"{character} team comps",
                "Start here if you need a practical shell and one flexible comparison route before locking partners.",
                support_page_path(slug, "team-comps"),
            ),
        ]
    cards = "\n".join(
        f"""        <article class="card">
          <h3>{question}</h3>
          <p><strong>{page_name}</strong></p>
          <p>{why}</p>
          <p><a href="{href}">Open {page_name}</a></p>
        </article>"""
        for question, page_name, why, href in rows
    )
    return f"""    <section class="section">
      <h2>Fastest starting points for {character}</h2>
      <div class="card-grid">
{cards}
      </div>
    </section>"""


def build_character_overview_decision_split(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    compare = snapshot["next"] if page["mode"] == "current" else snapshot["current"]
    if page["mode"] == "current":
        rows = [
            ("Spend decision first", f"Open pull advice before any farming if you still need to decide whether {character} is better than waiting for {compare['banner_name']}."),
            ("Farm decision first", f"Open materials first if you are already likely to spend and mainly need to protect stamina from overfarming."),
            ("Build decision first", f"Open build first if the real blocker is role shape, fallback weapon path, or upgrade order."),
            ("Team decision first", "Open team comps first if your account already knows the unit matters and the real question is shell stability."),
        ]
    else:
        rows = [
            ("Save decision first", f"Open pull advice before prep if you still need to decide whether saving for {character} beats spending into {compare['banner_name']}."),
            ("Soft-prep decision first", "Open materials first if you want the safest pre-release prep without converting that prep into a hard commitment."),
            ("Preview-build decision first", "Open build first if you want a route that stays usable before live testing fully settles."),
            ("Comparison-shell decision first", "Open team comps first if the real question is what practical shell would justify the save."),
        ]
    items_html = "\n".join(f"          <li><strong>{label}:</strong> {copy}</li>" for label, copy in rows)
    return f"""    <section class="section two-col">
      <div class="card">
        <h2>Choose your next page by question type</h2>
        <ul class="list">
{items_html}
        </ul>
      </div>
      <div class="card">
        <h2>Why this branch exists</h2>
        <p>The {character} hub should shorten the path from “I know the character name” to “I know which page solves my next question.” That is the main job of this layer between the character list and the deeper support pages.</p>
      </div>
    </section>"""


def build_character_overview_account_fit(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    compare = snapshot["next"] if page["mode"] == "current" else snapshot["current"]
    if page["mode"] == "current":
        rows = [
            (
                "Best when you need a live answer",
                f"Use {character} first if the current phase is where you are actually willing to spend.",
                f"This keeps the decision tied to the live window instead of drifting into vague comparison with {compare['banner_name']}.",
            ),
            (
                "Best when you need safe prep",
                f"Open {character} materials or build if the spend case is already mostly settled and the real risk is wasting stamina or upgrade stock.",
                "That route is stronger than reopening broad banner pages once the unit choice is mostly clear.",
            ),
            (
                "Not the best start when you are still saving",
                f"Leave this branch and go back to pull advice if {compare['banner_name']} is still the real candidate.",
                "The character hub is strongest after the unit question is mostly settled.",
            ),
        ]
    else:
        rows = [
            (
                "Best when you are planning ahead",
                f"Use {character} first if the next phase is the likely spend target and you want one clean place to compare prep, build, and shell routes.",
                f"That keeps the save decision tied to {compare['banner_name']} as the current alternative.",
            ),
            (
                "Best when you only want soft prep",
                f"Open {character} materials or build if you want low-risk preparation without converting it into a hard release-day commitment.",
                "This is the cleanest route for next-phase planning without overcommitting too early.",
            ),
            (
                "Not the best start when the live phase still wins",
                f"Go back to current banner or pull advice if {compare['banner_name']} is still the spend favorite.",
                "The character hub is stronger once the save direction is mostly settled.",
            ),
        ]
    rows_html = "\n".join(
        f"""            <tr><td>{label}</td><td>{best_move}</td><td>{why}</td></tr>"""
        for label, best_move, why in rows
    )
    return f"""    <section class="section">
      <h2>{character} account fit at a glance</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Situation</th><th>Best move</th><th>Why</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>"""


def render_character_overview_page(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = html.escape(page["character"])
    slug = page["slug"]
    path = page["path"]
    phase_copy = "current tracked phase" if page["mode"] == "current" else "next tracked phase"
    compare = snapshot["next"] if page["mode"] == "current" else snapshot["current"]
    title = f"Wuthering Waves {page['character']} Guide Hub | WuWa Banners"
    description = f"Browse the Wuthering Waves {page['character']} guide hub with pull advice, materials, build, and team comps pages in one place."
    faq_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "name": f"Wuthering Waves {page['character']} Guide Hub",
                    "url": f"https://wuwabanners.net{path}",
                    "isPartOf": {
                        "@type": "WebSite",
                        "name": "WuWa Banners",
                        "url": "https://wuwabanners.net/",
                    },
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": f"What should a {page['character']} overview page do first?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": f"It should route users into the fastest next page: pull advice, materials, build, or team comps, depending on where they are in the decision process for {page['character']}."
                            },
                        },
                        {
                            "@type": "Question",
                            "name": "Why make a character overview page instead of only support pages?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Because a clean overview page makes the site structure easier to scan and keeps character intent from scattering across unrelated URLs."
                            },
                        },
                    ],
                },
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="Wuthering Waves {character} Guide Hub">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="/guides/">Guides</a> / <a href="/wuthering-waves-characters/">Characters</a> / {character}</div>
    <h1>Wuthering Waves {character} Guide Hub</h1>
    <p class="lead">{character} is part of the {phase_copy}. This page works as the clean detail layer between the characters list and the deeper support pages, so users can choose the exact next page without guessing.</p>
    <div class="answer-box"><strong>Direct answer:</strong> Use the {character} overview page when you want one place that links pull advice, materials, build, and team comps. That is more useful than dropping users directly into one narrow page if they have not decided what they need yet.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(snapshot["updated"] + " 00:00")}.</p>
{build_character_overview_media(page, snapshot)}
    <div class="card-grid">
      <article class="card"><h2>Tracked phase</h2><p>{character} is currently tied to {html.escape(page["phase_label"])}.</p></article>
      <article class="card"><h2>Banner window</h2><p>{fmt_human_date(page["start_date"])} to {fmt_human_date(page["end_date"])}</p></article>
      <article class="card"><h2>Compare point</h2><p>If you are still deciding, compare this route against {html.escape(compare["banner_name"])} before locking resources.</p></article>
    </div>
{build_character_overview_entry_routes(page, snapshot)}
{build_character_overview_decision_split(page, snapshot)}
{build_character_overview_account_fit(page, snapshot)}
    <section class="section">
      <h2>How to use the {character} hub</h2>
      <div class="card-grid">
        <article class="card"><h3>1. Start here if you know the character</h3><p>Use this hub after the characters list when you already know the unit you care about but still need to choose which narrow page to open next.</p></article>
        <article class="card"><h3>2. Open the decision page first</h3><p>If the main question is still whether to spend, open the pull page before you drop into materials, build, or team comps.</p></article>
        <article class="card"><h3>3. Go into one support page</h3><p>Only after the main decision is clear should you move into one support page and keep the next click inside the same {character} branch.</p></article>
      </div>
    </section>
    <section class="section">
      <h2>{character} page list</h2>
      <div class="card-grid">
        <article class="card"><h2>Should you pull {character}?</h2><p>Start here if your main question is whether {character} is worth spending on right now.</p><p><a href="/wuthering-waves-should-you-pull-{slug}/">Open pull advice</a></p></article>
        <article class="card"><h2>{character} materials</h2><p>Use this page for pre-farm planning, ascension notes, and safe-versus-risky material decisions.</p><p><a href="{support_page_path(slug, "materials")}">Open materials</a></p></article>
        <article class="card"><h2>{character} build</h2><p>Use this page for role framing, early upgrade order, and practical build decisions.</p><p><a href="{support_page_path(slug, "build")}">Open build</a></p></article>
        <article class="card"><h2>{character} team comps</h2><p>Use this page for role slot decisions, fallback shell planning, and realistic team structure.</p><p><a href="{support_page_path(slug, "team-comps")}">Open team comps</a></p></article>
      </div>
    </section>
    <section class="section two-col">
      <div class="card">
        <h2>{character} branch context</h2>
        <p>{character} sits between the broad character list and the narrow support pages. This hub should stop users from bouncing between unrelated guides just because they have not chosen whether they need pull advice, materials, build, or teams yet.</p>
        <div class="reference-directory">
          <a class="directory-link" href="/wuthering-waves-characters/">Back to characters list</a>
          <a class="directory-link" href="/wuthering-waves-should-you-pull-{slug}/">Open pull page</a>
          <a class="directory-link" href="{support_page_path(slug, "materials")}">Open materials</a>
          <a class="directory-link" href="{support_page_path(slug, "build")}">Open build</a>
          <a class="directory-link" href="{support_page_path(slug, "team-comps")}">Open team comps</a>
        </div>
      </div>
      <div class="card">
        <h2>What to compare before committing</h2>
        <p>Do not read {character} in isolation. Compare the spend case, the farm case, and the roster-pressure case against {html.escape(compare["banner_name"])} so this hub helps users make a real account choice instead of only opening more tabs.</p>
      </div>
    </section>
    <section class="section two-col">
      <div class="card">
        <h2>Best next pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-should-you-pull-{slug}/">Should you pull {character}?</a></li>
          <li><a href="{support_page_path(slug, "materials")}">{character} materials</a></li>
          <li><a href="{support_page_path(slug, "build")}">{character} build</a></li>
          <li><a href="{support_page_path(slug, "team-comps")}">{character} team comps</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>How this page should be used</h2>
        <p>Use the characters list for scanning. Use this character hub when you know the unit you care about but still need to choose whether your next click should be pull advice, materials, build, or team comps.</p>
      </div>
    </section>
    <section class="section">
      <h2>FAQ</h2>
      <div class="faq-list">
        <article class="faq-item"><h3>What should a {character} overview page do first?</h3><p>It should route you into the fastest next page: pull advice, materials, build, or team comps.</p></article>
        <article class="faq-item"><h3>Why make a character overview page instead of only support pages?</h3><p>Because a clean overview page makes the structure easier to scan and stops character intent from scattering across unrelated URLs.</p></article>
      </div>
      <div class="sources">
        <strong>Source used for this {character} overview page</strong><br>
        Character phase source: {html.escape(page["source_url"])}<br>
        Official video archive: https://www.youtube.com/@WutheringWaves
      </div>
    </section>
  </div></main>
  <script defer src="/assets/js/site.js"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def render_sitemap(extra_urls: list[str]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in BASE_URLS + extra_urls:
        lines.append(f"  <url><loc>{url}</loc></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def discover_reference_urls() -> list[str]:
    urls: list[str] = []
    for section in ("wuthering-waves-characters", "wuthering-waves-weapons", "wuthering-waves-items"):
        base = ROOT / section
        if not base.exists():
            continue
        for path in sorted(base.glob("*/index.html")):
            slug = path.parent.name
            if slug == "index":
                continue
            urls.append(f"https://wuwabanners.net/{section}/{slug}/")
    return urls


def render_card_grid(cards: list[tuple[str, str]]) -> str:
    items = "\n".join(f'      <article class="card"><h2>{title}</h2><p>{copy}</p></article>' for title, copy in cards)
    return f"""    <div class="card-grid" style="margin-top:1.25rem;">
{items}
    </div>"""


def render_faq_block(items: list[tuple[str, str]]) -> str:
    return "\n".join(f'        <article class="faq-item"><h3>{question}</h3><p>{answer}</p></article>' for question, answer in items)


def render_faq_json(title: str, path: str, items: list[tuple[str, str]]) -> str:
    payload = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": title,
                "mainEntityOfPage": f"https://wuwabanners.net{path}",
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in items
                ],
            },
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_standard_page(
    *,
    title: str,
    description: str,
    path: str,
    breadcrumbs: str,
    heading: str,
    lead: str,
    answer: str,
    body: str,
    faq_items: list[tuple[str, str]],
) -> str:
    faq_json = render_faq_json(title, path, faq_items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="https://wuwabanners.net{path}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net{path}">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs">{breadcrumbs}</div>
    <h1>{html.escape(heading)}</h1>
    <p class="lead">{lead}</p>
    <div class="answer-box"><strong>Direct answer:</strong> {answer}</div>
{body}
    <section class="section">
      <h2>FAQ</h2>
      <div class="faq-list">
{render_faq_block(faq_items)}
      </div>
    </section>
  </div></main>
<script defer src="/assets/js/site.js"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def render_next_banner_date_page(snapshot: dict[str, object]) -> str:
    next_item = snapshot["next"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    if is_preview_phase(next_item):
        answer = f"As of {updated}, the next official banner-related date is {phase_event_label(next_item)} for {next_item['banner_name']}. The full next phase start date is still unconfirmed."
        next_title = "Next official preview"
        next_copy = next_event_copy(next_item)
        table_value = "Full lineup pending official confirmation"
    else:
        answer = f"As of {updated}, the next tracked banner date is {fmt_human_date(next_item['start_date'])}, when {next_item['banner_name']} is scheduled to begin."
        next_title = "Next phase start"
        next_copy = f"{next_item['banner_name']} is scheduled to start on {fmt_human_date(next_item['start_date'])}."
        table_value = ", ".join(next_item["featured_characters"])
    body = "\n".join(
        [
            render_card_grid(
                [
                    (next_title, next_copy),
                    ("Why users search this", "This is usually a planning query right before a pull or save decision."),
                    ("Best next pages", "The best follow-up pages are next banner, countdown, and banner schedule."),
                ]
            ),
            f"""    <section class="section">
      <h2>Next date snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>Date</th><th>Tracked focus</th><th>Best next page</th></tr></thead>
          <tbody>
            <tr><td>{next_item["banner_name"]}</td><td>{phase_event_label(next_item)}</td><td>{table_value}</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
            """    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
          <li><a href="/wuthering-waves-banner-countdown/">Banner countdown</a></li>
          <li><a href="/wuthering-waves-banner-schedule/">Banner schedule</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why keep this separate</h2>
        <p>A date page can stay much tighter than a full next-banner article, which makes it useful for narrow search intent.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Next Banner Date | WuWa Banners",
        description="Check the Wuthering Waves next banner date, including the next official banner-related timing and the best follow-up pages.",
        path="/wuthering-waves-next-banner-date/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Next banner date',
        heading="Wuthering Waves Next Banner Date",
        lead="Date-intent pages should be brutally clear. Users searching for the next banner date want one line first, then the smallest amount of supporting timing context needed to feel confident.",
        answer=answer,
        body=body,
        faq_items=[
            ("When is the next Wuthering Waves banner date?", answer),
            ("Which page should users open after checking the next banner date?", "Usually the next banner page, banner countdown page, or banner schedule page."),
        ],
    )


def render_current_banner_end_date_page(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    answer = f"As of {updated}, the current tracked banner end date is {fmt_human_date(current['end_date'])}, when {current['banner_name']} is scheduled to end."
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Live phase deadline", f"{current['banner_name']} remains live through {fmt_human_date(current['end_date'])}."),
                    ("Why users search this", "This query usually appears right before someone decides whether to pull now or save."),
                    ("Best next pages", "The strongest next steps are current banner, next banner, and pity system."),
                ]
            ),
            f"""    <section class="section">
      <h2>Current end-date snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>End date</th><th>Featured characters</th><th>Best next page</th></tr></thead>
          <tbody>
            <tr><td>{current["banner_name"]}</td><td>{fmt_human_date(current["end_date"])}</td><td>{", ".join(current["featured_characters"])}</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
            """    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-current-banner/">Current banner</a></li>
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
          <li><a href="/wuthering-waves-pity-system/">Pity system</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why this page is useful</h2>
        <p>Deadline-intent pages can rank separately from broader overview pages because they answer a narrower, more urgent question.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Current Banner End Date | WuWa Banners",
        description="Check the Wuthering Waves current banner end date, including the live phase deadline and the best pages to open before banners rotate.",
        path="/wuthering-waves-current-banner-end-date/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Current banner end date',
        heading="Wuthering Waves Current Banner End Date",
        lead="End-date pages are deadline pages. Users land here when they are close to making a decision and need a clear date more than a broad explanation.",
        answer=answer,
        body=body,
        faq_items=[
            ("When does the current Wuthering Waves banner end?", answer),
            ("What should users check before the current banner ends?", "Usually the current banner page, the next banner page, and the pity system before deciding how to spend resources."),
        ],
    )


def render_current_banner_characters_page(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    answer = f"As of {updated}, the current tracked featured characters are {', '.join(current['featured_characters'])} in {current['banner_name']}, which runs through {fmt_human_date(current['end_date'])}."
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Live lineup", f"The current tracked featured characters are {', '.join(current['featured_characters'])}."),
                    ("Current phase timing", f"{current['banner_name']} remains live through {fmt_human_date(current['end_date'])}."),
                    ("Best next pages", "After checking the current lineup, users usually want the current banner page, a pull page, or the pity system."),
                ]
            ),
            f"""    <section class="section">
      <h2>Current featured character snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>Featured characters</th><th>End date</th><th>Best next page</th></tr></thead>
          <tbody>
            <tr><td>{current["banner_name"]}</td><td>{", ".join(current["featured_characters"])}</td><td>{fmt_human_date(current["end_date"])}</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
            """    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-current-banner/">Current banner</a></li>
          <li><a href="/pull-advice/">Pull advice</a></li>
          <li><a href="/wuthering-waves-pity-system/">Pity system</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why this page is separate</h2>
        <p>It answers a narrower search than the broader current-banner page, which gives it a cleaner first screen and clearer CTR intent.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Current Banner Characters | WuWa Banners",
        description="Check the Wuthering Waves current banner characters, including the live featured lineup, phase timing, and the best follow-up pages.",
        path="/wuthering-waves-current-banner-characters/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Current banner characters',
        heading="Wuthering Waves Current Banner Characters",
        lead="This page exists for narrow intent. Some users do not want the full current-banner article first. They only want the current featured characters, then a quick path into the right decision page.",
        answer=answer,
        body=body,
        faq_items=[
            ("Who are the current Wuthering Waves banner characters?", answer),
            ("What should users check after the current banner characters?", "Most users should move to the current banner page, pull-advice hub, or pity system depending on whether they are about to spend resources."),
        ],
    )


def render_next_character_page(snapshot: dict[str, object]) -> str:
    next_item = snapshot["next"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    if next_item["featured_characters"]:
        answer = f"As of {updated}, the next tracked featured characters are {', '.join(next_item['featured_characters'])} in {next_item['banner_name']}, beginning on {fmt_human_date(next_item['start_date'])}."
        lead_card = ("Next phase lead", f"{next_focus_name(next_item)} is the lead next-phase name users are likely to compare first against the current phase.")
        support_card = ("Next phase support names", f"{', '.join(next_item['featured_characters'][1:]) or next_focus_name(next_item)} matter because users often search companion units separately after seeing the main next-banner page.")
        table_focus = ", ".join(next_item["featured_characters"])
        related_link = f'<li><a href="/wuthering-waves-should-you-pull-{slugify_character(next_focus_name(next_item))}/">Should you pull {next_focus_name(next_item)}?</a></li>'
    else:
        answer = f"As of {updated}, the next full featured-character lineup is still unconfirmed. The next official banner-related checkpoint is {next_item['banner_name']} on {phase_event_label(next_item)}."
        lead_card = ("No official next featured character yet", "The next full lineup has not been posted yet, so the safest answer is to wait for the next official preview or notice.")
        support_card = ("What to watch next", next_event_copy(next_item))
        table_focus = "Full lineup pending official confirmation"
        related_link = '<li><a href="/pull-advice/">Pull advice</a></li>'
    body = "\n".join(
        [
            render_card_grid(
                [
                    lead_card,
                    support_card,
                    ("What users usually need next", "After this page, most users need the next-banner page, the schedule page, or pull-advice context."),
                ]
            ),
            f"""    <section class="section">
      <h2>Next featured character snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>Tracked focus</th><th>Date</th><th>Best next page</th></tr></thead>
          <tbody>
            <tr><td>{next_item["banner_name"]}</td><td>{table_focus}</td><td>{phase_event_label(next_item)}</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
            f"""    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
          <li><a href="/wuthering-waves-banner-schedule/">Banner schedule</a></li>
          {related_link}
        </ul>
      </div>
      <div class="card">
        <h2>Why this page is separate</h2>
        <p>Some searchers do not ask for the full next banner. They ask for the next character directly, so the answer should be more focused and immediately scannable.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Next Character | WuWa Banners",
        description="Track the next Wuthering Waves featured characters, including the next official banner-related update and the best pages to check before deciding whether to save or pull now.",
        path="/wuthering-waves-next-character/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Next character',
        heading="Wuthering Waves Next Character",
        lead="Users searching for the next character usually want a faster answer than a full banner article. They want to know the next confirmed featured units if they exist, or whether the next official preview is still the only reliable checkpoint.",
        answer=answer,
        body=body,
        faq_items=[
            ("Who are the next Wuthering Waves featured characters?", answer),
            ("What should users check after a next-character page?", "They usually need the next-banner page, the schedule page, and character-specific pull advice before committing resources."),
        ],
    )


def render_banner_schedule_page(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    history = snapshot["history"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    table_rows = []
    for item in history:
        table_rows.append(
            f'            <tr><td>{item["version"]}</td><td>{item["phase"]}</td><td>{", ".join(item["featured_characters"])}</td><td>{fmt_human_date(item["start_date"])} to {fmt_human_date(item["end_date"])}</td></tr>'
        )
    table_rows.append(
        f'            <tr><td>{next_item["version"]}</td><td>{next_item["phase"]}</td><td>{next_character_copy(next_item)}</td><td>{phase_window_label(next_item)}</td></tr>'
    )
    answer = (
        f"As of {updated}, the current phase runs through {fmt_human_date(current['end_date'])}, and the next tracked official update is {next_item['banner_name']} on {phase_event_label(next_item)}."
        if is_preview_phase(next_item)
        else f"As of {updated}, the current phase runs through {fmt_human_date(current['end_date'])}, and the next phase begins on {fmt_human_date(next_item['start_date'])}."
    )
    body = "\n".join(
        [
            """    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves banner schedule snapshot." width="1200" height="675" decoding="async">
      </div>
      <div class="banner-art">
        <img src="/assets/img/next-banner-card.svg" alt="Next Wuthering Waves banner schedule snapshot." width="1200" height="675" decoding="async">
      </div>
    </div>""",
            render_card_grid(
                [
                    ("Current phase timing", f"{current['banner_name']} is live now, featuring {', '.join(current['featured_characters'])} through {fmt_human_date(current['end_date'])}."),
                    ("Next tracked timing", next_event_copy(next_item)),
                    ("What users usually need next", "After checking the schedule, users usually want the next-banner page, the current weapon banner, or a pull-advice page."),
                ]
            ),
            f"""    <section class="section">
      <h2>Current and recent schedule snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Version</th><th>Phase</th><th>Featured 5-stars</th><th>Dates</th></tr></thead>
          <tbody>
{chr(10).join(table_rows)}
          </tbody>
        </table>
      </div>
    </section>""",
            f"""    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
          <li><a href="/wuthering-waves-current-banner/">Current banner</a></li>
          <li><a href="/wuthering-waves-banner-countdown/">Banner countdown</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Sources</h2>
        <p>Current phase source: {current["source_url"]}</p>
        <p>Next tracked source: {next_item["source_url"]}</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Banner Schedule | WuWa Banners",
        description="Check the Wuthering Waves banner schedule, including the current phase end date, the next official banner-related update, and recent phase timing.",
        path="/wuthering-waves-banner-schedule/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Banner schedule',
        heading="Wuthering Waves Banner Schedule",
        lead="Schedule pages should make phase timing easy to scan on both mobile and desktop, not bury it under general game news.",
        answer=answer,
        body=body,
        faq_items=[
            ("What should a banner schedule page show first?", "It should show the current phase end date, the next tracked official banner-related update, and a short recent timeline."),
            ("Why does schedule information matter on a banner site?", "Schedule pages help users decide whether to pull now, save for the next phase, or wait for later banners with less guesswork."),
        ],
    )


def render_banner_order_page(snapshot: dict[str, object]) -> str:
    history = snapshot["history"]
    next_item = snapshot["next"]
    order_rows = list(history) + ([next_item] if is_preview_phase(next_item) else [])
    table_rows = []
    for index, item in enumerate(order_rows, start=1):
        focus = ", ".join(item["featured_characters"]) if item.get("featured_characters") else next_character_copy(item)
        href = "/wuthering-waves-banner-history/" if index == 1 else ("/wuthering-waves-next-banner/" if item["banner_name"] == next_item["banner_name"] else "/wuthering-waves-current-banner/")
        table_rows.append(f'            <tr><td>{index}</td><td>{item["banner_name"]}</td><td>{focus}</td><td><a href="{href}">Open page</a></td></tr>')
    recent_sequence = " then ".join(item["banner_name"] for item in order_rows)
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Recent order", f"The tracked recent sequence is {recent_sequence}."),
                    ("Why users search this", "Many users do not start with a specific date question. They start by asking what comes after what."),
                    ("Best next pages", "After this page, the most useful next steps are banner history, banner schedule, and next banner."),
                ]
            ),
            f"""    <section class="section">
      <h2>Recent tracked banner order</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Order</th><th>Phase</th><th>Tracked focus</th><th>Best next page</th></tr></thead>
          <tbody>
{chr(10).join(table_rows)}
          </tbody>
        </table>
      </div>
    </section>""",
            """    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-banner-history/">Banner history</a></li>
          <li><a href="/wuthering-waves-banner-schedule/">Banner schedule</a></li>
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why keep this separate</h2>
        <p>Banner order is simpler than a full history page. It works as a lighter entry page for users who want sequence, not a full archive.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Banner Order | WuWa Banners",
        description="Check the Wuthering Waves banner order, including recent phase flow, the current phase, and the next official banner-related update.",
        path="/wuthering-waves-banner-order/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Banner order',
        heading="Wuthering Waves Banner Order",
        lead="Banner order is broad-intent search. Users usually want a clean sequence answer first, then a way into the deeper history or schedule pages if they need more detail.",
        answer=f"The recent tracked banner order is {recent_sequence}.",
        body=body,
        faq_items=[
            ("What should a banner order page include?", "It should show recent phase order, the current live phase, the next tracked official update, and clear routes into history and schedule pages."),
            ("Why is banner order different from banner history?", "Banner order is a simpler sequence answer for broad intent, while history is the deeper reference page for timing and rerun context."),
        ],
    )


def render_next_banner_countdown_page(snapshot: dict[str, object]) -> str:
    next_item = snapshot["next"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    answer = (
        f"As of {updated}, the next tracked banner countdown points to {phase_event_label(next_item)} for {next_item['banner_name']}. The full next phase lineup is still unconfirmed."
        if is_preview_phase(next_item)
        else f"As of {updated}, the next tracked banner countdown points to {fmt_human_date(next_item['start_date'])}, when {next_item['banner_name']} is scheduled to begin."
    )
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Target date", phase_event_label(next_item)),
                    ("Why users search this", "This is a narrow timing query from users who are already close to a save-or-pull decision."),
                    ("Best next pages", "The strongest follow-ups are next banner, schedule, and timeline."),
                ]
            ),
            f"""    <section class="section">
      <h2>Next countdown snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>Date</th><th>Tracked focus</th><th>Best next page</th></tr></thead>
          <tbody>
            <tr><td>{next_item["banner_name"]}</td><td>{phase_event_label(next_item)}</td><td>{next_character_copy(next_item)}</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
            """    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-next-banner/">Next banner</a></li>
          <li><a href="/wuthering-waves-banner-schedule/">Banner schedule</a></li>
          <li><a href="/wuthering-waves-timeline/">Timeline</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why keep this page</h2>
        <p>A countdown-intent page is simpler and more focused than the full next-banner article, so it helps capture a tighter search variant.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title="Wuthering Waves Next Banner Countdown | WuWa Banners",
        description="Check the Wuthering Waves next banner countdown, including the next official banner-related date and the best follow-up timing pages.",
        path="/wuthering-waves-next-banner-countdown/",
        breadcrumbs='<a href="/">Home</a> / <a href="/banners/">Banners</a> / Next banner countdown',
        heading="Wuthering Waves Next Banner Countdown",
        lead="Countdown pages work best when they answer the date intent immediately, then move users into the full next-banner or schedule page if they need more context.",
        answer=answer,
        body=body,
        faq_items=[
            ("When is the next Wuthering Waves banner countdown pointing to?", answer),
            ("Which page should users check after the next banner countdown?", "Most users should move to the next-banner page, banner schedule page, or timeline page."),
        ],
    )


def render_characters_hub_page(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    current_rows = "\n".join(
        f'            <tr><td>Current</td><td>{name}</td><td><a href="/wuthering-waves-characters/{slugify_character(name)}/">Open {name} hub</a></td></tr>'
        for name in current["featured_characters"]
    )
    support_rows = "\n".join(
        f'            <tr><td>{name}</td><td>Current phase</td><td><a href="/wuthering-waves-characters/{slugify_character(name)}/">Open hub</a></td><td><a href="/wuthering-waves-{slugify_character(name)}-materials/">Materials</a> · <a href="/wuthering-waves-{slugify_character(name)}-build/">Build</a> · <a href="/wuthering-waves-{slugify_character(name)}-team-comps/">Team comps</a></td></tr>'
        for name in current["featured_characters"]
    )
    preview_notice = (
        f"The next full featured characters are still unconfirmed. Watch {next_item['banner_name']} on {phase_event_label(next_item)} for the next official reveal."
        if not next_item["featured_characters"]
        else f"The next tracked featured characters are {', '.join(next_item['featured_characters'])} in {next_item['banner_name']}."
    )
    faq_json = render_faq_json(
        "Wuthering Waves Characters",
        "/wuthering-waves-characters/",
        [
            ("What should a Wuthering Waves characters page show first?", "It should show current featured characters, the next tracked official character context, and the fastest routes into pull-advice pages."),
            ("Why is a characters page useful on this site?", "Because it connects banner intent, pull planning, and future character-specific support pages into one structure."),
        ],
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Wuthering Waves Characters | WuWa Banners</title>
  <meta name="description" content="Browse Wuthering Waves characters, including current banner characters, next official character context, pull planning, and the best related pages for decision support.">
  <link rel="canonical" href="https://wuwabanners.net/wuthering-waves-characters/">
  <meta property="og:title" content="Wuthering Waves Characters">
  <meta property="og:description" content="A clean Wuthering Waves characters page tied to current banner, next banner, and pull-planning pages.">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://wuwabanners.net/wuthering-waves-characters/">
  <meta property="og:image" content="https://wuwabanners.net/assets/img/og-default.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONT_PRELOAD_BLOCK}
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/">Home</a><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-characters/">Characters</a><a href="/wuthering-waves-weapons/">Weapons</a><a href="/wuthering-waves-items/">Items</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / Characters</div>
    <h1>Wuthering Waves Characters</h1>
    <p class="lead">Use the characters hub when the user wants a list first, then one character detail hub, then a deeper support page only if needed. This branch should feel like list, detail, support.</p>
    <div class="answer-box"><strong>Direct answer:</strong> As of {updated}, the current tracked featured characters are {", ".join(current["featured_characters"])} in {current["banner_name"]}. {preview_notice}</div>
    {render_card_grid([("Current featured characters", f"{', '.join(current['featured_characters'])} are the live tracked characters in {current['banner_name']}."), ("Next official character context", preview_notice), ("Why users search this", "This query often sits between broad banner discovery and character-specific pull or materials intent.")])}
    <section class="section">
      <h2>How to use the characters branch</h2>
      <div class="card-grid">
        <article class="card"><h3>1. Start from the character list</h3><p>Use this page when you know the user needs a character but not yet which deeper page.</p></article>
        <article class="card"><h3>2. Open one character hub</h3><p>Open the character detail hub first. That is the clean middle layer.</p></article>
        <article class="card"><h3>3. Open one support page</h3><p>Then move into pull advice, materials, build, or team comps only if needed.</p></article>
      </div>
    </section>
    <section class="section">
      <h2>Character branch map</h2>
      <p class="section-intro">Use this branch in three steps: start from the character hub, open a character detail page, then move into support pages only if you need deeper build or planning help.</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Layer</th><th>Best page type</th><th>What it is for</th></tr></thead>
          <tbody>
            <tr><td>Hub</td><td><a href="/wuthering-waves-characters/">Characters</a></td><td>The top-level list for current, next, and reference character browsing.</td></tr>
            <tr><td>Detail</td><td>Character detail page</td><td>The clean destination for one character image, one name, and the next useful routes.</td></tr>
            <tr><td>Support</td><td><a href="/pull-advice/">Pull advice</a> or character support pages</td><td>The narrower layer for materials, build, team comps, or pull planning.</td></tr>
          </tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <h2>Current and next character list</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Status</th><th>Characters</th><th>List action</th></tr></thead>
          <tbody>
{current_rows}
            <tr><td>Next preview</td><td>{next_character_copy(next_item)}</td><td><a href="/wuthering-waves-next-character/">Open next character page</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <h2>Character reference gallery</h2>
      <p class="section-intro">This section uses the local reference-image payload. After you run the downloader and publish the generated files, this gallery fills itself automatically.</p>
      <div class="reference-grid" data-reference-gallery="characters">
        <article class="notice reference-empty">Run <code>python3 scripts/download_wuwatracker_reference_images.py</code> to populate this gallery.</article>
      </div>
    </section>
    <section class="section">
      <h2>Character detail directory</h2>
      <p class="section-intro">Use this text directory if you want to jump straight from the character list into a detail hub without scanning the full portrait grid first.</p>
      <div class="reference-directory" data-reference-directory="characters">
        <article class="notice reference-empty">Run <code>python3 scripts/download_wuwatracker_reference_images.py</code> to populate this directory.</article>
      </div>
    </section>
    <section class="section">
      <h2>Character detail hubs</h2>
      <p class="section-intro">Each live tracked featured character gets a real detail layer. The detail hub sits between the characters list and the narrower support pages, which makes the site structure easier to scan.</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Character</th><th>Status</th><th>Detail hub</th><th>Support pages</th></tr></thead>
          <tbody>
{support_rows}
          </tbody>
        </table>
      </div>
    </section>
    <section class="section two-col">
      <div class="card">
        <h2>Best related pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-current-banner-characters/">Current banner characters</a></li>
          <li><a href="/wuthering-waves-next-character/">Next character</a></li>
          <li><a href="/pull-advice/">Pull advice</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why this page matters</h2>
        <p>This page gives you a clean top-level character node. That makes it easier to grow into materials, teams, and build-lite pages later.</p>
      </div>
    </section>
    <section class="section">
      <h2>Character branch links</h2>
      <p class="section-intro">These are the main pages users usually need before or after they open a character detail page.</p>
      <div class="reference-directory">
        <a class="directory-link" href="/pull-advice/">Pull advice hub</a>
        <a class="directory-link" href="/wuthering-waves-current-banner-characters/">Current banner characters</a>
        <a class="directory-link" href="/wuthering-waves-next-character/">Next character</a>
        <a class="directory-link" href="/wuthering-waves-current-banner/">Current banner</a>
        <a class="directory-link" href="/wuthering-waves-next-banner/">Next banner</a>
      </div>
    </section>
    <section class="section">
      <h2>FAQ</h2>
      <div class="faq-list">
{render_faq_block([("What should a Wuthering Waves characters page show first?", "It should show current featured characters, the next tracked official character context, and the fastest routes into pull-advice pages."), ("Why is a characters page useful on this site?", "Because it connects banner intent, pull planning, and future character-specific support pages into one structure.")])}
      </div>
    </section>
  </div></main>
<script defer src="/assets/js/site.js"></script>
{GTAG_SNIPPET}
</body>
</html>
"""


def get_reference_character_name_by_slug(slug: str) -> str:
    for entry in REFERENCE_PAYLOAD.get("characters", []):
        if entry.get("slug") == slug:
            return str(entry["name"])
    return slug.replace("-", " ").title()


def discover_legacy_guide_slugs(snapshot: dict[str, object]) -> list[str]:
    focus_slugs = {
        slugify_character(name)
        for name in list(snapshot["current"]["featured_characters"]) + list(snapshot["next"]["featured_characters"])
    }
    legacy_slugs: set[str] = set()

    for path in (ROOT / "wuthering-waves-characters").glob("*/index.html"):
        slug = path.parent.name
        if slug == "index" or slug in focus_slugs:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "Guide Hub" in text:
            legacy_slugs.add(slug)

    for pattern in (
        "wuthering-waves-should-you-pull-*",
        "wuthering-waves-*-materials",
        "wuthering-waves-*-build",
        "wuthering-waves-*-team-comps",
    ):
        for path in ROOT.glob(pattern):
            slug = path.name
            if slug.startswith("wuthering-waves-should-you-pull-"):
                slug = slug.removeprefix("wuthering-waves-should-you-pull-")
            else:
                for suffix in ("-materials", "-build", "-team-comps"):
                    if slug.endswith(suffix):
                        slug = slug[: -len(suffix)]
                        break
                slug = slug.removeprefix("wuthering-waves-")
            if slug and slug not in focus_slugs:
                legacy_slugs.add(slug)

    return sorted(legacy_slugs)


def render_legacy_character_page(slug: str, character: str, snapshot: dict[str, object]) -> str:
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    current = snapshot["current"]
    next_item = snapshot["next"]
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Current phase reference", f"{current['banner_name']} is the live banner, featuring {', '.join(current['featured_characters'])} through {fmt_human_date(current['end_date'])}."),
                    ("Next tracked update", next_event_copy(next_item)),
                    ("How to use this page now", f"Treat {character} as a reference or rerun-watch character until a future banner or official preview puts them back into focus."),
                ]
            ),
            f"""    <section class="section">
      <h2>{character} decision reset</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>If this is your question</th><th>Best next page</th><th>Why</th></tr></thead>
          <tbody>
            <tr><td>Should I spend right now?</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td><td>Use the live phase first, not an outdated character-specific recommendation.</td></tr>
            <tr><td>Should I keep saving?</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td><td>Compare the current live phase against the next official update before you lock a rerun plan.</td></tr>
            <tr><td>Am I mostly waiting for a rerun?</td><td><a href="/wuthering-waves-next-rerun/">Next rerun</a></td><td>This is the better route for a non-focus character that is not currently live or officially next.</td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
            f"""    <section class="section two-col">
      <div class="card">
        <h2>{character} support branch</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-should-you-pull-{slug}/">Should you pull {character}?</a></li>
          <li><a href="{support_page_path(slug, "materials")}">{character} materials</a></li>
          <li><a href="{support_page_path(slug, "build")}">{character} build</a></li>
          <li><a href="{support_page_path(slug, "team-comps")}">{character} team comps</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why this hub still exists</h2>
        <p>This page still works as a clean character branch for users who search the name directly, even when {character} is no longer in the live or next tracked focus set.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title=f"Wuthering Waves {character} Guide Hub | WuWa Banners",
        description=f"Browse the Wuthering Waves {character} guide hub with rerun-watch context, support pages, and current-versus-next banner routing.",
        path=character_overview_path(slug),
        breadcrumbs=f'<a href="/">Home</a> / <a href="/guides/">Guides</a> / <a href="/wuthering-waves-characters/">Characters</a> / {html.escape(character)}',
        heading=f"Wuthering Waves {character} Guide Hub",
        lead=f"{character} is not in the current live focus set or the next officially confirmed featured set. Use this page as a reference branch into current-banner, rerun-watch, and support-page decisions.",
        answer=f"As of {updated}, {character} is best treated as a reference or rerun-watch character rather than a live or officially next banner recommendation.",
        body=body,
        faq_items=[
            (f"What should the {character} overview page do now?", f"It should route users into current-banner, next-banner, rerun-watch, and support pages instead of pretending {character} is still a live focus character."),
            (f"Why keep a {character} hub if the character is not currently featured?", "Because users still search character names directly, and a clean hub is better than leaving an outdated phase-specific recommendation online."),
        ],
    )


def render_legacy_pull_page(slug: str, character: str, snapshot: dict[str, object]) -> str:
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    current = snapshot["current"]
    next_item = snapshot["next"]
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Current spend context", f"The live spend decision now sits in {current['banner_name']}, not in an old {character}-specific banner window."),
                    ("Next tracked update", next_event_copy(next_item)),
                    ("Best use of this page", f"Use this page as a rerun-watch or hold-for-later note for {character}, then compare against the current live banner and pity state."),
                ]
            ),
            f"""    <section class="section">
      <h2>{character} pull reset</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Situation</th><th>Safer move</th><th>Best next page</th></tr></thead>
          <tbody>
            <tr><td>You only care about spending right now</td><td>Judge the live phase first</td><td><a href="/wuthering-waves-current-banner/">Current banner</a></td></tr>
            <tr><td>You are mainly saving for future value</td><td>Compare next update and rerun timing</td><td><a href="/wuthering-waves-next-banner/">Next banner</a></td></tr>
            <tr><td>You are specifically waiting for {character}</td><td>Treat {character} as a rerun-watch target</td><td><a href="/wuthering-waves-next-rerun/">Next rerun</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title=f"Should You Pull {character} in Wuthering Waves? | WuWa Banners",
        description=f"Use this {character} page as a rerun-watch and future-pull reference while comparing current banners, next updates, and pity risk.",
        path=f"/wuthering-waves-should-you-pull-{slug}/",
        breadcrumbs=f'<a href="/">Home</a> / <a href="/pull-advice/">Pull advice</a> / {html.escape(character)}',
        heading=f"Should You Pull {character} in Wuthering Waves?",
        lead=f"{character} is not currently part of the live tracked focus set or the next officially confirmed featured lineup. This page should therefore act as a rerun-watch reference, not an outdated live-banner recommendation.",
        answer=f"As of {updated}, do not treat {character} as a current-banner recommendation. Compare the live banner, the next official update, pity state, and rerun timing first.",
        body=body,
        faq_items=[
            (f"Should you pull {character} right now?", f"Only if a future rerun plan still makes sense after you compare the live banner, next official update, and your pity state. {character} is not a current live-focus answer."),
            (f"What should you check before saving for {character}?", "Check the current banner, next banner, pity carry-over, and rerun-watch context before assuming an old character target is still your best plan."),
        ],
    )


def render_legacy_support_page(slug: str, character: str, kind: str, snapshot: dict[str, object]) -> str:
    updated = fmt_human_date(snapshot["updated"] + " 00:00")
    current = snapshot["current"]
    next_item = snapshot["next"]
    kind_label = {"materials": "Materials", "build": "Build", "team-comps": "Team Comps"}[kind]
    if kind == "materials":
        lead = f"Use this {character} materials page as a low-risk reference while the character is off the current live-banner path."
        answer = f"As of {updated}, the safe use for this page is to separate broadly reusable farming from route-locked farming until {character} re-enters a current or officially next focus window."
        focus_rows = [
            ("Reusable prep", "Shared credits, common drops, and overlap materials", "Safest while the character is off-cycle."),
            ("Route-locked prep", "Rare boss or weekly items", "Better saved until a future banner or clearer rerun target."),
            ("Best next comparison", f"{current['banner_name']} vs rerun-watch", "Compare live needs against long-term prep."),
        ]
    elif kind == "build":
        lead = f"Use this {character} build page as a reference branch instead of a live-banner lock-in."
        answer = f"As of {updated}, the safest build advice is to keep {character} on a flexible reference path until a future banner or rerun makes the investment active again."
        focus_rows = [
            ("Reference build lane", "Keep a flexible role and fallback weapon route", "Best when the character is not live or officially next."),
            ("Do not hard-lock yet", "Premium-only assumptions and narrow tuning", "Wait until future banner context returns."),
            ("Best next comparison", f"{current['banner_name']} vs rerun-watch", "Live value can still beat an old target."),
        ]
    else:
        lead = f"Use this {character} team comps page as a reference shell page while the character sits outside the live and next tracked focus set."
        answer = f"As of {updated}, the safest team-comp advice is to keep one practical shell for {character} without treating it as a live spend signal."
        focus_rows = [
            ("Reference shell", "One practical baseline team", "Keeps the page useful without pretending the character is current."),
            ("Do not over-specialize", "Narrow premium-only pairings", "Wait until future banner or rerun timing matters again."),
            ("Best next comparison", f"{current['banner_name']} vs rerun-watch", "Live roster pressure may still outweigh an old favorite."),
        ]
    rows_html = "\n".join(f"            <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in focus_rows)
    body = "\n".join(
        [
            render_card_grid(
                [
                    ("Current live context", f"{current['banner_name']} is the active banner path right now."),
                    ("Next tracked update", next_event_copy(next_item)),
                    ("Reference-only use", f"Keep {character} on a reference branch until a future banner or rerun makes the page active again."),
                ]
            ),
            f"""    <section class="section">
      <h2>{character} {kind_label.lower()} reference table</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Focus area</th><th>Best move</th><th>Why now</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>""",
            f"""    <section class="section two-col">
      <div class="card">
        <h2>Best next pages</h2>
        <ul class="list">
          <li><a href="/wuthering-waves-should-you-pull-{slug}/">Should you pull {character}?</a></li>
          <li><a href="/wuthering-waves-next-rerun/">Next rerun</a></li>
          <li><a href="/wuthering-waves-current-banner/">Current banner</a></li>
        </ul>
      </div>
      <div class="card">
        <h2>Why keep this page live</h2>
        <p>Users still search direct character support queries even when the character is off-cycle. A neutral reference page is safer than leaving an outdated live-phase version online.</p>
      </div>
    </section>""",
        ]
    )
    return render_standard_page(
        title=f"Wuthering Waves {character} {kind_label} | WuWa Banners",
        description=f"Use this {character} {kind_label.lower()} page as a neutral reference branch tied to rerun-watch, current-banner, and future update planning.",
        path=support_page_path(slug, kind),
        breadcrumbs=f'<a href="/">Home</a> / <a href="/guides/">Guides</a> / <a href="{character_overview_path(slug)}">{html.escape(character)}</a> / {kind_label}',
        heading=f"Wuthering Waves {character} {kind_label}",
        lead=lead,
        answer=answer,
        body=body,
        faq_items=[
            (f"What should a {character} {kind_label.lower()} page do when the character is off-cycle?", "It should work as a neutral reference branch, not as a live or next-phase commitment page."),
            (f"Why keep {character} {kind_label.lower()} inside the banner site structure?", "Because users still move from character-specific searches into current-banner, rerun-watch, and pity decisions even when the character is not currently featured."),
        ],
    )


def update_pages(snapshot: dict[str, object]) -> None:
    pull_pages = get_pull_pages(snapshot)
    overview_pages = get_character_overview_pages(pull_pages)
    support_pages = get_support_pages(pull_pages)
    history_pages = get_history_detail_pages(snapshot)
    legacy_slugs = discover_legacy_guide_slugs(snapshot)

    index_text = INDEX_HTML.read_text(encoding="utf-8")
    index_text = replace_block_exact(index_text, "HOME_TIMELINE", build_home_timeline(snapshot))
    index_text = replace_block_exact(index_text, "HOME_MEDIA", build_home_media(snapshot["updated"]))
    index_text = replace_block_exact(index_text, "HOME_UPDATE", build_home_update(snapshot["updated"]))
    INDEX_HTML.write_text(index_text, encoding="utf-8")

    next_text = NEXT_HTML.read_text(encoding="utf-8")
    next_text = replace_block_exact(next_text, "NEXT_INTRO", build_next_intro(snapshot))
    next_text = replace_block_exact(next_text, "NEXT_MEDIA", build_next_media(snapshot))
    next_text = replace_block_exact(next_text, "NEXT_CARDS", build_next_cards(snapshot))
    next_text = replace_block_exact(next_text, "NEXT_TABLE", build_next_table(snapshot))
    next_text = replace_block_exact(next_text, "NEXT_PULL", build_next_pull(snapshot))
    next_text = replace_block_exact(next_text, "NEXT_SOURCES", build_next_sources(snapshot))
    insert_after = """      <section class="section two-col">
        <!-- AUTO:NEXT_PULL -->"""
    if "AUTO:NEXT_COMPARE" not in next_text:
        next_text = next_text.replace(
            insert_after,
            f"""      <section class="section">
        <!-- AUTO:NEXT_COMPARE -->
{build_next_compare_matrix(snapshot)}
<!-- /AUTO:NEXT_COMPARE -->
      </section>

      <section class="section two-col">
        <!-- AUTO:NEXT_PULL -->""",
            1,
        )
    else:
        next_text = replace_block_exact(next_text, "NEXT_COMPARE", build_next_compare_matrix(snapshot))
    NEXT_HTML.write_text(next_text, encoding="utf-8")

    current_text = CURRENT_HTML.read_text(encoding="utf-8")
    current_text = replace_block_exact(current_text, "CURRENT_INTRO", build_current_intro(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_MEDIA", build_current_media(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_CARDS", build_current_cards(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_TABLE", build_current_table(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_SOURCES", build_current_sources(snapshot))
    if "AUTO:CURRENT_DECISION" not in current_text:
        current_table_end = """<!-- /AUTO:CURRENT_TABLE -->
    </section>"""
        current_text = current_text.replace(
            current_table_end,
            f"""<!-- /AUTO:CURRENT_TABLE -->
    </section>

    <section class="section">
      <!-- AUTO:CURRENT_DECISION -->
{build_current_decision_matrix(snapshot)}
<!-- /AUTO:CURRENT_DECISION -->
    </section>
    <section class="section two-col">
      <!-- AUTO:CURRENT_ROUTES -->
{build_current_account_routes(snapshot)}
<!-- /AUTO:CURRENT_ROUTES -->
    </section>
    <section class="section">
      <!-- AUTO:CURRENT_CHARACTER_LINKS -->
{build_current_character_links(snapshot)}
<!-- /AUTO:CURRENT_CHARACTER_LINKS -->
    </section>""",
            1,
        )
    else:
        current_text = replace_block_exact(current_text, "CURRENT_DECISION", build_current_decision_matrix(snapshot))
        current_text = replace_block_exact(current_text, "CURRENT_ROUTES", build_current_account_routes(snapshot))
        current_text = replace_block_exact(current_text, "CURRENT_CHARACTER_LINKS", build_current_character_links(snapshot))
    CURRENT_HTML.write_text(current_text, encoding="utf-8")

    history_text = HISTORY_HTML.read_text(encoding="utf-8")
    history_text = replace_block_exact(history_text, "HISTORY_INTRO", build_history_intro(snapshot))
    history_text = replace_block_exact(history_text, "HISTORY_MEDIA", build_history_media(snapshot))
    history_text = replace_block_exact(history_text, "HISTORY_TABLE", build_history_table(snapshot))
    history_text = replace_block_exact(history_text, "HISTORY_SOURCES", build_history_sources(snapshot))
    HISTORY_HTML.write_text(history_text, encoding="utf-8")

    rerun_text = RERUN_HTML.read_text(encoding="utf-8")
    rerun_text = replace_block_exact(rerun_text, "RERUN_INTRO", build_rerun_intro(snapshot))
    rerun_text = replace_block_exact(rerun_text, "RERUN_MEDIA", build_rerun_media())
    rerun_text = replace_block_exact(rerun_text, "RERUN_CARDS", build_rerun_cards(snapshot))
    rerun_text = replace_block_exact(rerun_text, "RERUN_TABLE", build_rerun_table(snapshot))
    rerun_text = replace_block_exact(rerun_text, "RERUN_SOURCES", build_rerun_sources(snapshot))
    RERUN_HTML.write_text(rerun_text, encoding="utf-8")

    countdown_text = COUNTDOWN_HTML.read_text(encoding="utf-8")
    countdown_text = replace_block_exact(countdown_text, "COUNTDOWN_INTRO", build_countdown_intro(snapshot))
    countdown_text = replace_block_exact(countdown_text, "COUNTDOWN_MEDIA", build_countdown_media(snapshot))
    countdown_text = replace_block_exact(countdown_text, "COUNTDOWN_CARDS", build_countdown_cards(snapshot))
    countdown_text = replace_block_exact(countdown_text, "COUNTDOWN_TABLE", build_countdown_table(snapshot))
    countdown_text = replace_block_exact(countdown_text, "COUNTDOWN_SOURCES", build_countdown_sources(snapshot))
    COUNTDOWN_HTML.write_text(countdown_text, encoding="utf-8")
    NEXT_COUNTDOWN_HTML.write_text(render_next_banner_countdown_page(snapshot), encoding="utf-8")
    NEXT_DATE_HTML.write_text(render_next_banner_date_page(snapshot), encoding="utf-8")
    CURRENT_END_HTML.write_text(render_current_banner_end_date_page(snapshot), encoding="utf-8")
    CURRENT_CHARACTERS_HTML.write_text(render_current_banner_characters_page(snapshot), encoding="utf-8")
    NEXT_CHARACTER_HTML.write_text(render_next_character_page(snapshot), encoding="utf-8")
    SCHEDULE_HTML.write_text(render_banner_schedule_page(snapshot), encoding="utf-8")
    ORDER_HTML.write_text(render_banner_order_page(snapshot), encoding="utf-8")
    CHARACTERS_HUB_HTML.write_text(render_characters_hub_page(snapshot), encoding="utf-8")

    pull_text = PULL_HUB_HTML.read_text(encoding="utf-8")
    pull_text = replace_block_exact(pull_text, "PULL_INTRO", build_pull_intro(snapshot, pull_pages))
    pull_text = replace_block_exact(pull_text, "PULL_GRID", build_pull_grid(snapshot))
    pull_text = replace_block_exact(pull_text, "PULL_LINKS", build_pull_links(pull_pages))
    pull_links_end = """<!-- /AUTO:PULL_LINKS -->
    </section>"""
    if "AUTO:PULL_ROUTES" not in pull_text:
        pull_text = pull_text.replace(
            pull_links_end,
            """<!-- /AUTO:PULL_LINKS -->
    </section>
    <section class="section">
      <!-- AUTO:PULL_ROUTES -->
PLACEHOLDER_PULL_ROUTES
<!-- /AUTO:PULL_ROUTES -->
    </section>
    <section class="section two-col">
      <!-- AUTO:PULL_COMPARE -->
PLACEHOLDER_PULL_COMPARE
<!-- /AUTO:PULL_COMPARE -->
    </section>""",
            1,
        )
        pull_text = pull_text.replace("PLACEHOLDER_PULL_ROUTES", build_pull_decision_routes(snapshot), 1)
        pull_text = pull_text.replace("PLACEHOLDER_PULL_COMPARE", build_pull_compare_cards(snapshot), 1)
    else:
        pull_text = replace_block_exact(pull_text, "PULL_ROUTES", build_pull_decision_routes(snapshot))
        pull_text = replace_block_exact(pull_text, "PULL_COMPARE", build_pull_compare_cards(snapshot))
    PULL_HUB_HTML.write_text(pull_text, encoding="utf-8")

    character_urls = []
    for page in pull_pages:
        page_dir = ROOT / f"wuthering-waves-should-you-pull-{page['slug']}"
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(render_character_page(page, snapshot), encoding="utf-8")
        character_urls.append(f"https://wuwabanners.net/wuthering-waves-should-you-pull-{page['slug']}/")

    overview_urls = []
    for page in overview_pages:
        page_dir = ROOT / page["path"].strip("/")
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(render_character_overview_page(page, snapshot), encoding="utf-8")
        overview_urls.append(f"https://wuwabanners.net{page['path']}")

    support_urls = []
    for page in support_pages:
        page_dir = ROOT / page["path"].strip("/")
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(render_support_page(page, snapshot), encoding="utf-8")
        support_urls.append(f"https://wuwabanners.net{page['path']}")

    legacy_urls = []
    for slug in legacy_slugs:
        name = get_reference_character_name_by_slug(slug)

        overview_dir = ROOT / character_overview_path(slug).strip("/")
        overview_dir.mkdir(parents=True, exist_ok=True)
        (overview_dir / "index.html").write_text(render_legacy_character_page(slug, name, snapshot), encoding="utf-8")
        legacy_urls.append(f"https://wuwabanners.net{character_overview_path(slug)}")

        pull_dir = ROOT / f"wuthering-waves-should-you-pull-{slug}"
        pull_dir.mkdir(parents=True, exist_ok=True)
        (pull_dir / "index.html").write_text(render_legacy_pull_page(slug, name, snapshot), encoding="utf-8")
        legacy_urls.append(f"https://wuwabanners.net/wuthering-waves-should-you-pull-{slug}/")

        for kind in ("materials", "build", "team-comps"):
            support_dir = ROOT / support_page_path(slug, kind).strip("/")
            support_dir.mkdir(parents=True, exist_ok=True)
            (support_dir / "index.html").write_text(render_legacy_support_page(slug, name, kind, snapshot), encoding="utf-8")
            legacy_urls.append(f"https://wuwabanners.net{support_page_path(slug, kind)}")

    history_urls = []
    for page in history_pages:
        page_dir = ROOT / page["path"].strip("/")
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(render_history_detail_page(page, snapshot), encoding="utf-8")
        history_urls.append(f"https://wuwabanners.net{page['path']}")

    reference_urls = discover_reference_urls()
    SITEMAP_XML.write_text(render_sitemap(character_urls + overview_urls + support_urls + legacy_urls + history_urls + reference_urls), encoding="utf-8")

    banners_hub = BANNERS_HUB_HTML.read_text(encoding="utf-8")
    if "/wuthering-waves-banner-countdown/" not in banners_hub:
        raise RuntimeError("Expected banner countdown link in banners hub")

    guides_hub = GUIDES_HUB_HTML.read_text(encoding="utf-8")
    if "/pull-advice/" not in guides_hub:
        raise RuntimeError("Expected pull-advice link in guides hub")


def main() -> int:
    rows = load_rows()
    snapshot = build_snapshot(rows)
    write_json(snapshot)
    write_cards(snapshot)
    update_pages(snapshot)
    print(f"Wrote {DATA_JSON}")
    print(f"Updated SVG cards in {IMG_DIR}")
    print("Updated dynamic page blocks and character pages from CSV")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
