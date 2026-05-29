from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DEFAULT_REPORT = DATA_DIR / "banner-update-report.json"
DEFAULT_DIFF = DATA_DIR / "banner-data.diff.txt"
DEFAULT_STATE = DATA_DIR / "banner-check-state.json"
DEFAULT_RECORD = DATA_DIR / "banner-check-record.txt"
DEFAULT_HISTORY = DATA_DIR / "banner-check-history.log"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare the latest WuWa banner check outputs against the previous run "
            "and write a human-friendly record file plus a history log."
        )
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--diff", type=Path, default=DEFAULT_DIFF)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--record", type=Path, default=DEFAULT_RECORD)
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_list(values: list[Any]) -> list[str]:
    items = [str(value).strip() for value in values if str(value).strip()]
    return sorted(dict.fromkeys(items))


def parse_diff_sections(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines()
    section = ""
    auto_updates: list[str] = []
    manual_review_ids: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped == "Automatic candidate updates applied":
            section = "auto"
            continue
        if stripped == "Rows that still need manual review":
            section = "manual"
            continue
        if stripped in {
            "Possible new version signals from feed checks",
            "Recommended next steps",
            "What this file means",
        }:
            section = ""
            continue

        if section == "auto" and line.startswith("- ") and stripped != "- none":
            auto_updates.append(line[2:].strip())
            continue

        if section == "manual" and line.startswith("- ") and " (" in stripped:
            manual_review_ids.append(line[2:].strip().split(" (", 1)[0].strip())

    return auto_updates, manual_review_ids


def build_signature(report: dict[str, Any], diff_text: str) -> dict[str, Any]:
    auto_updates, manual_review_ids = parse_diff_sections(diff_text)

    row_map: dict[str, Any] = {}
    source_map: dict[str, Any] = {}
    row_checks = report.get("row_checks", [])
    source_checks = report.get("source_checks", [])

    for row in row_checks:
        record_id = row.get("record_id", "").strip()
        if not record_id:
            continue
        row_map[record_id] = {
            "banner_name": row.get("banner_name", ""),
            "version": row.get("version", ""),
            "phase": row.get("phase", ""),
            "status": row.get("status", ""),
            "source_url": row.get("source_url", ""),
            "source_type": row.get("source_type", ""),
            "needs_review": bool(row.get("needs_review")),
            "reasons": normalize_list(row.get("reasons", [])),
        }

    for row, source in zip(row_checks, source_checks):
        record_id = row.get("record_id", "").strip()
        if not record_id:
            continue
        source_map[record_id] = {
            "fetch_ok": bool(source.get("fetch_ok")),
            "status": source.get("status", ""),
            "term_hits": normalize_list(source.get("term_hits", [])),
            "version_hits": normalize_list(source.get("version_hits", [])),
            "notes": normalize_list(source.get("notes", [])),
        }

    feed_map: dict[str, Any] = {}
    for feed in report.get("feed_checks", []):
        label = feed.get("label", "").strip()
        if not label:
            continue
        feed_map[label] = {
            "fetch_ok": bool(feed.get("fetch_ok")),
            "status": feed.get("status", ""),
            "version_hits": normalize_list(feed.get("version_hits", [])),
            "suggested_new_versions": normalize_list(feed.get("suggested_new_versions", [])),
            "notes": normalize_list(feed.get("notes", [])),
        }

    return {
        "report_generated_at": report.get("generated_at", ""),
        "summary": report.get("summary", {}),
        "rows": row_map,
        "sources": source_map,
        "feeds": feed_map,
        "auto_updates": auto_updates,
        "manual_review_ids": sorted(dict.fromkeys(manual_review_ids)),
    }


def diff_lists(old: list[str], new: list[str]) -> tuple[list[str], list[str]]:
    old_set = set(old)
    new_set = set(new)
    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    return added, removed


def join_or_none(values: list[str]) -> str:
    return ", ".join(values) if values else "none"


def compare_signatures(previous: dict[str, Any] | None, current: dict[str, Any]) -> tuple[str, list[str]]:
    if previous is None:
        return "FIRST_RUN", [
            "No previous baseline existed. Created the first comparison snapshot from the current report."
        ]

    changes: list[str] = []

    previous_summary = previous.get("summary", {})
    current_summary = current.get("summary", {})
    summary_keys = [
        "rows_checked",
        "rows_needing_review",
        "failed_source_fetches",
        "possible_new_versions",
    ]
    for key in summary_keys:
        old_value = previous_summary.get(key, [] if key == "possible_new_versions" else 0)
        new_value = current_summary.get(key, [] if key == "possible_new_versions" else 0)
        if old_value != new_value:
            changes.append(f"Summary changed: {key}: {old_value} -> {new_value}")

    previous_rows = previous.get("rows", {})
    current_rows = current.get("rows", {})
    previous_ids = set(previous_rows)
    current_ids = set(current_rows)
    for record_id in sorted(current_ids - previous_ids):
        row = current_rows[record_id]
        changes.append(
            f"New record appeared: {record_id} ({row.get('banner_name', '')}, {row.get('version', '')} {row.get('phase', '')})"
        )
    for record_id in sorted(previous_ids - current_ids):
        row = previous_rows[record_id]
        changes.append(
            f"Record disappeared: {record_id} ({row.get('banner_name', '')}, {row.get('version', '')} {row.get('phase', '')})"
        )

    shared_row_ids = sorted(previous_ids & current_ids)
    for record_id in shared_row_ids:
        old_row = previous_rows[record_id]
        new_row = current_rows[record_id]
        for field in ("source_url", "source_type", "status", "version", "phase", "needs_review"):
            if old_row.get(field) != new_row.get(field):
                changes.append(
                    f"{record_id}: {field} changed: {old_row.get(field)} -> {new_row.get(field)}"
                )
        old_reasons = old_row.get("reasons", [])
        new_reasons = new_row.get("reasons", [])
        if old_reasons != new_reasons:
            added, removed = diff_lists(old_reasons, new_reasons)
            changes.append(
                f"{record_id}: reasons changed. Added: {join_or_none(added)}. Removed: {join_or_none(removed)}"
            )

    previous_sources = previous.get("sources", {})
    current_sources = current.get("sources", {})
    for record_id in sorted(set(previous_sources) & set(current_sources)):
        old_source = previous_sources[record_id]
        new_source = current_sources[record_id]
        for field in ("fetch_ok", "status"):
            if old_source.get(field) != new_source.get(field):
                changes.append(
                    f"{record_id}: source probe {field} changed: {old_source.get(field)} -> {new_source.get(field)}"
                )
        for field in ("term_hits", "version_hits"):
            if old_source.get(field) != new_source.get(field):
                changes.append(
                    f"{record_id}: source probe {field} changed: {old_source.get(field)} -> {new_source.get(field)}"
                )

    previous_feeds = previous.get("feeds", {})
    current_feeds = current.get("feeds", {})
    for label in sorted(set(previous_feeds) | set(current_feeds)):
        old_feed = previous_feeds.get(label)
        new_feed = current_feeds.get(label)
        if old_feed is None and new_feed is not None:
            changes.append(f"New feed check appeared: {label}")
            continue
        if old_feed is not None and new_feed is None:
            changes.append(f"Feed check disappeared: {label}")
            continue
        assert old_feed is not None and new_feed is not None
        for field in ("fetch_ok", "status", "version_hits", "suggested_new_versions"):
            if old_feed.get(field) != new_feed.get(field):
                changes.append(
                    f"Feed {label}: {field} changed: {old_feed.get(field)} -> {new_feed.get(field)}"
                )

    old_auto_updates = previous.get("auto_updates", [])
    new_auto_updates = current.get("auto_updates", [])
    if old_auto_updates != new_auto_updates:
        added, removed = diff_lists(old_auto_updates, new_auto_updates)
        changes.append(
            "Automatic candidate updates changed. "
            f"Added: {join_or_none(added)}. Removed: {join_or_none(removed)}"
        )

    old_manual = previous.get("manual_review_ids", [])
    new_manual = current.get("manual_review_ids", [])
    if old_manual != new_manual:
        added, removed = diff_lists(old_manual, new_manual)
        changes.append(
            "Manual review rows changed. "
            f"Added: {join_or_none(added)}. Removed: {join_or_none(removed)}"
        )

    if not changes:
        return "NO_SIGNIFICANT_CHANGE", ["No significant change compared with the previous run."]
    return "CHANGED", changes


def build_record_text(status: str, current: dict[str, Any], changes: list[str]) -> str:
    summary = current.get("summary", {})
    lines: list[str] = []
    lines.append("WuWa Banner Check Record")
    lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Compared report generated at: {current.get('report_generated_at', 'unknown')}")
    lines.append(f"Comparison result: {status}")
    lines.append("")
    lines.append("What you should look at first")
    lines.append("- Read this file from top to bottom.")
    lines.append("- If Comparison result is NO_SIGNIFICANT_CHANGE, you usually do not need to do anything new today.")
    lines.append("- If Comparison result is CHANGED, review the changed items below before touching data/banner-data.csv.")
    lines.append("")
    lines.append("Current summary")
    lines.append(f"- rows_checked: {summary.get('rows_checked', 0)}")
    lines.append(f"- rows_needing_review: {summary.get('rows_needing_review', 0)}")
    lines.append(f"- failed_source_fetches: {summary.get('failed_source_fetches', 0)}")
    lines.append(
        f"- possible_new_versions: {join_or_none(summary.get('possible_new_versions', []))}"
    )
    lines.append(
        f"- manual_review_rows: {join_or_none(current.get('manual_review_ids', []))}"
    )
    lines.append(
        f"- automatic_candidate_updates: {join_or_none(current.get('auto_updates', []))}"
    )
    lines.append("")
    lines.append("Changes since last run")
    for change in changes:
        lines.append(f"- {change}")
    lines.append("")
    lines.append("Action today")
    if status == "NO_SIGNIFICANT_CHANGE":
        lines.append("- No new difference was detected against the previous run.")
        lines.append("- If the current summary also looks unchanged, you can usually stop here.")
    elif status == "FIRST_RUN":
        lines.append("- This was the first baseline build for the record system.")
        lines.append("- From the next run onward, this file will tell you exactly what changed.")
    else:
        lines.append("- Something changed compared with the previous run.")
        lines.append("- Check whether the change is a real official-source update or just a source-health change.")
        lines.append("- Only if the banner facts changed should you edit data/banner-data.csv and rebuild.")
    lines.append("")
    lines.append("Reference files")
    lines.append("- data/banner-update-report.json")
    lines.append("- data/banner-data.diff.txt")
    lines.append("- data/banner-data.candidate.csv")
    lines.append("- data/banner-data.csv")
    return "\n".join(lines) + "\n"


def append_history(path: Path, status: str, current: dict[str, Any], changes: list[str]) -> None:
    summary = current.get("summary", {})
    stamp = datetime.now().isoformat(timespec="seconds")
    lines = [
        f"[{stamp}] {status}",
        f"report_generated_at={current.get('report_generated_at', 'unknown')}",
        (
            "summary="
            f"rows_checked:{summary.get('rows_checked', 0)},"
            f"rows_needing_review:{summary.get('rows_needing_review', 0)},"
            f"failed_source_fetches:{summary.get('failed_source_fetches', 0)},"
            f"possible_new_versions:{join_or_none(summary.get('possible_new_versions', []))}"
        ),
    ]
    for change in changes:
        lines.append(f"- {change}")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    report = load_json(args.report)
    diff_text = load_text(args.diff)
    current = build_signature(report, diff_text)

    previous_state: dict[str, Any] | None = None
    if args.state.exists():
        previous_state = load_json(args.state)

    status, changes = compare_signatures(previous_state, current)
    args.record.write_text(build_record_text(status, current, changes), encoding="utf-8")
    append_history(args.history, status, current, changes)
    args.state.write_text(
        json.dumps(current, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote record file: {args.record}")
    print(f"Appended history log: {args.history}")
    print(f"Comparison result: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
