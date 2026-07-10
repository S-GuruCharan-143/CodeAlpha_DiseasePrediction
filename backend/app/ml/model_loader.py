"""
Model loading and lifecycle management.

Provides a singleton-based ModelManager that lazily loads the trained
Random Forest model and its associated preprocessor from disk using joblib.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib

from ..core.config import MODEL_PATH, PREPROCESSOR_PATH

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singletons — populated by load_*() functions
# ---------------------------------------------------------------------------
_model: Any | None = None
_preprocessor: Any | None = None


class ModelManager:
    """Handles loading, caching, and retrieval of ML artefacts."""

    # ----- loaders ---------------------------------------------------------

    @staticmethod
    def load_model() -> Any:
        """Load the trained model from *MODEL_PATH* and cache it.

        Returns
        -------
        Any
            The deserialised scikit-learn model object.

        Raises
        ------
        FileNotFoundError
            If the model file does not exist at the configured path.
        RuntimeError
            If joblib fails to deserialise the file.
        """
        global _model

        if not Path(MODEL_PATH).is_file():
            raise FileNotFoundError(
                f"Model file not found at '{MODEL_PATH}'. "
                "Please train the model first."
            )

        try:
            _model = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully from '%s'.", MODEL_PATH)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load model from '{MODEL_PATH}': {exc}"
            ) from exc

        return _model

    @staticmethod
    def load_preprocessor() -> Any:
        """Load the fitted preprocessor from *PREPROCESSOR_PATH* and cache it.

        Returns
        -------
        Any
            The deserialised scikit-learn preprocessor pipeline.

        Raises
        ------
        FileNotFoundError
            If the preprocessor file does not exist at the configured path.
        RuntimeError
            If joblib fails to deserialise the file.
        """
        global _preprocessor

        if not Path(PREPROCESSOR_PATH).is_file():
            raise FileNotFoundError(
                f"Preprocessor file not found at '{PREPROCESSOR_PATH}'. "
                "Please train the model first."
            )

        try:
            _preprocessor = joblib.load(PREPROCESSOR_PATH)
            logger.info(
                "Preprocessor loaded successfully from '%s'.",
                PREPROCESSOR_PATH,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load preprocessor from '{PREPROCESSOR_PATH}': {exc}"
            ) from exc

        return _preprocessor

    # ----- accessors -------------------------------------------------------

    @staticmethod
    def get_model() -> Any:
        """Return the cached model, raising if it hasn't been loaded yet.

        Returns
        -------
        Any
            The scikit-learn model object.

        Raises
        ------
        RuntimeError
            If the model has not been loaded via ``load_model()``.
        """
        if _model is None:
            raise RuntimeError(
                "Model is not loaded. Call ModelManager.load_model() first."
            )
        return _model

    @staticmethod
    def get_preprocessor() -> Any:
        """Return the cached preprocessor, raising if it hasn't been loaded yet.

        Returns
        -------
        Any
            The scikit-learn preprocessor pipeline object.

        Raises
        ------
        RuntimeError
            If the preprocessor has not been loaded via ``load_preprocessor()``.
        """
        if _preprocessor is None:
            raise RuntimeError(
                "Preprocessor is not loaded. "
                "Call ModelManager.load_preprocessor() first."
            )
        return _preprocessor

    # ----- convenience -----------------------------------------------------

    @staticmethod
    def is_model_loaded() -> bool:
        """Return *True* if the model singleton is populated."""
        return _model is not None

    @staticmethod
    def is_preprocessor_loaded() -> bool:
        """Return *True* if the preprocessor singleton is populated."""
        return _preprocessor is not None
