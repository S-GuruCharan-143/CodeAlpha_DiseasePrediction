"""
Credit Scoring Model Training Script

Trains a Random Forest Classifier on the German Credit Dataset
and saves the model and preprocessor for inference.

Usage:
    python scripts/train.py
"""

import os
import sys

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib


def get_project_root():
    """Get the project root directory (parent of scripts/)."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def load_data(data_path):
    """
    Load the German Credit Dataset from CSV.

    Args:
        data_path: Path to the CSV file.

    Returns:
        pandas DataFrame with the raw dataset.
    """
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    return df


def preprocess_data(df):
    """
    Handle missing values and prepare features and target.

    - Fills NaN in 'Saving accounts' and 'Checking account' with 'unknown'.
    - Maps the 'Risk' column to binary: good -> 1, bad -> 0.

    Args:
        df: Raw DataFrame.

    Returns:
        X (features DataFrame), y (target Series).
    """
    # Handle missing values
    df["Saving accounts"] = df["Saving accounts"].fillna("unknown")
    df["Checking account"] = df["Checking account"].fillna("unknown")

    print(f"\nMissing values after filling:")
    print(df.isnull().sum())

    # Separate features and target
    X = df.drop("Risk", axis=1)
    y = df["Risk"].map({"good": 1, "bad": 0})

    print(f"\nFeatures shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")

    return X, y


def build_preprocessor(numerical_features, categorical_features):
    """
    Build a ColumnTransformer preprocessor.

    - StandardScaler for numerical features.
    - OneHotEncoder for categorical features.

    Args:
        numerical_features: List of numerical column names.
        categorical_features: List of categorical column names.

    Returns:
        Fitted ColumnTransformer instance.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
        ]
    )
    return preprocessor


def train_model(X_train_transformed, y_train):
    """
    Train a Random Forest Classifier.

    Args:
        X_train_transformed: Preprocessed training features.
        y_train: Training target values.

    Returns:
        Fitted RandomForestClassifier.
    """
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train_transformed, y_train)
    print("Training complete.")
    return model


def evaluate_model(model, X_test_transformed, y_test):
    """
    Evaluate the trained model on test data.

    Prints accuracy, classification report, and confusion matrix.

    Args:
        model: Trained classifier.
        X_test_transformed: Preprocessed test features.
        y_test: Test target values.
    """
    y_pred = model.predict(X_test_transformed)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n{'='*50}")
    print(f"Model Evaluation Results")
    print(f"{'='*50}")
    print(f"Accuracy: {accuracy:.4f}")

    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["bad (0)", "good (1)"]))

    print(f"Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print(f"  [TN={cm[0][0]}, FP={cm[0][1]}]")
    print(f"  [FN={cm[1][0]}, TP={cm[1][1]}]")


def save_artifacts(preprocessor, model, save_dir):
    """
    Save the fitted preprocessor and model to disk.

    Args:
        preprocessor: Fitted ColumnTransformer.
        model: Fitted RandomForestClassifier.
        save_dir: Directory to save the .joblib files.
    """
    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Save the preprocessor
    preprocessor_path = os.path.join(save_dir, "preprocessor.joblib")
    joblib.dump(preprocessor, preprocessor_path)
    print(f"\nPreprocessor saved to: {preprocessor_path}")

    # Save the model
    model_path = os.path.join(save_dir, "random_forest_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to:        {model_path}")


def main():
    """Main training pipeline."""
    # ── Resolve paths relative to project root ──────────────────────────
    project_root = get_project_root()
    data_path = os.path.join(project_root, "datasets", "german_credit_data.csv")
    save_dir = os.path.join(project_root, "saved_models")

    print(f"Project root: {project_root}")
    print(f"{'='*50}")
    print(f"Credit Scoring Model Training")
    print(f"{'='*50}\n")

    # ── 1. Load data ────────────────────────────────────────────────────
    if not os.path.exists(data_path):
        print(f"ERROR: Dataset not found at {data_path}")
        print("Please ensure 'datasets/german_credit_data.csv' exists.")
        sys.exit(1)

    df = load_data(data_path)

    # ── 2. Preprocess data ──────────────────────────────────────────────
    X, y = preprocess_data(df)

    # Define feature groups
    numerical_features = ["Age", "Job", "Credit amount", "Duration"]
    categorical_features = [
        "Sex",
        "Housing",
        "Saving accounts",
        "Checking account",
        "Purpose",
    ]

    # ── 3. Split data ──────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain set size: {X_train.shape[0]}")
    print(f"Test set size:  {X_test.shape[0]}")

    # ── 4. Build and fit preprocessor ──────────────────────────────────
    preprocessor = build_preprocessor(numerical_features, categorical_features)
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    print(f"Transformed feature count: {X_train_transformed.shape[1]}")

    # ── 5. Train model ─────────────────────────────────────────────────
    model = train_model(X_train_transformed, y_train)

    # ── 6. Evaluate model ──────────────────────────────────────────────
    evaluate_model(model, X_test_transformed, y_test)

    # ── 7. Save artifacts ──────────────────────────────────────────────
    save_artifacts(preprocessor, model, save_dir)

    print(f"\n{'='*50}")
    print("Training pipeline complete!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
