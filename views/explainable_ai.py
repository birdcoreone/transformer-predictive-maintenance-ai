"""SHAP-based diagnostic explanation for GridGuard AI assessment results.

In v2, explainability is embedded directly within the transformer
assessment result rather than presented as a separate application page.
SHAP is used as the single explanation method for deployed assessments.
"""

import matplotlib.pyplot as plt
import shap
import streamlit as st

from utils.explainability import (
    generate_shap_explanation,
    shap_explanation_to_dataframe,
)


def generate_shap_interpretation(
    shap_df,
    predicted_class: str,
    confidence: float,
) -> str:
    """Create a concise engineering interpretation of SHAP contributions."""

    supporting_features = (
        shap_df[shap_df["Impact Score"] > 0]
        .head(3)["Measurement"]
        .tolist()
    )

    opposing_features = (
        shap_df[shap_df["Impact Score"] < 0]
        .sort_values("Impact Score")
        .head(3)["Measurement"]
        .tolist()
    )

    if supporting_features:
        supporting_text = ", ".join(supporting_features)
    else:
        supporting_text = "no single measurement dominated the prediction"

    if opposing_features:
        opposing_text = ", ".join(opposing_features)
    else:
        opposing_text = "no major measurement strongly opposed the prediction"

    return (
        f"The transformer was classified as **{predicted_class}** with "
        f"**{confidence * 100:.2f}% model confidence**. "
        f"The strongest measurements supporting this classification were "
        f"**{supporting_text}**. Measurements exerting the strongest "
        f"influence away from this classification were **{opposing_text}**. "
        f"These contributions describe how the measured transformer "
        f"conditions influenced the model's assessment."
    )


def _get_predicted_class_index(
    metadata,
    predicted_class: str,
) -> int:
    """Resolve the model class index for the predicted health status."""

    class_mapping = {
        int(class_id): class_name
        for class_id, class_name in metadata["class_mapping"].items()
    }

    return next(
        class_id
        for class_id, class_name in class_mapping.items()
        if class_name == predicted_class
    )


def _create_waterfall_explanation(
    shap_explanation,
    input_data,
    predicted_class_index: int,
):
    """Create a single-class SHAP explanation for the waterfall plot."""

    shap_values = shap_explanation.values
    base_values = shap_explanation.base_values

    if shap_values.ndim == 3:
        selected_shap_values = shap_values[
            0,
            :,
            predicted_class_index,
        ]
        selected_base_value = base_values[
            0,
            predicted_class_index,
        ]

    elif shap_values.ndim == 2:
        selected_shap_values = shap_values[0]

        if hasattr(base_values, "ndim") and base_values.ndim == 2:
            selected_base_value = base_values[
                0,
                predicted_class_index,
            ]
        else:
            selected_base_value = base_values[0]

    else:
        raise ValueError(
            f"Unexpected SHAP values shape: {shap_values.shape}"
        )

    return shap.Explanation(
        values=selected_shap_values,
        base_values=selected_base_value,
        data=input_data.iloc[0].values,
        feature_names=input_data.columns.tolist(),
    )


def render_explanation_section(
    model,
    metadata,
    shap_explainer,
) -> None:
    """Render the SHAP explanation for the current assessment."""

    result = st.session_state["assessment_result"]

    input_data = result["input_data"]
    predicted_class = result["predicted_class"]
    confidence = result["confidence"]

    st.markdown("### Diagnostic Influence Analysis")

    st.write(
        "This section shows which transformer measurements had the "
        "greatest influence on the predicted health condition."
    )

    with st.expander(
        "View measurements used for this assessment",
        expanded=False,
    ):
        st.dataframe(
            input_data.T.rename(columns={0: "Measured Value"}),
            use_container_width=True,
        )

    predicted_class_index = _get_predicted_class_index(
        metadata=metadata,
        predicted_class=predicted_class,
    )

    shap_explanation = generate_shap_explanation(
        shap_explainer=shap_explainer,
        input_data=input_data,
    )

    shap_df = shap_explanation_to_dataframe(
        explanation=shap_explanation,
        predicted_class_index=predicted_class_index,
        feature_names=input_data.columns.tolist(),
    )

    waterfall_explanation = _create_waterfall_explanation(
        shap_explanation=shap_explanation,
        input_data=input_data,
        predicted_class_index=predicted_class_index,
    )

    plot_column, table_column = st.columns(
        [1.35, 1],
        gap="large",
    )

    with plot_column:
        st.markdown("#### Measurement Influence")

        st.caption(
            "Red measurements increased support for the predicted "
            "health class, while blue measurements reduced it."
        )

        fig, _ = plt.subplots(figsize=(10, 7))

        shap.plots.waterfall(
            waterfall_explanation,
            max_display=10,
            show=False,
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

        plt.close(fig)

    with table_column:
        st.markdown("#### Most Influential Measurements")

        st.caption(
            "Measurements ranked by their contribution to this assessment."
        )

        shap_display_df = shap_df[
            [
                "Measurement",
                "Impact Score",
                "Effect",
            ]
        ].head(10).copy()

        shap_display_df["Impact Score"] = (
            shap_display_df["Impact Score"].round(4)
        )

        st.dataframe(
            shap_display_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### Engineering Interpretation")

    interpretation = generate_shap_interpretation(
        shap_df=shap_df,
        predicted_class=predicted_class,
        confidence=confidence,
    )

    st.info(interpretation)

    st.caption(
        "SHAP explanations describe the influence of individual "
        "measurements on the model prediction. They should be considered "
        "alongside standard transformer diagnostic procedures and "
        "professional engineering judgment."
    )