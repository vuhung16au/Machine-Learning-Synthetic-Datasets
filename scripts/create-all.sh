#!/usr/bin/env bash
set -euo pipefail

# Generate representative datasets across tasks and sizes

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

echo "Generating classification datasets..."
$PYTHON_BIN scripts/generate_datasets.py --task classification --size small  --num-samples 5000   --num-features 20 --num-classes 3 --random-state 42
$PYTHON_BIN scripts/generate_datasets.py --task classification --size medium --num-samples 20000  --num-features 30 --num-classes 5 --random-state 7
$PYTHON_BIN scripts/generate_datasets.py --task classification --size large  --num-samples 120000 --num-features 40 --num-classes 2 --random-state 1

echo "Generating regression datasets..."
$PYTHON_BIN scripts/generate_datasets.py --task regression --size small  --num-samples 4000   --num-features 15 --noise 3.0 --bias 1.0 --random-state 11
$PYTHON_BIN scripts/generate_datasets.py --task regression --size medium --num-samples 30000  --num-features 25 --noise 5.0 --bias 0.0 --random-state 21
$PYTHON_BIN scripts/generate_datasets.py --task regression --size large  --num-samples 150000 --num-features 35 --noise 8.0 --bias 2.0 --random-state 31

echo "Generating clustering datasets..."
$PYTHON_BIN scripts/generate_datasets.py --task clustering --size small  --num-samples 6000   --num-features 10 --num-clusters 4 --cluster-std 1.0 --random-state 101
$PYTHON_BIN scripts/generate_datasets.py --task clustering --size medium --num-samples 40000  --num-features 12 --num-clusters 6 --cluster-std 1.2 --random-state 202
$PYTHON_BIN scripts/generate_datasets.py --task clustering --size large  --num-samples 200000 --num-features 16 --num-clusters 5 --cluster-std 1.5 --random-state 303

echo "All datasets generated in ./datasets/{small,medium,large}"

