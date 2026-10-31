#!/usr/bin/env python3
"""Build the public-only static asset bundle used by Cloudflare Workers."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HOST = "wuwabanners.net"
EXCLUDED_PARTS = {
    ".git",
    ".github",
    ".vercel",
    "YouTube",
    "__pycache__",
    "dist",
    "product-design-audit-2026-06-17",
    "reports",
    "scripts",
}
ROOT_PUBLIC_FILES = {
    "index.html",
    "404.html",
    "ads.txt",
    "robots.txt",
    "sitemap.xml",
    "favicon.ico",
    "favicon.svg",
    "site.webmanifest",
}
PUBLIC_JSON = {"data/reference-images.json"}
VERIFICATION_FILE = re.compile(r"^[0-9a-f]{32}\.txt$")


def should_copy(relative: Path) -> bool:
    if any(part in EXCLUDED_PARTS or part.startswith(".") for part in relative.parts):
        return False
    if relative.as_posix() in PUBLIC_JSON:
        return True
    if len(relative.parts) == 1:
        return relative.name in ROOT_PUBLIC_FILES or bool(VERIFICATION_FILE.fullmatch(relative.name))
    if relative.parts[0] == "assets":
        return True
    return relative.suffix.lower() == ".html"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or (ROOT in output.parents and output.name in {"assets", "scripts"}):
        raise SystemExit(f"Refusing unsafe output directory: {output}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    count = 0
    for source in ROOT.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        if not should_copy(relative):
            continue
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        count += 1
    headers = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

https://:worker.bingkun-zhao.workers.dev/*
  X-Robots-Tag: noindex
"""
    (output / "_headers").write_text(headers, encoding="utf-8")
    required = [
        output / "index.html",
        output / "404.html",
        output / "robots.txt",
        output / "sitemap.xml",
        output / "data/reference-images.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing required public files: " + ", ".join(missing))
    print(f"Built {count} public files for https://{CANONICAL_HOST} in {output}")


if __name__ == "__main__":
    main()
