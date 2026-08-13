"""Transformer assessment page for GridGuard AI."""

from typing import Any

import pandas as pd
import streamlit as st
import xgboost as xgb

from utils.predictor import (
    create_input_dataframe,
    get_maintenance_guidance,
    normalize_class_mapping,
    predict_transformer_health,
)


FALLBACK_FEATURE_NAMES = [
    "Hydrogen",
    "Oxygen",
    "Nitrogen",
    "Methane",
    "CO",
    "CO2",
    "Ethylene",
    "Ethane",
    "Acetylene",
    "DBDS",
    "Power_factor",
    "Interfacial_V",
    "Dielectric_rigidity",
    "Water_content",
]


DISPLAY_NAMES = {
    "Hydrogen": "Hydrogen",
    "Oxygen": "Oxygen",
    "Nitrogen": "Nitrogen",
    "Methane": "Methane",
    "CO": "Carbon Monoxide",
    "CO2": "Carbon Dioxide",
    "Ethylene": "Ethylene",
    "Ethane": "Ethane",
    "Acetylene": "Acetylene",
    "DBDS": "DBDS",
    "Power_factor": "Power Factor",
    "Interfacial_V": "Interfacial Voltage",
    "Dielectric_rigidity": "Dielectric Rigidity",
    "Water_content": "Water Content",
}


DGA_FEATURES = [
    "Hydrogen",
    "Oxygen",
    "Nitrogen",
    "Methane",
    "CO",
    "CO2",
    "Ethylene",
    "Ethane",
    "Acetylene",
]


OIL_FEATURES = [
    "DBDS",
    "Power_factor",
    "Interfacial_V",
    "Dielectric_rigidity",
    "Water_content",
]


STATUS_ICONS = {
    "Critical": "🔴",
    "Poor": "🟠",
    "Good": "🔵",
    "Excellent": "🟢",
}


STATUS_MESSAGES = {
    "Critical": (
        "Severe deterioration or fault indicators were detected. "
        "Immediate engineering attention is recommended."
    ),
    "Poor": (
        "The transformer shows signs of deterioration that require "
        "closer investigation and planned maintenance."
    ),
    "Good": (
        "The transformer is operating in generally acceptable "
        "condition, although continued monitoring is required."
    ),
    "Excellent": (
        "The transformer measurements indicate a healthy condition "
        "under the trained model."
    ),
}


def _render_feature_inputs(
    features: list[str],
    prefix: str,
) -> dict[str, float]:
    """Render numeric inputs for a feature group."""

    values: dict[str, float] = {}
    

    columns = st.columns(2)

    for index, feature in enumerate(features):
        with columns[index % 2]:
            values[feature] = st.number_input(
                label=DISPLAY_NAMES.get(feature, feature),
                min_value=0.0,
                step=0.01,
                format="%.4f",
                key=f"{prefix}_{feature}",
                help=(
                    f"Enter the measured value for "
                    f"{DISPLAY_NAMES.get(feature, feature)}."
                ),
            )

    return values


def _render_probability_results(
    probabilities: dict[str, float],
) -> None:
    """Display model probabilities for all health classes."""

    st.markdown("### Class Probability Distribution")

    ordered_classes = [
        "Critical",
        "Poor",
        "Good",
        "Excellent",
    ]

    probability_columns = st.columns(4)

    for column, class_name in zip(
        probability_columns,
        ordered_classes,
    ):
        probability = probabilities.get(class_name, 0.0)

        with column:
            st.metric(
                label=class_name,
                value=f"{probability * 100:.2f}%",
            )

            st.progress(
                min(
                    max(probability, 0.0),
                    1.0,
                )
            )


def _render_input_summary(
    input_data: pd.DataFrame,
) -> None:
    """Display the submitted measurements."""

    with st.expander(
        "View submitted diagnostic measurements",
        expanded=False,
    ):
        display_data = input_data.rename(
            columns=DISPLAY_NAMES
        )

        st.dataframe(
            display_data.T.rename(
                columns={0: "Measured Value"}
            ),
            use_container_width=True,
        )


def _apply_simulation_preset(
    simulation_presets: dict[str, Any],
) -> None:
    """Load the selected preset into the input widgets."""

    selected_preset = st.session_state.get(
        "simulation_mode",
        "Manual Entry",
    )

    selected_values = simulation_presets.get(
        selected_preset,
        {},
    )

    for feature in DGA_FEATURES:
        st.session_state[f"dga_{feature}"] = float(
            selected_values.get(feature, 0.0)
        )

    for feature in OIL_FEATURES:
        st.session_state[f"oil_{feature}"] = float(
            selected_values.get(feature, 0.0)
        )

    st.session_state.pop(
        "assessment_result",
        None,
    )

