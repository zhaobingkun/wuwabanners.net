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
IMG_DIR = ROOT / "assets" / "img"
INDEX_HTML = ROOT / "index.html"
NEXT_HTML = ROOT / "wuthering-waves-next-banner" / "index.html"
CURRENT_HTML = ROOT / "wuthering-waves-current-banner" / "index.html"
HISTORY_HTML = ROOT / "wuthering-waves-banner-history" / "index.html"
RERUN_HTML = ROOT / "wuthering-waves-next-rerun" / "index.html"
COUNTDOWN_HTML = ROOT / "wuthering-waves-banner-countdown" / "index.html"
PULL_HUB_HTML = ROOT / "pull-advice" / "index.html"
SITEMAP_XML = ROOT / "sitemap.xml"
BANNERS_HUB_HTML = ROOT / "banners" / "index.html"
GUIDES_HUB_HTML = ROOT / "guides" / "index.html"

GTAG_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-C73K15FD00"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-C73K15FD00');
</script>"""

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
    "https://wuwabanners.net/pull-advice/",
]


def load_rows() -> list[dict[str, str]]:
    with DATA_CSV.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def split_field(value: str) -> list[str]:
    return [part.strip() for part in value.split("|") if part.strip()]


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


def pick_current_and_next(rows: list[dict[str, str]], updated: date) -> tuple[dict[str, str], dict[str, str], list[dict[str, str]]]:
    char_rows = [
        row
        for row in rows
        if row["banner_type"] == "character" and row["start_date"] and row["end_date"] and row["status"] in {"official", "expected"}
    ]
    char_rows.sort(key=lambda row: parse_date(row["start_date"]) or date.max)
    if not char_rows:
        raise RuntimeError("No character banner rows with dates found in banner-data.csv")

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
    next_row = char_rows[current_index + 1] if current_index + 1 < len(char_rows) else current_row
    history_rows = char_rows[max(0, current_index - 1) : min(len(char_rows), current_index + 2)]
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
            "banner_name": current_char["banner_name"],
            "featured_characters": split_field(current_char["featured_characters"]),
            "featured_weapons": split_field(current_weapon["featured_weapons"]) if current_weapon else [],
            "start_date": current_char["start_date"],
            "end_date": current_char["end_date"],
            "source_url": current_char["source_url"],
        },
        "next": {
            "version": next_char["version"],
            "phase": next_char["phase"],
            "banner_name": next_char["banner_name"],
            "featured_characters": split_field(next_char["featured_characters"]),
            "featured_weapons": split_field(next_weapon["featured_weapons"]) if next_weapon else [],
            "start_date": next_char["start_date"],
            "end_date": next_char["end_date"],
            "source_url": next_char["source_url"],
        },
        "history": [
            {
                "version": row["version"],
                "phase": row["phase"],
                "banner_name": row["banner_name"],
                "featured_characters": split_field(row["featured_characters"]),
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
            ", ".join(next_item["featured_characters"]),
            "Weapons: " + ", ".join(next_item["featured_weapons"]),
            "Starts " + fmt_human_date(next_item["start_date"]),
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
          <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves banner snapshot generated from the latest CSV build.">
        </div>
        <div class="video-card">
          <h2>Official preview video slot</h2>
          <p class="section-intro">Use one official broadcast or trailer on the homepage. This keeps the front page visually stronger without turning the site into a video-first layout.</p>
          <div class="video-embed">
            <iframe src="https://www.youtube.com/embed/viOkAhoa0k8" title="Wuthering Waves Version 3.3 Preview Special Broadcast" loading="lazy" allowfullscreen></iframe>
          </div>
        </div>
      </div>"""


def build_home_update(updated: str) -> str:
    return f'        <p class="update-stamp">Snapshot updated for {fmt_human_date(updated + " 00:00")}. Current and next banner values should be rechecked against official notices and in-game Convene at every phase change.</p>'


