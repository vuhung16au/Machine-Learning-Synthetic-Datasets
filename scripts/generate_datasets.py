#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression, make_blobs


SIZE_TO_DIR = {
    "small": "small",
    "medium": "medium",
    "large": "large",
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_output_dir(root: Path, size: str) -> Path:
    if size not in SIZE_TO_DIR:
        raise ValueError(f"size must be one of {list(SIZE_TO_DIR.keys())}")
    out = root / SIZE_TO_DIR[size]
    ensure_dir(out)
    return out


def sanitize_float(value: float) -> str:
    s = ("%g" % value).replace(".", "p")
    return s


def make_filename(task: str,
                  num_samples: int,
                  num_features: int,
                  extra: str,
                  random_state: Optional[int]) -> str:
    parts = [task, f"n{num_samples}", f"f{num_features}"]
    if extra:
        parts.append(extra)
    if random_state is not None:
        parts.append(f"rs{random_state}")
    return "_".join(parts) + ".csv"


def generate_classification(num_samples: int,
                            num_features: int,
                            num_informative: Optional[int],
                            num_redundant: int,
                            num_repeated: int,
                            num_classes: int,
                            class_sep: float,
                            random_state: Optional[int]) -> Tuple[pd.DataFrame, str]:
    if num_informative is None:
        # heuristic: half informative, rest split redundant/repeated
        num_informative = max(2, min(num_features, num_features // 2))
    n_redundant = min(num_redundant, max(0, num_features - num_informative))
    n_repeated = min(num_repeated, max(0, num_features - num_informative - n_redundant))

    X, y = make_classification(
        n_samples=num_samples,
        n_features=num_features,
        n_informative=num_informative,
        n_redundant=n_redundant,
        n_repeated=n_repeated,
        n_classes=num_classes,
        class_sep=class_sep,
        shuffle=True,
        random_state=random_state,
    )
    columns = [f"x{i+1}" for i in range(num_features)]
    df = pd.DataFrame(X, columns=columns)
    df["y"] = y
    extra = f"c{num_classes}_inf{num_informative}_sep{sanitize_float(class_sep)}"
    return df, extra


def generate_regression(num_samples: int,
                        num_features: int,
                        noise: float,
                        bias: float,
                        random_state: Optional[int]) -> Tuple[pd.DataFrame, str]:
    X, y = make_regression(
        n_samples=num_samples,
        n_features=num_features,
        noise=noise,
        bias=bias,
        random_state=random_state,
    )
    columns = [f"x{i+1}" for i in range(num_features)]
    df = pd.DataFrame(X, columns=columns)
    df["y"] = y
    extra = f"noise{sanitize_float(noise)}_bias{sanitize_float(bias)}"
    return df, extra


def generate_clustering(num_samples: int,
                        num_features: int,
                        num_clusters: int,
                        cluster_std: float,
                        center_box_min: float,
                        center_box_max: float,
                        random_state: Optional[int]) -> Tuple[pd.DataFrame, str]:
    centers = num_clusters
    X, y = make_blobs(
        n_samples=num_samples,
        n_features=num_features,
        centers=centers,
        cluster_std=cluster_std,
        center_box=(center_box_min, center_box_max),
        shuffle=True,
        random_state=random_state,
    )
    columns = [f"x{i+1}" for i in range(num_features)]
    df = pd.DataFrame(X, columns=columns)
    df["cluster"] = y
    extra = f"k{num_clusters}_std{sanitize_float(cluster_std)}"
    return df, extra


def maybe_apply_semi_supervised(df: pd.DataFrame,
                                label_column: str,
                                unlabeled_fraction: float,
                                unlabeled_value: str = "") -> pd.DataFrame:
    if unlabeled_fraction <= 0:
        return df
    rng = np.random.default_rng()
    mask = rng.uniform(size=len(df)) < unlabeled_fraction
    df = df.copy()
    df.loc[mask, label_column] = unlabeled_value
    return df


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate synthetic ML datasets (CSV)")
    p.add_argument("--task", choices=["classification", "regression", "clustering"], required=True)
    p.add_argument("--size", choices=["small", "medium", "large"], required=True)
    p.add_argument("--root", default="datasets", help="Root output directory (default: datasets)")

    p.add_argument("--num-samples", type=int, required=True)
    p.add_argument("--num-features", type=int, required=True)
    p.add_argument("--random-state", type=int, default=None)

    # classification-specific
    p.add_argument("--num-classes", type=int, default=2)
    p.add_argument("--num-informative", type=int, default=None)
    p.add_argument("--num-redundant", type=int, default=0)
    p.add_argument("--num-repeated", type=int, default=0)
    p.add_argument("--class-sep", type=float, default=1.0)

    # regression-specific
    p.add_argument("--noise", type=float, default=0.0)
    p.add_argument("--bias", type=float, default=0.0)

    # clustering-specific
    p.add_argument("--num-clusters", type=int, default=3)
    p.add_argument("--cluster-std", type=float, default=1.0)
    p.add_argument("--center-box-min", type=float, default=-10.0)
    p.add_argument("--center-box-max", type=float, default=10.0)

    # semi-supervised
    p.add_argument("--semi-supervised", type=float, default=0.0,
                   help="Fraction of labels to mask (0-1). Applies to y/cluster column.")

    return p.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    out_dir = get_output_dir(root, args.size)

    if args.task == "classification":
        df, extra = generate_classification(
            num_samples=args.num_samples,
            num_features=args.num_features,
            num_informative=args.num_informative,
            num_redundant=args.num_redundant,
            num_repeated=args.num_repeated,
            num_classes=args.num_classes,
            class_sep=args.class_sep,
            random_state=args.random_state,
        )
        label_col = "y"
    elif args.task == "regression":
        df, extra = generate_regression(
            num_samples=args.num_samples,
            num_features=args.num_features,
            noise=args.noise,
            bias=args.bias,
            random_state=args.random_state,
        )
        label_col = "y"
    else:  # clustering
        df, extra = generate_clustering(
            num_samples=args.num_samples,
            num_features=args.num_features,
            num_clusters=args.num_clusters,
            cluster_std=args.cluster_std,
            center_box_min=args.center_box_min,
            center_box_max=args.center_box_max,
            random_state=args.random_state,
        )
        label_col = "cluster"

    if args.semi_supervised > 0:
        df = maybe_apply_semi_supervised(df, label_col, args.semi_supervised)

    filename = make_filename(
        task=args.task,
        num_samples=args.num_samples,
        num_features=args.num_features,
        extra=extra,
        random_state=args.random_state,
    )
    out_path = out_dir / filename
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
