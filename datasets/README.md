# Datasets

This directory stores generated CSV datasets.

## Layout
- `small/`: ~1k – 10k rows
- `medium/`: ~10k – 100k rows
- `large/`: ~100k – 1M rows

All files are UTF-8, comma-separated, and include a header row.

## File naming

Naming pattern depends on task:
- Classification: `classification_n{N}_f{F}_c{C}_inf{INF}_sep{SEP}_rs{RS}.csv`
- Regression: `regression_n{N}_f{F}_noise{NOISE}_bias{BIAS}_rs{RS}.csv`
- Clustering: `clustering_n{N}_f{F}_k{K}_std{STD}_rs{RS}.csv`

Where:
- `N` = number of samples
- `F` = number of features
- `C` = number of classes
- `INF` = number of informative features
- `SEP` = class separation
- `K` = number of clusters
- `STD` = cluster standard deviation
- `RS` = random state (if specified)

Columns:
- Features: `x1, x2, ..., xF`
- Labels: `y` for classification/regression; `cluster` for clustering

## Generating
Use the CLI:
```bash
python ../scripts/generate_datasets.py --help
```

Example:
```bash
python ../scripts/generate_datasets.py --task classification --size small \
  --num-samples 5000 --num-features 20 --num-classes 3 --random-state 42
```

## Compression
Gzip in place:
```bash
python ../scripts/compress_datasets.py --root ..
```
