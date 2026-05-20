#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."
python3 scripts/download_wuwatracker_reference_images.py
