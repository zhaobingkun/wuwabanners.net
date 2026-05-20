#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import ssl
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_JSON = ROOT / "data" / "reference-images.json"
CHAR_DIR = ROOT / "assets" / "img" / "reference" / "characters"
WEAPON_DIR = ROOT / "assets" / "img" / "reference" / "weapons"

PAGES = {
    "characters": "https://wuwatracker.com/characters",
    "weapons": "https://wuwatracker.com/weapons",
}

BASE_URL = "https://wuwatracker.com"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0 Safari/537.36"


def fetch_text(url: str) -> str:
    try:
        result = subprocess.run(
            ["curl", "-L", "--compressed", "-A", USER_AGENT, url],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        context = ssl.create_default_context()
        with urllib.request.urlopen(request, context=context, timeout=30) as response:
            return response.read().decode("utf-8", errors="ignore")


def download_file(url: str, target: Path) -> None:
    try:
        subprocess.run(
            ["curl", "-L", "--compressed", "-A", USER_AGENT, "-o", str(target), url],
            check=True,
            capture_output=True,
            text=True,
        )
        return
    except (FileNotFoundError, subprocess.CalledProcessError):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        context = ssl.create_default_context()
        with urllib.request.urlopen(request, context=context, timeout=30) as response:
            target.write_bytes(response.read())


def unique_by_slug(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    picked: list[dict[str, str]] = []
    for entry in entries:
        slug = entry["slug"]
        if slug in seen:
            continue
        seen.add(slug)
        picked.append(entry)
    return picked


def decode_next_payload(html: str) -> str:
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S)
    if not chunks:
        return html

    decoded: list[str] = []
    for chunk in chunks:
        try:
            decoded.append(bytes(chunk, "utf-8").decode("unicode_escape"))
        except UnicodeDecodeError:
            decoded.append(chunk.replace('\\"', '"'))
    return "\n".join(decoded)


def extract_asset_url(block: str, preferred_prefix: str, fallback_prefix: str) -> tuple[str | None, str]:
    preferred = re.search(rf'"portraitSrc":\{{.*?"url":"(?P<url>{re.escape(preferred_prefix)}[^"]+)"', block, re.S)
    if preferred:
        return preferred.group("url"), "Portrait"

    fallback = re.search(rf'"iconSrc":\{{.*?"url":"(?P<url>{re.escape(fallback_prefix)}[^"]+)"', block, re.S)
    if fallback:
        return fallback.group("url"), "Icon"

    return None, ""


def parse_characters(html: str) -> list[dict[str, str]]:
    text = decode_next_payload(html)
    pattern = re.compile(r'"name":"(?P<name>[^"]+)","slug":"(?P<slug>[^"]+)".{0,1600}', re.S)
    entries: list[dict[str, str]] = []
    for match in pattern.finditer(text):
        block = match.group(0)
        url, label = extract_asset_url(block, "/api/character-portraits/file/", "/api/character-icons/file/")
        if not url:
            continue
        ext = Path(url).suffix or ".webp"
        entries.append(
            {
                "name": match.group("name"),
                "slug": match.group("slug"),
                "remote_url": BASE_URL + url,
                "filename": match.group("slug") + ext,
                "note": label,
            }
        )
    return unique_by_slug(entries)


def parse_weapons(html: str) -> list[dict[str, str]]:
    text = decode_next_payload(html)
    pattern = re.compile(r'"name":"(?P<name>[^"]+)","slug":"(?P<slug>[^"]+)".{0,1600}', re.S)
    entries: list[dict[str, str]] = []
    for match in pattern.finditer(text):
        block = match.group(0)
        url, label = extract_asset_url(block, "/api/weapon-portraits/file/", "/api/weapon-icons/file/")
        if not url:
            continue
        ext = Path(url).suffix or ".webp"
        entries.append(
            {
                "name": match.group("name"),
                "slug": match.group("slug"),
                "remote_url": BASE_URL + url,
                "filename": match.group("slug") + ext,
                "note": label,
            }
        )
    return unique_by_slug(entries)


def sync_entries(entries: list[dict[str, str]], target_dir: Path, kind: str) -> list[dict[str, str]]:
    target_dir.mkdir(parents=True, exist_ok=True)
    for existing in target_dir.iterdir():
        if existing.is_file():
            existing.unlink()

    output: list[dict[str, str]] = []
    for entry in entries:
        target_path = target_dir / entry["filename"]
        download_file(entry["remote_url"], target_path)
        output.append(
            {
                "name": entry["name"],
                "slug": entry["slug"],
                "src": f"/assets/img/reference/{kind}/{entry['filename']}",
                "note": entry["note"],
                "source": entry["remote_url"],
            }
        )
    return output


def main() -> int:
    char_html = fetch_text(PAGES["characters"])
    weapon_html = fetch_text(PAGES["weapons"])

    character_entries = parse_characters(char_html)
    weapon_entries = parse_weapons(weapon_html)

    data = {
        "characters": sync_entries(character_entries, CHAR_DIR, "characters"),
        "weapons": sync_entries(weapon_entries, WEAPON_DIR, "weapons"),
    }

    DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Downloaded {len(data['characters'])} character reference images into {CHAR_DIR}")
    print(f"Downloaded {len(data['weapons'])} weapon reference images into {WEAPON_DIR}")
    print(f"Wrote {DATA_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
