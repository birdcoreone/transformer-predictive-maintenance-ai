"""GridGuard AI application entry point (v2 — engineer-focused)."""

import json

import streamlit as st

from utils.style import apply_global_styles
from views.assessment import render_assessment
from utils.explainability import create_shap_explainer
from utils.loader import (
    load_model_metadata,
    load_simulation_presets,
    load_xgboost_model,
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
# INITIALIZATION
# ---------------------------------------------------------
apply_global_styles()

try:
    metadata = load_model_metadata()
    model = load_xgboost_model()

    shap_explainer = create_shap_explainer(model)

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
# SIDEBAR — identity only. No nav radio, no model name,
# no explainability badge, no system-status theatrics.
# ---------------------------------------------------------
with st.sidebar:
    st.html(
        """
        <div style="padding: 0.5rem 0 1rem 0;">
            <div style="
                color: #f8fafc;
                font-size: 1.4rem;
                font-weight: 800;
                letter-spacing: -0.03em;
            ">
                ⚡ GridGuard AI
            </div>

            <div style="
                margin-top: 0.3rem;
                color: #8ea8bf;
                font-size: 0.8rem;
                line-height: 1.5;
            ">
                Transformer Health Assessment
            </div>
        </div>
        """
    )
    st.divider()
    st.caption("GridGuard AI · Teddy Boamah · KsTU")

# ---------------------------------------------------------
# ENTRY POINT — one flow: input form → result. render_assessment
# internally decides which to show based on session state.
# ---------------------------------------------------------
render_assessment(
    model=model,
    metadata=metadata,
    simulation_presets=simulation_presets,
    shap_explainer=shap_explainer,
)
