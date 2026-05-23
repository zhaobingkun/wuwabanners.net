from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_JSON = ROOT / "data" / "banner-snapshot.json"
REFERENCE_JSON = ROOT / "data" / "reference-images.json"
SITEMAP_XML = ROOT / "sitemap.xml"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_file(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"Missing required file: {path.relative_to(ROOT)}")


def require_text(path: Path, needles: list[str], failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"Missing page for text check: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            failures.append(f"{path.relative_to(ROOT)} is missing expected text: {needle}")


def require_sitemap_urls(urls: list[str], failures: list[str]) -> None:
    if not SITEMAP_XML.exists():
        failures.append("Missing sitemap.xml")
        return
    text = SITEMAP_XML.read_text(encoding="utf-8")
    for url in urls:
        if url not in text:
            failures.append(f"sitemap.xml is missing URL: {url}")


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    require_file(SNAPSHOT_JSON, failures)
    require_file(REFERENCE_JSON, failures)
    require_file(SITEMAP_XML, failures)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    snapshot = load_json(SNAPSHOT_JSON)
    references = load_json(REFERENCE_JSON)

    current = snapshot["current"]
    nxt = snapshot["next"]
    history = snapshot.get("history", [])

    home = ROOT / "index.html"
    next_page = ROOT / "wuthering-waves-next-banner" / "index.html"
    current_page = ROOT / "wuthering-waves-current-banner" / "index.html"
    history_page = ROOT / "wuthering-waves-banner-history" / "index.html"
    pull_page = ROOT / "pull-advice" / "index.html"
    banners_hub = ROOT / "banners" / "index.html"
    guides_hub = ROOT / "guides" / "index.html"
    characters_hub = ROOT / "wuthering-waves-characters" / "index.html"
    weapons_hub = ROOT / "wuthering-waves-weapons" / "index.html"
    items_hub = ROOT / "wuthering-waves-items" / "index.html"

    require_text(
        home,
        [
            "Current timeline snapshot",
            current["banner_name"],
            nxt["banner_name"],
            "Best starting points",
            "Choose your next page by question type",
        ],
        failures,
    )
    require_text(
        next_page,
        [
            current["banner_name"],
            nxt["banner_name"],
            "Current and next banner snapshot",
            "Should you pull now or wait?",
        ],
        failures,
    )
    require_text(
        current_page,
        [
            current["banner_name"],
            current["featured_characters"][0],
            "Current banner",
        ],
        failures,
    )
    require_text(
        history_page,
        [
            "Recent banner history list",
            history[0]["banner_name"] if history else "Version",
            current["banner_name"],
            nxt["banner_name"],
        ],
        failures,
    )
    require_text(
        pull_page,
        [
            "Current phase pull pages",
            "Next phase pull pages",
            current["featured_characters"][0],
            nxt["featured_characters"][0],
        ],
        failures,
    )
    require_text(
        banners_hub,
        ["How to use the banners branch", "Banner directory", "Timing cluster"],
        failures,
    )
    require_text(
        guides_hub,
        ["How to use the guides branch", "Guide directory", "Support page directory"],
        failures,
    )
    require_text(
        characters_hub,
        ["How to use the characters branch", "branch map", "branch links"],
        failures,
    )
    require_text(
        weapons_hub,
        ["How to use the weapons branch", "branch map", "branch links"],
        failures,
    )
    require_text(
        items_hub,
        ["How to use the items branch", "branch map", "branch links"],
        failures,
    )

    # Ensure focus character hubs and support pages exist.
    focus_names = current["featured_characters"] + nxt["featured_characters"]
    for name in focus_names:
        slug = slugify(name)
        hub = ROOT / "wuthering-waves-characters" / slug / "index.html"
        materials = ROOT / f"wuthering-waves-{slug}-materials" / "index.html"
        build = ROOT / f"wuthering-waves-{slug}-build" / "index.html"
        teams = ROOT / f"wuthering-waves-{slug}-team-comps" / "index.html"
        should_pull = ROOT / f"wuthering-waves-should-you-pull-{slug}" / "index.html"
        for path in [hub, materials, build, teams, should_pull]:
            require_file(path, failures)

    # Ensure reference branches have real data.
    for branch in ("characters", "weapons", "items"):
        entries = references.get(branch, [])
        if not entries:
            failures.append(f"reference-images.json has no entries for {branch}")
        else:
            first_entry = entries[0]
            entry_page = ROOT / f"wuthering-waves-{branch}" / first_entry["slug"] / "index.html"
            require_file(entry_page, failures)

    key_urls = [
        "https://wuwabanners.net/",
        "https://wuwabanners.net/banners/",
        "https://wuwabanners.net/guides/",
        "https://wuwabanners.net/wuthering-waves-next-banner/",
        "https://wuwabanners.net/wuthering-waves-current-banner/",
        "https://wuwabanners.net/wuthering-waves-banner-history/",
        "https://wuwabanners.net/pull-advice/",
        "https://wuwabanners.net/wuthering-waves-characters/",
        "https://wuwabanners.net/wuthering-waves-weapons/",
        "https://wuwabanners.net/wuthering-waves-items/",
    ]
    require_sitemap_urls(key_urls, failures)

    # Warnings only: note secondary sources that should be replaced later.
    trusted_domains = (
        "wutheringwaves.kurogames.com",
        "youtube.com",
        "blog.playstation.com",
        "dearplayers.com",
    )
    for row in history:
        source_url = row.get("source_url", "")
        if source_url and not any(domain in source_url for domain in trusted_domains):
            warnings.append(
                f"History row {row['banner_name']} still uses a secondary source: {source_url}"
            )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        for warning in warnings:
            print(f"WARN: {warning}")
        return 1

    print("PASS: core files, hubs, focus character pages, and sitemap entries are present.")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
