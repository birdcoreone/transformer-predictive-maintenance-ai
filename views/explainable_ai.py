"""Explainable AI page for GridGuard AI."""

import streamlit as st
import matplotlib.pyplot as plt
import shap

from utils.explainability import (
    create_lime_explainer,
    generate_lime_explanation,
    generate_shap_explanation,
    lime_explanation_to_dataframe,
    shap_explanation_to_dataframe,
)

def generate_shap_interpretation(
    shap_df,
    predicted_class: str,
    confidence: float,
) -> str:
    """Create a plain-language summary of the SHAP explanation."""

    supporting_features = (
        shap_df[shap_df["Impact Score"] > 0]
        .head(3)["Measurement"]
        .tolist()
    )

    opposing_features = (
        shap_df[shap_df["Impact Score"] < 0]
        .head(3)["Measurement"]
        .tolist()
    )

    supporting_text = (
        ", ".join(supporting_features)
        if supporting_features
        else "no individual measurement strongly supported the prediction"
    )

    opposing_text = (
        ", ".join(opposing_features)
        if opposing_features
        else "no major measurement opposed the prediction"
    )

    return (
        f"The AI model classified this transformer as "
        f"**{predicted_class}** with an overall confidence of "
        f"**{confidence * 100:.2f}%**. "

        f"The measurements with the greatest positive influence "
        f"on this prediction were **{supporting_text}**. "

        f"The measurements that reduced the prediction score "
        f"were **{opposing_text}**. "

        f"These SHAP contributions provide a transparent explanation "
        f"of how the model reached its prediction for this "
        f"transformer assessment."
    )


def render_explainable_ai(
    model,
    metadata,
    shap_explainer,
    lime_reference_data,
):
    """Render explanations for the latest transformer assessment."""
   

    st.title("Explainable AI")

    st.caption(
        "Understand the factors that influenced the latest "
        "transformer health prediction."
        
    )

    result = st.session_state.get("assessment_result")

    if result is None:
        st.warning(
            "No transformer assessment is available. "
            "Please complete an assessment first."
        )
        return

    input_data = result["input_data"]
    predicted_class = result["predicted_class"]
    confidence = result["confidence"]

    st.success(
        "The latest transformer assessment has been loaded "
        "successfully."
    )

    summary_left, summary_right = st.columns(2)

    with summary_left:
        st.metric(
            label="Latest Predicted Health Status",
            value=predicted_class,
        )

    with summary_right:
        st.metric(
            label="Model Confidence",
            value=f"{confidence * 100:.2f}%",
        )

    with st.expander(
        "View measurements being explained",
        expanded=False,
    ):
        st.dataframe(
            input_data.T.rename(
                columns={0: "Measured Value"}
            ),
            use_container_width=True,
        )

    lime_explainer = create_lime_explainer(
        lime_reference_data
    )
    

    class_mapping = {
        int(class_id): class_name
        for class_id, class_name
        in metadata["class_mapping"].items()
    }

    predicted_class_index = next(
        class_id
        for class_id, class_name
        in class_mapping.items()
        if class_name == predicted_class
    )
    

    lime_explanation = generate_lime_explanation(
        lime_explainer=lime_explainer,
        model=model,
        input_data=input_data,
        predicted_class=predicted_class_index,
        num_features=10,
    )
    

    lime_df = lime_explanation_to_dataframe(
        explanation=lime_explanation,
        predicted_class=predicted_class_index,
    )
    

    st.divider()

    st.markdown("## LIME Local Explanation")

    st.caption(
        "The table shows the features that most strongly supported "
        "or opposed the latest prediction."
    )

    st.dataframe(
        lime_df[
            [
                "Feature Condition",
                "Contribution",
                "Direction",
            ]
        ],
        use_container_width=True,
        hide_index=True,
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

    st.divider()

    st.markdown("## SHAP Local Explanation")

    st.caption(
        "SHAP shows how each transformer measurement pushed the model "
        "toward or away from the predicted health class."
    )

    # ---------------------------------------------------------
    # PREPARE WATERFALL EXPLANATION
    # ---------------------------------------------------------
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


    waterfall_explanation = shap.Explanation(
        values=selected_shap_values,
        base_values=selected_base_value,
        data=input_data.iloc[0].values,
        feature_names=input_data.columns.tolist(),
    )


    # ---------------------------------------------------------
    # WATERFALL PLOT AND FEATURE TABLE
    # ---------------------------------------------------------
    plot_column, table_column = st.columns(
        [1.25, 1],
        gap="large",
    )

    with plot_column:
        st.markdown("### Prediction Waterfall")

        st.caption(
            "Red features increase the model score for the predicted "
            "class, while blue features reduce it."
        )

        fig, axis = plt.subplots(
            figsize=(10, 7)
        )

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
        st.markdown("### Top SHAP Features")

        st.caption(
            "The ten measurements with the strongest influence on "
            "the latest prediction."
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


    # ---------------------------------------------------------
    # PLAIN-LANGUAGE INTERPRETATION
    # ---------------------------------------------------------
    st.markdown("### Explanation Summary")

    interpretation = generate_shap_interpretation(
        shap_df=shap_df,
        predicted_class=predicted_class,
        confidence=confidence,
    )

    st.info(interpretation)