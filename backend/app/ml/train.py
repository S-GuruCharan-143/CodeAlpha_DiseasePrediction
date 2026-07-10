"""
Heart Disease Model Training Script

Trains a Random Forest classifier on the Heart Disease dataset
and saves the trained model together with the preprocessing pipeline.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)

logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


def main():

    project_root = get_project_root()

    data_path = project_root / "datasets" / "heart.csv"

    saved_models = project_root / "saved_models"

    if not data_path.exists():
        logger.error("Dataset not found: %s", data_path)
        sys.exit(1)

    logger.info("Loading dataset...")

    df = pd.read_csv(data_path)

    logger.info("Dataset shape: %s", df.shape)

    X = df.drop(columns=["target"])

    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    logger.info("Training samples: %d", len(X_train))
    logger.info("Testing samples : %d", len(X_test))

    numeric_features = list(X.columns)

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                "passthrough",
                numeric_features,
            )
        ]
    )

    X_train_processed = preprocessor.fit_transform(X_train)

    X_test_processed = preprocessor.transform(X_test)

    logger.info("Training Random Forest...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
    )

    model.fit(X_train_processed, y_train)

    predictions = model.predict(X_test_processed)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(y_test, predictions)

    recall = recall_score(y_test, predictions)

    f1 = f1_score(y_test, predictions)

    cm = confusion_matrix(y_test, predictions)

    logger.info("=" * 60)
    logger.info("MODEL EVALUATION")
    logger.info("=" * 60)

    logger.info("Accuracy : %.4f", accuracy)
    logger.info("Precision: %.4f", precision)
    logger.info("Recall   : %.4f", recall)
    logger.info("F1 Score : %.4f", f1)

    logger.info("Confusion Matrix:")
    logger.info("\n%s", cm)

    saved_models.mkdir(exist_ok=True)

    joblib.dump(
        model,
        saved_models / "random_forest_model.joblib",
    )

    joblib.dump(
        preprocessor,
        saved_models / "preprocessing_pipeline.joblib",
    )

    joblib.dump(
        preprocessor,
        saved_models / "preprocessor.joblib",
    )

    logger.info("Model saved successfully.")

    logger.info("Training complete.")


if __name__ == "__main__":
    main()