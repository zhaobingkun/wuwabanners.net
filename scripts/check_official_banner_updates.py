from __future__ import annotations

import argparse
import csv
import json
import re
import ssl
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "banner-data.csv"
DEFAULT_REPORT = ROOT / "data" / "banner-update-report.json"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)

FETCH_TARGETS = [
    {
        "label": "official_site",
        "url": "https://wutheringwaves.kurogames.com/",
        "match_terms": ["wuthering waves", "version", "preview", "news"],
    },
    {
        "label": "official_youtube",
        "url": "https://www.youtube.com/@WutheringWaves/videos",
        "match_terms": ["wuthering waves", "preview", "special broadcast", "version"],
    },
    {
        "label": "dearplayers_updates",
        "url": "https://www.dearplayers.com/en-US/updates/wuthering-waves",
        "match_terms": ["wuthering waves", "version", "preview"],
    },
]


@dataclass
class FetchResult:
    url: str
    ok: bool
    status: str
    body: str = ""
    content_type: str = ""
    error: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check official Wuthering Waves sources for banner-related changes "
            "without modifying banner-data.csv."
        )
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DATA_CSV,
        help="Path to banner-data.csv",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="Path to write the JSON report",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Fetch timeout in seconds",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Do not write the JSON report file",
    )
    return parser.parse_args()


