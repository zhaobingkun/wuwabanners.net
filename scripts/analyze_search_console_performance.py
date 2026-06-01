#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


ALIASES = {
    "query": {"query", "queries", "top queries", "搜索字词", "查询", "热门查询"},
    "page": {"page", "pages", "url", "网址", "网页", "页面", "排名靠前的网页", "热门网页"},
    "clicks": {"clicks", "点击次数", "点击"},
    "impressions": {"impressions", "展示次数", "展示"},
    "ctr": {"ctr", "点击率"},
    "position": {"position", "average position", "avg position", "排名", "平均排名", "平均排名位置"},
}


def normalize_header(value: str) -> str:
    return value.strip().lower().replace("\ufeff", "")


def find_column(headers: list[str], logical_name: str) -> str | None:
    wanted = ALIASES[logical_name]
    for header in headers:
        if normalize_header(header) in wanted:
            return header
    return None


def parse_number(value: str) -> float:
    value = value.strip().replace(",", "").replace("%", "")
    if not value:
        return 0.0
    return float(value)


def parse_ctr(value: str) -> float:
    stripped = value.strip()
    if not stripped:
        return 0.0
    parsed = parse_number(stripped)
    return parsed / 100.0 if "%" in stripped or parsed > 1 else parsed


def score_row(clicks: float, impressions: float, ctr: float, position: float) -> float:
    if impressions <= 0:
        return 0.0
    rank_bonus = max(0.0, 35.0 - position) if position else 10.0
    ctr_gap = max(0.0, 0.06 - ctr)
    return impressions * ctr_gap * (1.0 + rank_bonus / 35.0) - clicks * 0.25


def classify_action(ctr: float, position: float, impressions: float) -> str:
    if impressions < 20:
        return "watch"
    if position and position <= 12 and ctr < 0.04:
        return "rewrite title/meta and first answer"
    if position and 12 < position <= 30:
        return "expand page answer and strengthen internal links"
    if position and position > 30:
        return "check intent fit before expanding"
    if ctr < 0.03:
        return "rewrite snippet target"
    return "monitor"


def analyze(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise SystemExit(
            f"Input CSV not found: {input_path}\n"
            "Pass the real Search Console Performance export path, for example:\n"
            "python3 scripts/analyze_search_console_performance.py "
            "'/Users/zhaobingkun/doc/seo资料/performance.csv'\n"
            "The placeholder name search-console-performance.csv is not created by the script."
        )

    with input_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise SystemExit("Input CSV has no header row.")
        headers = reader.fieldnames
        columns = {name: find_column(headers, name) for name in ALIASES}
        if not columns["clicks"] or not columns["impressions"]:
            header_text = ", ".join(headers)
            raise SystemExit(
                "CSV must include clicks and impressions columns.\n"
                f"Detected columns: {header_text}\n"
                "This script needs a Search Console Performance export, not a Coverage/Indexing export. "
                "In Search Console, open Performance, then export Queries or Pages."
            )

        rows = []
        for row in reader:
            clicks = parse_number(row.get(columns["clicks"], "")) if columns["clicks"] else 0.0
            impressions = parse_number(row.get(columns["impressions"], "")) if columns["impressions"] else 0.0
            ctr = parse_ctr(row.get(columns["ctr"], "")) if columns["ctr"] else 0.0
            position = parse_number(row.get(columns["position"], "")) if columns["position"] else 0.0
            rows.append(
                {
                    "query": row.get(columns["query"], "") if columns["query"] else "",
                    "page": row.get(columns["page"], "") if columns["page"] else "",
                    "clicks": int(clicks),
                    "impressions": int(impressions),
                    "ctr": f"{ctr:.4f}",
                    "position": f"{position:.1f}" if position else "",
                    "priority_score": f"{score_row(clicks, impressions, ctr, position):.2f}",
                    "recommended_action": classify_action(ctr, position, impressions),
                }
            )

    rows.sort(key=lambda item: float(item["priority_score"]), reverse=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        fieldnames = ["query", "page", "clicks", "impressions", "ctr", "position", "priority_score", "recommended_action"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prioritize Search Console queries/pages by impressions, CTR gap, and position.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/search-console-opportunities.csv"))
    args = parser.parse_args()
    analyze(args.input_csv, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
