#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root as parent of this script's directory
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"

cd "$ROOT_DIR"

echo "Compressing all CSV datasets under ./datasets ..."
$PYTHON_BIN scripts/compress_datasets.py --root datasets "$@"

echo "Compression complete."