def build_next_intro(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    updated = snapshot["updated"]
    return f"""      <p class="lead">As of {fmt_human_date(updated + " 00:00")}, the active Wuthering Waves banners are in {current["banner_name"]}, while the next banner rotation is {next_item["banner_name"]} scheduled to begin on {fmt_human_date(next_item["start_date"])}. This page combines a live-style snapshot with the structure needed for long-term updates: current banner, next banner, countdown logic, and pull-or-save context.</p>
      <div class="answer-box"><strong>Direct answer:</strong> The current {current["banner_name"]} banners feature {", ".join(current["featured_characters"])} through {fmt_human_date(current["end_date"])}. The next {next_item["banner_name"]} banners are {", ".join(next_item["featured_characters"])}, with the next phase expected to begin on {fmt_human_date(next_item["start_date"])}.</div>
      <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_next_media(snapshot: dict[str, object]) -> str:
    next_item = snapshot["next"]
    return f"""      <div class="media-grid" style="margin-top:1.25rem;">
        <div class="banner-art">
          <img src="/assets/img/next-banner-card.svg" alt="Next Wuthering Waves banner snapshot for {next_item["banner_name"]}.">
        </div>
        <div class="video-card">
          <h2>Official preview media</h2>
          <p class="muted">Keep one official preview video on the page and let the text carry the primary answer.</p>
          <div class="video-embed">
            <iframe src="https://www.youtube.com/embed/viOkAhoa0k8" title="Wuthering Waves Version 3.3 Preview Special Broadcast" loading="lazy" allowfullscreen></iframe>
          </div>
        </div>
      </div>"""


def build_next_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""      <div class="card-grid">
        <article class="card"><h2>Current live phase</h2><p>{current["banner_name"]} is live right now. The featured five-stars are {", ".join(current["featured_characters"])}, and the weapon focus is {", ".join(current["featured_weapons"])}.</p></article>
        <article class="card"><h2>Next phase snapshot</h2><p>The next phase is {next_item["banner_name"]}. The featured five-stars are {", ".join(next_item["featured_characters"])}, and the weapon focus is {", ".join(next_item["featured_weapons"])}.</p></article>
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
              <tr><td>Next</td><td>{next_item["banner_name"]}</td><td>{", ".join(next_item["featured_characters"])}</td><td>{", ".join(next_item["featured_weapons"])}</td><td>Starts {fmt_human_date(next_item["start_date"])}</td></tr>
            </tbody>
          </table>
        </div>"""


def build_next_pull(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""        <div class="card">
          <h2>Should you pull now or wait?</h2>
          <p>For a new or lightly built account, the key question is whether {", ".join(current["featured_characters"])} fills an urgent team hole before {current["banner_name"]} ends. For users already saving for {next_item["featured_characters"][0]} or a later rerun, the page should say that clearly instead of forcing them to infer it from the table.</p>
          <ul class="list">
            <li><strong>Pull now:</strong> if the current phase solves an immediate roster need.</li>
            <li><strong>Consider waiting:</strong> if {", ".join(next_item["featured_characters"])} better matches your roster direction.</li>
            <li><strong>Save harder:</strong> if your main goal is a future rerun or a later patch target.</li>
          </ul>
        </div>
        <div class="card">
          <h2>Weapon banner snapshot</h2>
          <p>The current weapon focus is {", ".join(current["featured_weapons"])} through {fmt_human_date(current["end_date"])}. The next weapon group is {", ".join(next_item["featured_weapons"])} in the next phase.</p>
          <p><a href="/wuthering-waves-pity-system/">Check pity carry-over before spending more tides</a></p>
        </div>"""


def build_next_sources(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""        <div class="sources">
          <strong>Sources used for this {fmt_human_date(updated + " 00:00")} snapshot</strong><br>
          Current phase source: {current["source_url"]}<br>
          Next phase source: {next_item["source_url"]}<br>
          Official Version 3.3 preview broadcast: https://youtube.com/live/viOkAhoa0k8
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
        <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves banner snapshot for {current["banner_name"]}.">
      </div>
      <div class="video-card">
        <h2>Official preview media slot</h2>
        <p class="muted">Use the preview broadcast or official trailer to support the page visually, but keep the live answer in text above it.</p>
        <div class="video-embed">
          <iframe src="https://www.youtube.com/embed/viOkAhoa0k8" title="Wuthering Waves Version 3.3 Preview Special Broadcast" loading="lazy" allowfullscreen></iframe>
        </div>
      </div>
    </div>"""


def build_current_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    return f"""    <div class="card-grid">
      <article class="card"><h2>Live status matters more than speculation</h2><p>Users on the current banner page care more about what is active now than what might happen later. That means the live box, dates, and role summary should stay at the top.</p></article>
      <article class="card"><h2>Current phase snapshot</h2><p>The featured five-star lineup is {", ".join(current["featured_characters"])}. The companion weapon focus is {", ".join(current["featured_weapons"])} through {fmt_human_date(current["end_date"])}.</p></article>
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


def build_current_sources(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = snapshot["updated"]
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} snapshot</strong><br>
        Current phase source: {current["source_url"]}<br>
        Official Version 3.3 preview broadcast: https://youtube.com/live/viOkAhoa0k8
      </div>"""


def build_history_intro(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    return f"""    <p class="lead">A banner history page is more than an archive. It gives users a way to compare version pacing, judge rerun timing, and decide whether waiting is realistic or too costly for their account goals. This timeline snapshot is generated from the site CSV so phase updates stay consistent.</p>
    <div class="answer-box"><strong>Direct answer:</strong> The best Wuthering Waves banner history page shows version, phase, featured characters, featured weapons, and dates in a table that makes rerun patterns easy to scan.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_history_media(snapshot: dict[str, object]) -> str:
    return """    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/banner-history-card.svg" alt="Wuthering Waves banner history snapshot generated from the latest CSV build.">
      </div>
      <div class="card">
        <h2>Why this page benefits from an image</h2>
        <p>History pages often look too dense. A single visual summary makes the section less intimidating while the table still carries the real SEO value.</p>
        <p><a href="/wuthering-waves-next-banner/">Compare history against the next banner page</a></p>
      </div>
    </div>"""


def build_history_table(snapshot: dict[str, object]) -> str:
    rows = []
    for item in snapshot["history"]:
        rows.append(
            f'            <tr><td>{item["version"]}</td><td>{item["phase"]}</td><td>{", ".join(item["featured_characters"])}</td><td>{fmt_human_date(item["start_date"])} to {fmt_human_date(item["end_date"])}</td></tr>'
        )
    rows_html = "\n".join(rows)
    return f"""      <h2>Recent banner timeline snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Version</th><th>Phase</th><th>Featured 5-stars</th><th>Dates</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>"""


def build_history_sources(snapshot: dict[str, object]) -> str:
    updated = snapshot["updated"]
    urls = [item["source_url"] for item in snapshot["history"]]
    lines = "<br>\n".join([f"        Timeline source: {url}" for url in urls])
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} history snapshot</strong><br>
{lines}<br>
        Official Version 3.3 preview broadcast: https://youtube.com/live/viOkAhoa0k8
      </div>"""


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
        <img src="/assets/img/banner-history-card.svg" alt="Wuthering Waves rerun watch image based on recent banner history.">
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
    return f"""    <p class="lead">Countdown intent is mostly practical. Users want the current phase end date and the next phase start date without needing to decode a long article first.</p>
    <div class="answer-box"><strong>Direct answer:</strong> {current["banner_name"]} ends on {fmt_human_date(current["end_date"])}, and {next_item["banner_name"]} begins on {fmt_human_date(next_item["start_date"])}.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_countdown_media(snapshot: dict[str, object]) -> str:
    return """    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/current-banner-card.svg" alt="Current Wuthering Waves countdown context card.">
      </div>
      <div class="banner-art">
        <img src="/assets/img/next-banner-card.svg" alt="Next Wuthering Waves countdown context card.">
      </div>
    </div>"""


def build_countdown_cards(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""    <div class="card-grid">
      <article class="card"><h2>Current phase end</h2><p>{current["banner_name"]} is scheduled to end on {fmt_human_date(current["end_date"])}.</p></article>
      <article class="card"><h2>Next phase start</h2><p>{next_item["banner_name"]} is scheduled to start on {fmt_human_date(next_item["start_date"])}.</p></article>
      <article class="card"><h2>Why clarity matters</h2><p>Users often search countdown pages from mobile. Put the dates in plain text first, then support them with tables and related links.</p></article>
    </div>"""


def build_countdown_table(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""      <h2>Banner timing snapshot</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Phase</th><th>Event</th><th>Date</th></tr></thead>
          <tbody>
            <tr><td>{current["banner_name"]}</td><td>Current phase ends</td><td>{fmt_human_date(current["end_date"])}</td></tr>
            <tr><td>{next_item["banner_name"]}</td><td>Next phase starts</td><td>{fmt_human_date(next_item["start_date"])}</td></tr>
          </tbody>
        </table>
      </div>"""


def build_countdown_sources(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    updated = snapshot["updated"]
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} countdown snapshot</strong><br>
        Current phase source: {current["source_url"]}<br>
        Official Version 3.3 preview broadcast: https://youtube.com/live/viOkAhoa0k8
      </div>"""


def get_pull_pages(snapshot: dict[str, object]) -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for mode, key, card_name in (("current", "current", "current-banner-card.svg"), ("next", "next", "next-banner-card.svg")):
        phase = snapshot[key]
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
                    "card_name": card_name,
                }
            )
    return pages


def build_pull_intro(snapshot: dict[str, object], pull_pages: list[dict[str, str]]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    updated = snapshot["updated"]
    return f"""    <p class="lead">This hub is where banner facts turn into player decisions. Right now the tracked pull set covers {len(pull_pages)} featured characters across the live {current["banner_name"]} phase and the upcoming {next_item["banner_name"]} phase.</p>
    <div class="answer-box"><strong>Direct answer:</strong> Start with a current-phase page if you are deciding whether to spend now. Start with a next-phase page if you are deciding whether to save.</div>
    <p class="update-stamp">Last updated: {fmt_human_date(updated + " 00:00")}.</p>"""


def build_pull_grid(snapshot: dict[str, object]) -> str:
    current = snapshot["current"]
    next_item = snapshot["next"]
    return f"""    <div class="card-grid">
      <article class="card"><h2>Account-need framing</h2><p>Good pull advice starts with user context: missing DPS, missing sustain, saving for a rerun, or targeting a specific team role.</p></article>
      <article class="card"><h2>Current phase pool</h2><p>The live phase pages cover {", ".join(current["featured_characters"])} and should answer whether spending now is worth the pity and Astrite cost.</p></article>
      <article class="card"><h2>Next phase pool</h2><p>The next phase pages cover {", ".join(next_item["featured_characters"])} and should answer whether saving beats the current live banner.</p></article>
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
    return f"""      <h2>Current phase pull pages</h2>
      <div class="card-grid">
{chr(10).join(current_cards)}
      </div>
      <h2 style="margin-top:1.5rem;">Next phase pull pages</h2>
      <div class="card-grid">
{chr(10).join(next_cards)}
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
    return f"""    <div class="media-grid" style="margin-top:1.25rem;">
      <div class="banner-art">
        <img src="/assets/img/{page["card_name"]}" alt="Pull advice card for {page["character"]}.">
      </div>
      <div class="video-card">
        <h2>Phase reference video</h2>
        <div class="video-embed">
          <iframe src="https://www.youtube.com/embed/viOkAhoa0k8" title="Wuthering Waves Version 3.3 Preview Special Broadcast" loading="lazy" allowfullscreen></iframe>
        </div>
      </div>
    </div>"""


def build_character_blocks(page: dict[str, str], snapshot: dict[str, object]) -> str:
    character = page["character"]
    if page["mode"] == "current":
        next_names = ", ".join(snapshot["next"]["featured_characters"])
        return f"""    <div class="card-grid">
      <article class="card"><h2>Best for who</h2><p>Best for accounts that want to invest in the current live phase instead of waiting for the next banner rotation.</p></article>
      <article class="card"><h2>Reasons to pull</h2><p>Pull when {character} is the clearest answer to your current roster gap and you are not preserving pity for the next phase lineup: {next_names}.</p></article>
      <article class="card"><h2>Reasons to skip</h2><p>Skip if you are already aiming at the next phase or holding resources for a rerun target that matters more.</p></article>
    </div>"""
    current_names = ", ".join(snapshot["current"]["featured_characters"])
    return f"""    <div class="card-grid">
      <article class="card"><h2>Best for who</h2><p>Best for accounts planning around the next phase rather than using resources immediately in the current rotation.</p></article>
      <article class="card"><h2>Reasons to save</h2><p>Save for {character} if your pity position and account plan already point toward the next phase instead of the current lineup: {current_names}.</p></article>
      <article class="card"><h2>Reasons to wait longer</h2><p>Wait even beyond {character} if your real target is a rerun unit and the next phase still does not match your account needs.</p></article>
    </div>"""


def build_character_faq(page: dict[str, str]) -> str:
    if page["mode"] == "current":
        return """      <div class="faq-list">
        <article class="faq-item"><h3>Should you pull this current featured character now?</h3><p>Pull only if the live phase matches your roster needs better than saving for the next banner or your rerun watchlist.</p></article>
        <article class="faq-item"><h3>What should you check before pulling?</h3><p>Check your pity state, the current banner end date, and whether your next target is close enough to justify saving.</p></article>
      </div>"""
    return """      <div class="faq-list">
        <article class="faq-item"><h3>Should you save for this next featured character?</h3><p>Save when the upcoming phase fits your planned roster better than the current one and your pity state supports waiting.</p></article>
        <article class="faq-item"><h3>What should you compare before deciding?</h3><p>Compare the current banner end date, your pity progress, your rerun watchlist, and whether the upcoming phase solves a bigger problem for your account.</p></article>
      </div>"""


def build_character_sources(page: dict[str, str], updated: str) -> str:
    return f"""      <div class="sources">
        <strong>Sources used for this {fmt_human_date(updated + " 00:00")} pull snapshot</strong><br>
        Character phase source: {page["source_url"]}<br>
        Official Version 3.3 preview broadcast: https://youtube.com/live/viOkAhoa0k8
      </div>"""


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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{faq_json}
  </script>
</head>
<body>
  <header class="site-header"><div class="container nav"><a class="brand" href="/index.html"><span class="brand-mark">WB</span><span><strong>WuWa Banners</strong><small>Wuthering Waves banner tracker and guide hub</small></span></a><nav class="nav-links"><a href="/banners/">Banners</a><a href="/guides/">Guides</a><a href="/wuthering-waves-banner-history/">History</a><a href="/wuthering-waves-pity-system/">Pity</a></nav></div></header>
  <main class="section"><div class="container">
    <div class="breadcrumbs"><a href="/index.html">Home</a> / <a href="/pull-advice/">Pull advice</a> / {character}</div>
    <h1>Should You Pull {character} in Wuthering Waves?</h1>
{build_character_intro(page, snapshot)}
{build_character_media(page)}
{build_character_blocks(page, snapshot)}
    <section class="section">
      <h2>FAQ</h2>
{build_character_faq(page)}
{build_character_sources(page, snapshot["updated"])}
    </section>
  </div></main>
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


def update_pages(snapshot: dict[str, object]) -> None:
    pull_pages = get_pull_pages(snapshot)

    index_text = INDEX_HTML.read_text(encoding="utf-8")
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
    NEXT_HTML.write_text(next_text, encoding="utf-8")

    current_text = CURRENT_HTML.read_text(encoding="utf-8")
    current_text = replace_block_exact(current_text, "CURRENT_INTRO", build_current_intro(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_MEDIA", build_current_media(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_CARDS", build_current_cards(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_TABLE", build_current_table(snapshot))
    current_text = replace_block_exact(current_text, "CURRENT_SOURCES", build_current_sources(snapshot))
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

    pull_text = PULL_HUB_HTML.read_text(encoding="utf-8")
    pull_text = replace_block_exact(pull_text, "PULL_INTRO", build_pull_intro(snapshot, pull_pages))
    pull_text = replace_block_exact(pull_text, "PULL_GRID", build_pull_grid(snapshot))
    pull_text = replace_block_exact(pull_text, "PULL_LINKS", build_pull_links(pull_pages))
    PULL_HUB_HTML.write_text(pull_text, encoding="utf-8")

    character_urls = []
    for page in pull_pages:
        page_dir = ROOT / f"wuthering-waves-should-you-pull-{page['slug']}"
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(render_character_page(page, snapshot), encoding="utf-8")
        character_urls.append(f"https://wuwabanners.net/wuthering-waves-should-you-pull-{page['slug']}/")

    SITEMAP_XML.write_text(render_sitemap(character_urls), encoding="utf-8")

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
