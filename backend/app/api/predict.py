"""
API route definitions for the credit scoring service.

Endpoints
---------
GET  /         → Welcome message
GET  /health   → Health check (includes model-loaded status)
POST /predict  → Credit risk prediction
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from ..ml.model_loader import ModelManager
from ..schemas.disease import DiseaseInput, DiseasePrediction
from ..services.prediction import predict_disease

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# GET /  — Welcome
# ---------------------------------------------------------------------------
@router.get("/", summary="Welcome", tags=["General"])
async def root() -> dict[str, str]:
    """Return a simple welcome message."""
    return {"message": "Welcome to the Credit Scoring API 🚀"}


# ---------------------------------------------------------------------------
# GET /health  — Health check
# ---------------------------------------------------------------------------
@router.get("/health", summary="Health Check", tags=["General"])
async def health_check() -> dict[str, object]:
    """Report service health and whether the ML model is loaded."""
    return {
        "status": "healthy",
        "model_loaded": ModelManager.is_model_loaded(),
        "preprocessor_loaded": ModelManager.is_preprocessor_loaded(),
    }


# ---------------------------------------------------------------------------
# POST /predict  — Credit risk prediction
# ---------------------------------------------------------------------------
@router.post(
    "/predict",
    response_model=DiseasePrediction,
    summary="Predict Heart Disease",
    tags=["Prediction"],
)
async def predict(input_data: DiseaseInput) -> DiseasePrediction:
    """Accept applicant data and return a credit risk prediction.

    Returns a JSON object with the prediction label, confidence
    score, and human-readable risk level.
    """
    try:
        result: DiseasePrediction = predict_disease(input_data)
        logger.info(
            "Prediction completed — result=%s, confidence=%.4f",
            result.prediction,
            result.confidence,
        )
        return result

    except RuntimeError as exc:
        # Model / preprocessor not loaded
        logger.error("Runtime error during prediction: %s", exc)
        raise HTTPException(
            status_code=503,
            detail=f"Model service unavailable: {exc}",
        ) from exc

    except ValueError as exc:
        # Data transformation issues
        logger.error("Value error during prediction: %s", exc)
        raise HTTPException(
            status_code=422,
            detail=f"Input processing error: {exc}",
        ) from exc

    except Exception as exc:
        # Catch-all for unexpected errors
        logger.exception("Unexpected error during prediction.")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {exc}",
        ) from exc
