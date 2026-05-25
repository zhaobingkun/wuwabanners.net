from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "data" / "banner-data.csv"
DEFAULT_REPORT = ROOT / "data" / "banner-update-report.json"
DEFAULT_CANDIDATE = ROOT / "data" / "banner-data.candidate.csv"
DEFAULT_DIFF = ROOT / "data" / "banner-data.diff.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a safe candidate CSV and a human-readable diff report from "
            "banner-update-report.json without modifying the live banner-data.csv."
        )
    )
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to the live banner CSV.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="Path to the JSON check report.")
    parser.add_argument(
        "--candidate",
        type=Path,
        default=DEFAULT_CANDIDATE,
        help="Where to write the candidate CSV copy.",
    )
    parser.add_argument(
        "--diff",
        type=Path,
        default=DEFAULT_DIFF,
        help="Where to write the text diff / action list.",
    )
    parser.add_argument(
        "--today",
        type=str,
        default=date.today().isoformat(),
        help="Override the YYYY-MM-DD date used for safe last_checked suggestions.",
    )
    return parser.parse_args()


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_maps(report: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    row_checks = {
        item["record_id"]: item
        for item in report.get("row_checks", [])
        if item.get("record_id")
    }
    source_checks = {
        row["record_id"]: source
        for row, source in zip(report.get("row_checks", []), report.get("source_checks", []))
        if row.get("record_id")
    }
    return row_checks, source_checks


def can_auto_refresh_last_checked(row_check: dict[str, Any], source_check: dict[str, Any]) -> bool:
    if not source_check.get("fetch_ok"):
        return False
    if row_check.get("source_type") == "secondary_media":
        return False
    if not source_check.get("term_hits"):
        return False
    notes = source_check.get("notes", [])
    if any("did not contain" in note.lower() for note in notes):
        return False
    return True


def write_candidate_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_diff_text(
    rows: list[dict[str, str]],
    row_checks: dict[str, dict[str, Any]],
    source_checks: dict[str, dict[str, Any]],
    report: dict[str, Any],
    today: str,
    auto_updates: list[str],
) -> str:
    lines: list[str] = []
    lines.append("WuWa Banners Candidate CSV Diff")
    lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Candidate date: {today}")
    lines.append("")
    lines.append("What this file means")
    lines.append("- This is not the live CSV.")
    lines.append("- Safe rows may have only `last_checked` refreshed to today.")
    lines.append("- Anything involving lineup, dates, source_url, source_type, or new versions still needs manual review.")
    lines.append("")

    lines.append("Automatic candidate updates applied")
    if auto_updates:
        for item in auto_updates:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("Rows that still need manual review")
    any_manual = False
    for row in rows:
        record_id = row.get("record_id", "")
        row_check = row_checks.get(record_id, {})
        source_check = source_checks.get(record_id, {})
        reasons = list(row_check.get("reasons", []))
        if source_check.get("notes"):
            reasons.extend(source_check["notes"])
        if can_auto_refresh_last_checked(row_check, source_check):
            continue
        if not reasons:
            continue
        any_manual = True
        lines.append(f"- {record_id} ({row.get('banner_name', '')})")
        lines.append(f"  - Current source: {row.get('source_url', '')}")
        for reason in reasons:
            lines.append(f"  - {reason}")
    if not any_manual:
        lines.append("- none")
    lines.append("")

    lines.append("Possible new version signals from feed checks")
    feed_checks = report.get("feed_checks", [])
    any_new_versions = False
    for feed in feed_checks:
        suggested = feed.get("suggested_new_versions", [])
        if not suggested:
            continue
        any_new_versions = True
        lines.append(f"- {feed.get('label', 'feed')}: {', '.join(suggested)}")
    if not any_new_versions:
        lines.append("- none")
    lines.append("")

    lines.append("Recommended next steps")
    lines.append("1. Open data/banner-data.diff.txt and read only the rows listed under manual review.")
    lines.append("2. Compare those rows against official notices or in-game Convene.")
    lines.append("3. If the candidate CSV only refreshed last_checked on safe rows, you may copy those cells into data/banner-data.csv.")
    lines.append("4. For banner, date, lineup, or source_url changes, edit data/banner-data.csv manually.")
    lines.append("5. Then run: python3 scripts/run_banner_update_cycle.py")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if not args.report.exists():
        subprocess.run(
            ["python3", "scripts/check_official_banner_updates.py"],
            cwd=ROOT,
            check=True,
        )
    fieldnames, rows = read_csv_rows(args.csv)
    report = load_json(args.report)
    row_checks, source_checks = build_maps(report)
    auto_updates: list[str] = []

    for row in rows:
        record_id = row.get("record_id", "")
        row_check = row_checks.get(record_id, {})
        source_check = source_checks.get(record_id, {})
        if not row_check:
            continue
        if can_auto_refresh_last_checked(row_check, source_check):
            previous = row.get("last_checked", "")
            if previous != args.today:
                row["last_checked"] = args.today
                auto_updates.append(f"{record_id}: last_checked {previous or '[empty]'} -> {args.today}")

    write_candidate_csv(args.candidate, fieldnames, rows)
    diff_text = build_diff_text(rows, row_checks, source_checks, report, args.today, auto_updates)
    args.diff.write_text(diff_text, encoding="utf-8")

    print(f"Wrote candidate CSV: {args.candidate}")
    print(f"Wrote diff report: {args.diff}")
    print(f"Automatic safe last_checked updates: {len(auto_updates)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
