#!/usr/bin/env bash
set -euo pipefail

# Creates a virtualenv (if missing), activates it, installs dependencies and runs the game.
# Usage: ./start.sh

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
  python -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python main.py

