"""
Train a basic Explainable Boosting Machine for MedFindr urgency/risk.
Version: V09.1a

Run this script once to create models/ebm_urgency_model.pkl

Usage:
    python scripts/train_ebm.py
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Paths
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "ebm_urgency_model.pkl"
EVAL_PATH = DATA_DIR / "evaluation_set.json"


def create_synthetic_data(n_samples: int = 400) -> pd.DataFrame:
    """Generate simple synthetic data aligned with our urgency categories."""
    rng = np.random.default_rng(42)

    rows = []
    for _ in range(n_samples):
        # Random feature profile
        has_chest = rng.integers(0, 2)
        has_breathing = rng.integers(0, 2)
        has_fever = rng.integers(0, 2)
        has_severe = rng.integers(0, 2)
        has_neuro = rng.integers(0, 2)
        has_bleeding = rng.integers(0, 2)
        text_length = rng.integers(3, 40)

        # Simple rule to assign label (so the model has something to learn)
        score = (
            has_chest * 3 +
            has_breathing * 3 +
            has_neuro * 3 +
            has_bleeding * 2 +
            has_severe * 2 +
            has_fever * 1
        )

        if score >= 5:
            label = 2  # high
        elif score >= 2:
            label = 1  # moderate
        else:
            label = 0  # low

        rows.append({
            "has_chest_pain": has_chest,
            "has_breathing": has_breathing,
            "has_fever": has_fever,
            "has_severe": has_severe,
            "has_neuro": has_neuro,
            "has_bleeding": has_bleeding,
            "text_length": text_length,
            "label": label,
        })

    return pd.DataFrame(rows)


def main():
    print("Creating synthetic training data...")
    df = create_synthetic_data(500)

    feature_cols = [
        "has_chest_pain", "has_breathing", "has_fever",
        "has_severe", "has_neuro", "has_bleeding", "text_length"
    ]
    X = df[feature_cols]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Explainable Boosting Machine...")
    ebm = ExplainableBoostingClassifier(
        random_state=42,
        max_bins=64,
        max_interaction_bins=32,
        outer_bags=4,
        inner_bags=0,
        learning_rate=0.01,
        max_rounds=300,
        min_samples_leaf=3,
        max_leaves=3,
    )

    ebm.fit(X_train, y_train)

    print("\nEvaluation on hold-out set:")
    preds = ebm.predict(X_test)
    print(classification_report(y_test, preds, target_names=["low", "moderate", "high"]))

    # Save
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(ebm, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")
    print("You can now restart the Streamlit app – it will use the trained model.")


if __name__ == "__main__":
    main()
