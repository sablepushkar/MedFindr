"""
Train a basic Explainable Boosting Machine for MedFindr.
Improved feature set for better practical value.

Usage:
    python scripts/train_ebm.py
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from interpret.glassbox import ExplainableBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

ROOT = Path(__file__).parent.parent
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "ebm_urgency_model.pkl"


def create_training_data(n_samples: int = 600) -> pd.DataFrame:
    """Generate improved synthetic data with more useful features."""
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n_samples):
        has_chest = rng.integers(0, 2)
        has_breathing = rng.integers(0, 2)
        has_fever = rng.integers(0, 2)
        has_severe = rng.integers(0, 2)
        has_neuro = rng.integers(0, 2)
        has_bleeding = rng.integers(0, 2)
        has_vomit = rng.integers(0, 2)
        has_dizziness = rng.integers(0, 2)
        duration_days = rng.integers(1, 14)
        text_length = rng.integers(3, 45)

        score = (
            has_chest * 4 +
            has_breathing * 4 +
            has_neuro * 4 +
            has_bleeding * 3 +
            has_severe * 2 +
            has_fever * 1 +
            has_vomit * 1 +
            has_dizziness * 1
        )

        if score >= 6:
            label = 2  # high
        elif score >= 3:
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
            "has_vomit": has_vomit,
            "has_dizziness": has_dizziness,
            "duration_days": duration_days,
            "text_length": text_length,
            "label": label,
        })

    return pd.DataFrame(rows)


def main():
    print("Generating improved training data...")
    df = create_training_data(600)

    feature_cols = [
        "has_chest_pain", "has_breathing", "has_fever", "has_severe",
        "has_neuro", "has_bleeding", "has_vomit", "has_dizziness",
        "duration_days", "text_length"
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
        outer_bags=6,
        learning_rate=0.01,
        max_rounds=350,
        min_samples_leaf=3,
        max_leaves=3,
    )

    ebm.fit(X_train, y_train)

    print("\nHold-out performance:")
    preds = ebm.predict(X_test)
    print(classification_report(y_test, preds, target_names=["low", "moderate", "high"]))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(ebm, MODEL_PATH)
    print(f"\nModel saved → {MODEL_PATH}")
    print("Restart the Streamlit app to use the new model.")


if __name__ == "__main__":
    main()
