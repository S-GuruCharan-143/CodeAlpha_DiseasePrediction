"""
Application configuration module.

Defines project-wide settings including project metadata,
model file paths, and CORS configuration.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Project metadata
# ---------------------------------------------------------------------------
PROJECT_NAME: str = "Credit Scoring API"
VERSION: str = "1.0.0"

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------
# Resolve the project root directory (CreditScoring/).
# Structure: backend/app/core/config.py → 4 levels up to reach project root.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent

# Paths to the serialised model artefacts produced during training.
MODEL_PATH: Path = PROJECT_ROOT / "saved_models" / "random_forest_model.joblib"
PREPROCESSOR_PATH: Path = PROJECT_ROOT / "saved_models" / "preprocessing_pipeline.joblib"

# ---------------------------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------------------------
# Origins allowed to make cross-origin requests (Vite dev server by default).
CORS_ORIGINS: list[str] = ["http://localhost:5173"]