def render_assessment(
    model: xgb.XGBClassifier,
    metadata: dict[str, Any],
    simulation_presets: dict[str, Any],
) -> None:
    """Render the interactive transformer assessment page."""

    preset_options = list(simulation_presets.keys())

    st.selectbox(
        "🧪 Simulation Mode",
        options=preset_options,
        key="simulation_mode",
        on_change=_apply_simulation_preset,
        args=(simulation_presets,),
        help=(
            "Choose a verified transformer example "
            "or enter values manually."
        ),
    )

    if "_simulation_inputs_initialized" not in st.session_state:
        _apply_simulation_preset(simulation_presets)

        st.session_state[
            "_simulation_inputs_initialized"
        ] = True

    st.caption(
        "LIVE MODEL INFERENCE · CONDITION-BASED MAINTENANCE"
    )

    st.title("⚡ Transformer Assessment")

    st.write(
        """
        Enter the latest dissolved-gas and oil-quality measurements.
        GridGuard AI will classify the transformer as Critical, Poor,
        Good or Excellent and present the model's confidence across
        all four health classes.
        """
    )

    st.info(
        "Use measurements produced by an appropriate laboratory or "
        "transformer diagnostic process. The system is a decision-support "
        "prototype and should not replace professional engineering judgment."
    )

    feature_names = metadata.get(
        "feature_names",
        FALLBACK_FEATURE_NAMES,
    )

    class_mapping = normalize_class_mapping(
        metadata.get("class_mapping")
    )

    with st.form("transformer_assessment_form"):
        dga_tab, oil_tab = st.tabs(
            [
                "Dissolved Gas Analysis",
                "Oil-Quality Indicators",
            ]
        )

        with dga_tab:
            st.markdown("#### Dissolved Gas Measurements")

            st.caption(
                "Enter the measured gas concentrations using the "
                "same units applied in the training dataset."
            )

            dga_values = _render_feature_inputs(
                DGA_FEATURES,
                prefix="dga",
            )

        with oil_tab:
            st.markdown("#### Oil-Quality Measurements")

            st.caption(
                "Enter the latest transformer-oil condition values."
            )

            oil_values = _render_feature_inputs(
                OIL_FEATURES,
                prefix="oil",
            )

        st.markdown("---")

        submit_assessment = st.form_submit_button(
            "⚡ Analyze Transformer",
            type="primary",
            use_container_width=True,
        )

    if submit_assessment:
        feature_values = {
            **dga_values,
            **oil_values,
        }

        try:
            input_data = create_input_dataframe(
                feature_values=feature_values,
                feature_names=feature_names,
            )

            result = predict_transformer_health(
                model=model,
                input_data=input_data,
                class_mapping=class_mapping,
            )

            st.session_state["assessment_result"] = result

        except Exception as error:
            st.error(
                "The transformer assessment could not be completed."
            )
            st.exception(error)

    result = st.session_state.get("assessment_result")

    if result is None:
        st.caption(
            "Complete the measurements above and select "
            "'Analyze Transformer' to generate an assessment."
        )
        return

    predicted_class = result["predicted_class"]
    confidence = result["confidence"]
    status_icon = STATUS_ICONS.get(
        predicted_class,
        "⚪",
    )

    st.divider()

    st.markdown("## Assessment Result")

    result_left, result_right = st.columns(
        [1.4, 2.6],
        vertical_alignment="center",
    )

    with result_left:
        with st.container(border=True):
            st.caption("PREDICTED HEALTH STATUS")

            st.markdown(
                f"# {status_icon} {predicted_class}"
            )

            st.metric(
                label="Model Confidence",
                value=f"{confidence * 100:.2f}%",
            )

    with result_right:
        with st.container(border=True):
            st.markdown("#### Condition Interpretation")

            st.write(
                STATUS_MESSAGES.get(
                    predicted_class,
                    "Review the generated assessment.",
                )
            )

    _render_probability_results(
        result["probabilities"]
    )

    st.markdown("### Recommended Maintenance Response")

    with st.container(border=True):
        for recommendation in get_maintenance_guidance(
            predicted_class
        ):
            st.markdown(f"- {recommendation}")

    _render_input_summary(
        result["input_data"]
    )