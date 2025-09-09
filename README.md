# Machine-Learning-Synthetic-Datasets

A collection of synthetic datasets for machine learning models and experiments.

## Repository structure

```
.
├── datasets/
│   ├── small/
│   ├── medium/
│   ├── large/
│   ├── README.md
│   └── .gitignore
├── scripts/
│   ├── generate_datasets.py
│   ├── compress_datasets.py
│   ├── README.md
│   └── .gitignore
├── LICENSE.md
├── requirements.txt
└── README.md
```

## Objectives of the synthetic datasets

- Provide ready-to-use datasets to demonstrate ML workflows
- Cover supervised, unsupervised, and semi-supervised learning
- Support task types: classification, regression, clustering
- Support a range of dataset sizes and feature counts

Size targets (rows):
- small: 1,000 – 10,000
- medium: 10,000 – 100,000
- large: 100,000 – 1,000,000
- extra large: 1,000,000 – 10,000,000

Feature targets:
- Features: 1 – 100 (default range)
- Classes: 2 – 10 (classification)
- Clusters: 2 – 10 (clustering)

All datasets are CSV with header, comma-separated, UTF-8 encoded.

## How to generate the datasets

1) Install dependencies

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Generate datasets (examples)

- Classification (tabular):
```bash
python scripts/generate_datasets.py \
  --task classification \
  --size small \
  --num-samples 5000 \
  --num-features 20 \
  --num-classes 3 \
  --random-state 42
```

- Regression (tabular):
```bash
python scripts/generate_datasets.py \
  --task regression \
  --size medium \
  --num-samples 20000 \
  --num-features 15 \
  --noise 5.0 \
  --random-state 7
```

- Clustering (tabular):
```bash
python scripts/generate_datasets.py \
  --task clustering \
  --size large \
  --num-samples 150000 \
  --num-features 10 \
  --num-clusters 5 \
  --cluster-std 1.2 \
  --random-state 1
```

- Semi-supervised variant (mask labels):
```bash
python scripts/generate_datasets.py \
  --task classification \
  --size small \
  --num-samples 8000 \
  --num-features 10 \
  --num-classes 2 \
  --semi-supervised 0.3 \
  --random-state 123
```

Outputs are written to `datasets/<size>/` with informative filenames.

## How to compress the datasets

Compress all CSVs with gzip, producing `.csv.gz` side-by-side:

```bash
python scripts/compress_datasets.py --root datasets
```

## Makefile usage

Convenience targets from the repository root:

```bash
make help           # List available targets
make create-all     # Generate representative datasets across tasks and sizes
make compress-all   # Compress all CSV datasets (creates .csv.gz)
make clean          # Delete all CSV files in datasets/
make clean-gzip     # Delete all .csv.gz files in datasets/
```

## Shell scripts usage

You can run the helper shell scripts directly from the root (they auto-detect the venv’s Python):

```bash
bash scripts/create-all.sh
bash scripts/compress-all.sh [--overwrite]
```

## How to use the datasets

- Load with pandas:
```python
import pandas as pd
Xy = pd.read_csv("datasets/small/classification_n8000_f10_c2_rs123.csv")
```
- Typical model demos (Phase 1.2 targets): linear/logistic regression, decision tree, random forest, SVM, k-means, DBSCAN, neural networks, gradient boosting, XGBoost, LightGBM, CatBoost, Naive Bayes.

For examples of which datasets are suitable:
- Classification: logistic regression, SVM, trees/forests, boosting, naive bayes, neural nets
- Regression: linear regression, trees/forests, boosting, neural nets
- Clustering: k-means, DBSCAN, GMM (not bundled), spectral clustering (not bundled)

See `scripts/README.md` for full CLI options.
