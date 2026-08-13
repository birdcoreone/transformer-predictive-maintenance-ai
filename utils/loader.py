"""Resource-loading utilities for GridGuard AI."""

import json
from pathlib import Path
from typing import Any
import streamlit as st
import xgboost as xgb
import joblib
import pandas as pd



BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "smote_xgboost.json"
METADATA_PATH = MODEL_DIR / "model_metadata.json"
PRESET_PATH = MODEL_DIR / "simulation_presets.json"
SHAP_EXPLAINER_PATH = MODEL_DIR / "shap_explainer.pkl"
LIME_REFERENCE_PATH = MODEL_DIR / "lime_reference_data.csv"


@st.cache_resource
def load_xgboost_model() -> xgb.XGBClassifier:
    """Load the trained XGBoost classifier."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)

    return model


@st.cache_data
def load_model_metadata() -> dict[str, Any]:
    """Load the model metadata JSON file."""

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_PATH}"
        )

    with METADATA_PATH.open(
        mode="r",
        encoding="utf-8",
    ) as metadata_file:
        return json.load(metadata_file)

@st.cache_data
def load_simulation_presets() -> dict:
    """Load simulation presets."""

    if not PRESET_PATH.exists():
        return {}

    with PRESET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)

@st.cache_resource
def load_shap_explainer():
    """Load and cache the saved SHAP explainer."""

    if not SHAP_EXPLAINER_PATH.exists():
        raise FileNotFoundError(
            f"SHAP explainer not found: {SHAP_EXPLAINER_PATH}"
        )

    return joblib.load(SHAP_EXPLAINER_PATH)

@st.cache_data
def load_lime_reference_data() -> pd.DataFrame:
    """Load and cache the reference data used by LIME."""

    if not LIME_REFERENCE_PATH.exists():
        raise FileNotFoundError(
            f"LIME reference data not found: {LIME_REFERENCE_PATH}"
        )

    return pd.read_csv(LIME_REFERENCE_PATH)