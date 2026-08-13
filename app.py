"""GridGuard AI application entry point."""

import json
from pathlib import Path
from typing import Any
import streamlit as st
from views.home import render_home
from utils.style import apply_global_styles
from views.assessment import render_assessment
from utils.explainability import create_shap_explainer
from views.explainable_ai import render_explainable_ai
from views.about_developer import render_about_developer
from utils.loader import (
    load_lime_reference_data,
    load_model_metadata,
    load_simulation_presets,
    load_xgboost_model
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="GridGuard AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
METADATA_PATH = BASE_DIR / "models" / "model_metadata.json"


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_metadata() -> dict[str, Any]:
    """Load model metadata from the models directory."""

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata file was not found at: {METADATA_PATH}"
        )

    with METADATA_PATH.open(
        mode="r",
        encoding="utf-8",
    ) as metadata_file:
        return json.load(metadata_file)


# ---------------------------------------------------------
# PLACEHOLDER PAGE
# ---------------------------------------------------------
def render_placeholder(
    title: str,
    description: str,
) -> None:
    """Render a temporary page while development continues."""

    st.title(title)

    st.html(
        f"""
        <div class="glass-panel">
            <div class="panel-title">
                Module under construction
            </div>

            <div class="panel-copy">
                {description}
            </div>
        </div>
        """
    )
# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
apply_global_styles()

try:
    metadata = load_model_metadata()
    model = load_xgboost_model()

    shap_explainer = create_shap_explainer(model)
    lime_reference_data = load_lime_reference_data()

    simulation_presets = load_simulation_presets()
except (
    FileNotFoundError,
    json.JSONDecodeError,
    ValueError,
) as error:
    st.error(
        "GridGuard AI could not initialize its intelligence engine."
    )
    st.exception(error)
    st.stop()


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.html(
        """
        <div style="padding: 0.5rem 0 1rem 0;">
            <div style="
                color: #f8fafc;
                font-size: 1.55rem;
                font-weight: 850;
                letter-spacing: -0.03em;
            ">
                ⚡ GridGuard AI
            </div>

            <div style="
                margin-top: 0.35rem;
                color: #8ea8bf;
                font-size: 0.82rem;
                line-height: 1.5;
            ">
                Transformer Health Intelligence System
            </div>
        </div>
        """
    )
    st.divider()

    selected_page = st.radio(
        label="Navigation",
        options=[
            "🏠 Home",
            "⚡ Transformer Assessment",
            "🧠 Explainable AI",
            "📈 Model Insights",
            "👤 About Developer",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.success("● Intelligence Engine Online")

    st.caption("ACTIVE MODEL")

    st.markdown(
        f"**{metadata.get('model_name', 'SMOTE XGBoost')}**"
    )

    st.caption("EXPLAINABILITY")

    st.markdown("**SHAP + LIME**")


# ---------------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------------
if selected_page == "🏠 Home":
    render_home(metadata)

elif selected_page == "⚡ Transformer Assessment":
    render_assessment(
        model=model,
        metadata=metadata,
        simulation_presets=simulation_presets
    )

elif selected_page == "🧠 Explainable AI":
    render_explainable_ai(
        model=model,
        metadata=metadata,
        shap_explainer=shap_explainer,
        lime_reference_data=lime_reference_data,
    )

elif selected_page == "📈 Model Insights":
    render_placeholder(
        "📈 Model Insights",
        "This module will present evaluation metrics, the "
        "confusion matrix and dataset characteristics.",
    )

elif selected_page == "👤 About Developer":
    render_about_developer()