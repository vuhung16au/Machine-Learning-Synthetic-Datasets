#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root as parent of this script's directory
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
# Auto-detect python (prefer project venv)
if [ -z "${PYTHON_BIN:-}" ]; then
  if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
    PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python)"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "Python not found. Set PYTHON_BIN to your interpreter." >&2
    exit 1
  fi
fi

cd "$ROOT_DIR"

echo "Compressing all CSV datasets under ./datasets ..."
$PYTHON_BIN scripts/compress_datasets.py --root datasets "$@"

echo "Compression complete."

