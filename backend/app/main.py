"""
FastAPI application entry point.

Creates and configures the ASGI application with:
- Project metadata (title, version)
- CORS middleware
- API router registration
- Startup event for model loading
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.predict import router as predict_router
from .core.config import CORS_ORIGINS, PROJECT_NAME, VERSION
from .ml.model_loader import ModelManager

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Application lifespan (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle application startup and shutdown events.

    On startup the model and preprocessor are loaded into memory.
    If the artefact files are missing (e.g. model hasn't been trained yet),
    a warning is logged but the server still starts so the health endpoint
    remains reachable.
    """
    # ---- Startup ----------------------------------------------------------
    logger.info("Starting %s v%s …", PROJECT_NAME, VERSION)

    try:
        ModelManager.load_model()
        logger.info("✅  Model loaded successfully.")
    except FileNotFoundError:
        logger.warning(
            "⚠️  Model file not found – the /predict endpoint will return 503 "
            "until the model is trained and the server is restarted."
        )
    except RuntimeError as exc:
        logger.error("❌  Failed to load model: %s", exc)

    try:
        ModelManager.load_preprocessor()
        logger.info("✅  Preprocessor loaded successfully.")
    except FileNotFoundError:
        logger.warning(
            "⚠️  Preprocessor file not found – the /predict endpoint will "
            "return 503 until the preprocessor is available."
        )
    except RuntimeError as exc:
        logger.error("❌  Failed to load preprocessor: %s", exc)

    yield  # Application is running

    # ---- Shutdown ---------------------------------------------------------
    logger.info("Shutting down %s …", PROJECT_NAME)


# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=(
        "REST API for predicting credit risk using a trained "
        "Random Forest model on the German Credit dataset."
    ),
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Router registration
# ---------------------------------------------------------------------------
app.include_router(predict_router)
