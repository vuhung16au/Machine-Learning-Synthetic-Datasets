# Scripts

Utilities to generate and compress datasets.

## generate_datasets.py

Generate tabular synthetic datasets for different ML tasks.

Usage:
```bash
python scripts/generate_datasets.py --task {classification,regression,clustering} \
  --size {small,medium,large} \
  --num-samples N --num-features F [options]
```

Common options:
- `--random-state INT`: set RNG seed
- `--semi-supervised FLOAT`: fraction (0-1) of labels to mask

Classification options:
- `--num-classes INT` (default 2)
- `--num-informative INT` (default F//2 heuristic)
- `--num-redundant INT` (default 0)
- `--num-repeated INT` (default 0)
- `--class-sep FLOAT` (default 1.0)

Regression options:
- `--noise FLOAT` (default 0.0)
- `--bias FLOAT` (default 0.0)

Clustering options:
- `--num-clusters INT` (default 3)
- `--cluster-std FLOAT` (default 1.0)
- `--center-box-min FLOAT` (default -10)
- `--center-box-max FLOAT` (default 10)

Outputs are written to `datasets/<size>/`.

## compress_datasets.py

Gzip all CSV files under a root directory.

Usage:
```bash
python scripts/compress_datasets.py --root datasets [--overwrite]
```
