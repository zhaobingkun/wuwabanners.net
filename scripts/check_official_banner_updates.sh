#!/bin/zsh
set -euo pipefail
cd /Users/zhaobingkun/dev/wuthering-waves-next-banner/wuwabanners.net
python3 scripts/check_official_banner_updates.py "$@"
