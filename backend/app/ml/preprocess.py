"""
Input preprocessing utilities.

Converts a validated DiseaseInput Pydantic model into a single-row
pandas DataFrame ready for the saved scikit-learn preprocessor pipeline.
"""

from __future__ import annotations

import pandas as pd

from ..schemas.disease import DiseaseInput


def preprocess_input(data: DiseaseInput) -> pd.DataFrame:
    """Convert a DiseaseInput instance to a single-row DataFrame.

    The column names and order must match those used during
    model training.

    Parameters
    ----------
    data : DiseaseInput
        Validated request body from the frontend.

    Returns
    -------
    pd.DataFrame
        A one-row DataFrame containing the patient features.
    """
    row = data.model_dump()
    return pd.DataFrame([row])