from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run_step(label: str, command: list[str]) -> None:
    print(f"\n== {label} ==", flush=True)
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    run_step("Rebuild reference detail pages", ["python3", "scripts/build_reference_pages.py"])
    run_step("Rebuild banner snapshot pages", ["python3", "scripts/build_banner_snapshot.py"])
    run_step(
        "Compile-check Python scripts",
        [
            "python3",
            "-m",
            "py_compile",
            "scripts/build_banner_snapshot.py",
            "scripts/build_reference_pages.py",
            "scripts/verify_site_build.py",
            "scripts/run_banner_update_cycle.py",
        ],
    )
    run_step("Syntax-check site.js", ["node", "--check", "assets/js/site.js"])
    run_step("Verify core site build", ["python3", "scripts/verify_site_build.py"])
    print("\nUpdate cycle completed successfully.")
    print("Next step: preview locally or deploy the refreshed site.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
