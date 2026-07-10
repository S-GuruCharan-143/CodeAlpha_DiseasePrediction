"""
Prediction service layer.

Runs preprocessing, model inference, and maps the result
to a DiseasePrediction response.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..ml.model_loader import ModelManager
from ..ml.preprocess import preprocess_input
from ..schemas.disease import DiseaseInput, DiseasePrediction


def predict_disease(input_data: DiseaseInput) -> DiseasePrediction:
    """
    Run the complete prediction pipeline for one patient.
    """

    # Convert validated input into a DataFrame
    raw_df: pd.DataFrame = preprocess_input(input_data)

    # Load cached preprocessing pipeline and model
    preprocessor = ModelManager.get_preprocessor()
    model = ModelManager.get_model()

    # Transform features
    transformed: np.ndarray = preprocessor.transform(raw_df)

    # Predict class and probabilities
    prediction_array: np.ndarray = model.predict(transformed)
    probability_array: np.ndarray = model.predict_proba(transformed)

    predicted_class: int = int(prediction_array[0])

    # Target convention:
    # 0 -> Healthy
    # 1 -> Heart Disease
    prediction_label = (
        "Heart Disease"
        if predicted_class == 1
        else "Healthy"
    )

    confidence: float = float(
        probability_array[0][predicted_class]
    )

    risk = (
        "High"
        if predicted_class == 1
        else "Low"
    )

    return DiseasePrediction(
        prediction=prediction_label,
        confidence=round(confidence, 4),
        risk=risk,
    )