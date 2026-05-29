#!/bin/zsh
set -euo pipefail

ROOT="/Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net"
PYTHON_BIN="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

cd "$ROOT"

if [[ -f "$ROOT/.banner_check.env" ]]; then
  set -a
  source "$ROOT/.banner_check.env"
  set +a
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting WuWa daily official check"
"$PYTHON_BIN" -u scripts/check_official_banner_updates.py
"$PYTHON_BIN" -u scripts/prepare_banner_csv_candidate.py
"$PYTHON_BIN" -u scripts/update_daily_check_record.py
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Finished WuWa daily official check"
