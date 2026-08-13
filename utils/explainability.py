"""Explainability utilities for GridGuard AI."""

import pandas as pd
import streamlit as st
from lime.lime_tabular import LimeTabularExplainer
import shap


CLASS_NAMES = [
    "Critical",
    "Poor",
    "Good",
    "Excellent",
]


@st.cache_resource
def create_lime_explainer(
    reference_data: pd.DataFrame,
) -> LimeTabularExplainer:
    """Create and cache the LIME tabular explainer."""

    return LimeTabularExplainer(
        training_data=reference_data.values,
        feature_names=reference_data.columns.tolist(),
        class_names=CLASS_NAMES,
        mode="classification",
        random_state=42,
    )

def generate_lime_explanation(
    lime_explainer: LimeTabularExplainer,
    model,
    input_data: pd.DataFrame,
    predicted_class: int,
    num_features: int = 10,
):
    """Generate a local LIME explanation for one transformer assessment."""

    if len(input_data) != 1:
        raise ValueError(
            "LIME explanation requires exactly one input row."
        )

    explanation = lime_explainer.explain_instance(
        data_row=input_data.iloc[0].values,
        predict_fn=model.predict_proba,
        labels=[predicted_class],
        num_features=num_features,
    )

    return explanation

def lime_explanation_to_dataframe(
    explanation,
    predicted_class: int,
) -> pd.DataFrame:
    """Convert a LIME explanation into a display-ready DataFrame."""

    lime_items = explanation.as_list(
        label=predicted_class
    )

    explanation_df = pd.DataFrame(
        lime_items,
        columns=[
            "Feature Condition",
            "Contribution",
        ],
    )

    explanation_df["Direction"] = (
        explanation_df["Contribution"]
        .apply(
            lambda value: (
                "Supports prediction"
                if value > 0
                else "Opposes prediction"
            )
        )
    )

    explanation_df["Absolute Contribution"] = (
        explanation_df["Contribution"].abs()
    )

    explanation_df = explanation_df.sort_values(
        by="Absolute Contribution",
        ascending=False,
    ).reset_index(drop=True)

    return explanation_df

@st.cache_resource
def create_shap_explainer(
    _model,
) -> shap.TreeExplainer:
    """Create and cache a SHAP explainer for the XGBoost model."""

    return shap.TreeExplainer(_model)

def generate_shap_explanation(
    shap_explainer,
    input_data: pd.DataFrame,
):
    """Generate a SHAP explanation for one transformer assessment."""

    if len(input_data) != 1:
        raise ValueError(
            "SHAP explanation requires exactly one input row."
        )

    return shap_explainer(input_data)

def shap_explanation_to_dataframe(
    explanation,
    predicted_class_index: int,
    feature_names: list[str],
) -> pd.DataFrame:
    """Convert one multiclass SHAP explanation into a readable table."""

    shap_values = explanation.values

    if shap_values.ndim == 3:
        class_shap_values = shap_values[
            0,
            :,
            predicted_class_index,
        ]
    elif shap_values.ndim == 2:
        class_shap_values = shap_values[0]
    else:
        raise ValueError(
            f"Unexpected SHAP values shape: {shap_values.shape}"
        )

    shap_df = pd.DataFrame(
        {
            "Measurement": feature_names,
            "Impact Score": class_shap_values,
        }
    )

    shap_df["Effect"] = shap_df["Impact Score"].apply(
        lambda value: (
            "🟢 Supports prediction"
            if value > 0
            else "🔴 Opposes prediction"
        )
    )

    shap_df["Absolute Impact"] = (
        shap_df["Impact Score"].abs()
    )

    return (
        shap_df.sort_values(
            by="Absolute Impact",
            ascending=False,
        )
        .reset_index(drop=True)
    )