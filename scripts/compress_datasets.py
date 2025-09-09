#!/usr/bin/env python3
import argparse
import gzip
import shutil
from pathlib import Path


def compress_csv(csv_path: Path, overwrite: bool = False) -> Path:
    gz_path = csv_path.with_suffix(csv_path.suffix + ".gz")
    if gz_path.exists() and not overwrite:
        return gz_path
    with open(csv_path, "rb") as f_in, gzip.open(gz_path, "wb", compresslevel=6, mtime=0) as f_out:
        shutil.copyfileobj(f_in, f_out)
    return gz_path


def iter_csv_files(root: Path):
    for p in root.rglob("*.csv"):
        yield p


def parse_args():
    p = argparse.ArgumentParser(description="Gzip all CSV files under a root directory")
    p.add_argument("--root", default="datasets", help="Root directory to scan (default: datasets)")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing .csv.gz files")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    count = 0
    for csv_path in iter_csv_files(root):
        gz_path = compress_csv(csv_path, overwrite=args.overwrite)
        count += 1
        print(f"Compressed {csv_path} -> {gz_path}")
    if count == 0:
        print("No CSV files found.")
    else:
        print(f"Done. Compressed {count} CSV files.")


if __name__ == "__main__":
    main()