def parse_date(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def split_pipe(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split("|") if part.strip()]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def strip_html(value: str) -> str:
    value = re.sub(r"(?is)<script.*?>.*?</script>", " ", value)
    value = re.sub(r"(?is)<style.*?>.*?</style>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def fetch_url(url: str, timeout: int) -> FetchResult:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    context = ssl.create_default_context()
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            raw = response.read()
            content_type = response.headers.get("Content-Type", "")
            charset = response.headers.get_content_charset() or "utf-8"
            body = raw.decode(charset, errors="replace")
            return FetchResult(
                url=url,
                ok=True,
                status=str(response.status),
                body=body,
                content_type=content_type,
            )
    except (HTTPError, URLError, ssl.SSLError, TimeoutError) as exc:
        return fetch_url_with_curl(url, timeout, f"{type(exc).__name__}: {exc}")


def fetch_url_with_curl(url: str, timeout: int, previous_error: str) -> FetchResult:
    try:
        completed = subprocess.run(
            [
                "curl",
                "-L",
                "-sS",
                "--max-time",
                str(timeout),
                "-A",
                USER_AGENT,
                url,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return FetchResult(
            url=url,
            ok=True,
            status="curl-ok",
            body=completed.stdout,
            content_type="text/html",
        )
    except subprocess.CalledProcessError as exc:
        return FetchResult(
            url=url,
            ok=False,
            status="fetch-failed",
            error=f"{previous_error}; curl fallback failed: {exc}",
        )


def detect_versions(text: str) -> list[str]:
    matches = re.findall(r"version\s+(\d+\.\d+)", text, flags=re.I)
    seen: list[str] = []
    for match in matches:
        if match not in seen:
            seen.append(match)
    return seen


def build_row_check(row: dict[str, str], today: date) -> dict[str, Any]:
    last_checked = parse_date(row.get("last_checked", ""))
    age_days = (today - last_checked).days if last_checked else None
    row_check: dict[str, Any] = {
        "record_id": row.get("record_id", ""),
        "banner_name": row.get("banner_name", ""),
        "banner_type": row.get("banner_type", ""),
        "version": row.get("version", ""),
        "phase": row.get("phase", ""),
        "status": row.get("status", ""),
        "source_url": row.get("source_url", ""),
        "source_type": row.get("source_type", ""),
        "last_checked": row.get("last_checked", ""),
        "age_days": age_days,
        "needs_review": False,
        "reasons": [],
    }
    if age_days is None:
        row_check["needs_review"] = True
        row_check["reasons"].append("missing last_checked")
    elif age_days >= 7:
        row_check["needs_review"] = True
        row_check["reasons"].append(f"last_checked is {age_days} days old")
    if row.get("source_type") == "secondary_media":
        row_check["needs_review"] = True
        row_check["reasons"].append("source_type is secondary_media")
    return row_check


def probe_row_source(row: dict[str, str], timeout: int) -> dict[str, Any]:
    url = row.get("source_url", "").strip()
    if not url:
        return {
            "url": "",
            "fetch_ok": False,
            "status": "missing-url",
            "term_hits": [],
            "version_hits": [],
            "notes": ["No source_url set on this row."],
        }

    result = fetch_url(url, timeout)
    names = [
        row.get("banner_name", ""),
        *split_pipe(row.get("featured_characters", "")),
        *split_pipe(row.get("featured_weapons", "")),
        row.get("version", ""),
        row.get("phase", ""),
    ]
    probe_text = strip_html(result.body).lower()
    terms = [name for name in names if name]
    term_hits = [term for term in terms if term.lower() in probe_text]
    version_hits = detect_versions(probe_text)
    notes: list[str] = []

    if result.ok and terms and not term_hits:
        notes.append("Fetched page did not contain the expected banner or unit names.")
    if result.ok and row.get("version") and row["version"] not in version_hits:
        notes.append("Fetched page did not clearly expose the current version string.")
    if not result.ok:
        notes.append(result.error or "Could not fetch source URL.")

    return {
        "url": url,
        "fetch_ok": result.ok,
        "status": result.status,
        "term_hits": term_hits,
        "version_hits": version_hits,
        "notes": notes,
    }


def build_feed_checks(timeout: int, csv_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    current_versions = sorted({row.get("version", "") for row in csv_rows if row.get("version")})
    current_names = sorted(
        {
            name
            for row in csv_rows
            for name in split_pipe(row.get("featured_characters", "")) + split_pipe(row.get("featured_weapons", ""))
        }
    )
    checks: list[dict[str, Any]] = []
    for target in FETCH_TARGETS:
        result = fetch_url(target["url"], timeout)
        text = strip_html(result.body).lower()
        version_hits = detect_versions(text) if result.ok else []
        matched_names = [name for name in current_names if name.lower() in text]
        matched_terms = [term for term in target["match_terms"] if term.lower() in text]
        notes: list[str] = []
        if not result.ok:
            notes.append(result.error or "Could not fetch feed target.")
        if result.ok and not matched_terms:
            notes.append("Fetched page did not show the expected general Wuthering Waves update terms.")
        unseen_versions = [ver for ver in version_hits if ver not in current_versions]
        if unseen_versions:
            notes.append(f"Found possible newer version references: {', '.join(unseen_versions)}")
        checks.append(
            {
                "label": target["label"],
                "url": target["url"],
                "fetch_ok": result.ok,
                "status": result.status,
                "matched_terms": matched_terms,
                "matched_names": matched_names[:12],
                "version_hits": version_hits,
                "suggested_new_versions": unseen_versions,
                "notes": notes,
            }
        )
    return checks


def build_report(rows: list[dict[str, str]], timeout: int) -> dict[str, Any]:
    today = date.today()
    row_checks = [build_row_check(row, today) for row in rows]
    source_checks = [probe_row_source(row, timeout) for row in rows]
    for row_check, source_check in zip(row_checks, source_checks):
        if not source_check["fetch_ok"]:
            row_check["needs_review"] = True
            row_check["reasons"].append(f"source fetch failed: {source_check['status']}")
        elif not source_check["term_hits"]:
            row_check["needs_review"] = True
            row_check["reasons"].append("source page did not clearly match expected banner names")

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "csv_path": str(DATA_CSV.relative_to(ROOT)) if DATA_CSV.is_relative_to(ROOT) else str(DATA_CSV),
        "row_checks": row_checks,
        "source_checks": source_checks,
        "feed_checks": build_feed_checks(timeout, rows),
    }
    report["summary"] = summarize_report(report)
    return report


def summarize_report(report: dict[str, Any]) -> dict[str, Any]:
    row_checks = report["row_checks"]
    feed_checks = report["feed_checks"]
    needs_review = [row for row in row_checks if row["needs_review"]]
    failed_fetches = [row for row in report["source_checks"] if not row["fetch_ok"]]
    suggested_versions: list[str] = []
    for feed in feed_checks:
        for version in feed.get("suggested_new_versions", []):
            if version not in suggested_versions:
                suggested_versions.append(version)
    return {
        "rows_checked": len(row_checks),
        "rows_needing_review": len(needs_review),
        "failed_source_fetches": len(failed_fetches),
        "possible_new_versions": suggested_versions,
    }


def print_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print("WuWa Banners Official Update Check")
    print(f"Generated at: {report['generated_at']}")
    print(
        "Summary: "
        f"{summary['rows_needing_review']} rows need review, "
        f"{summary['failed_source_fetches']} source fetches failed, "
        f"possible new versions: {', '.join(summary['possible_new_versions']) or 'none'}"
    )
    print("\nRows needing review:")
    any_rows = False
    for row in report["row_checks"]:
        if not row["needs_review"]:
            continue
        any_rows = True
        print(f"- {row['record_id']} ({row['banner_name']}):")
        for reason in row["reasons"]:
            print(f"  - {reason}")
    if not any_rows:
        print("- none")

    print("\nFeed checks:")
    for feed in report["feed_checks"]:
        versions = ", ".join(feed["version_hits"]) or "none"
        suggested = ", ".join(feed["suggested_new_versions"]) or "none"
        print(f"- {feed['label']}: {feed['status']} | versions seen: {versions} | new: {suggested}")
        for note in feed["notes"]:
            print(f"  - {note}")


def main() -> int:
    args = parse_args()
    rows = read_rows(args.csv)
    report = build_report(rows, args.timeout)
    print_report(report)

    if not args.no_report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nWrote report: {args.report}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
