"""Home page for GridGuard AI."""

from typing import Any

import streamlit as st


def _format_percentage(value: Any, fallback: float) -> str:
    """Format a decimal value as a percentage."""

    try:
        return f"{float(value) * 100:.2f}%"
    except (TypeError, ValueError):
        return f"{fallback * 100:.2f}%"


def _format_score(value: Any, fallback: float) -> str:
    """Format an evaluation score to four decimal places."""

    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return f"{fallback:.4f}"


def render_home(metadata: dict[str, Any]) -> None:
    """Render the GridGuard AI landing page."""

    # -----------------------------------------------------
    # DASHBOARD HEADER
    # -----------------------------------------------------
    header_left, header_right = st.columns(
        [3.6, 1.2],
        vertical_alignment="center",
    )

    with header_left:
        st.caption(
            "PREDICTIVE MAINTENANCE · EXPLAINABLE ARTIFICIAL INTELLIGENCE"
        )

        st.markdown(
            """
            <div class="brand-kicker">
                ⚡ GRIDGUARD AI
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.title("Transformer Health Intelligence System")

        st.write(
            """
            GridGuard AI converts dissolved-gas and oil-quality
            measurements into explainable transformer condition
            assessments, helping maintenance teams detect risks
            before they develop into costly failures.
            """
        )

    with header_right:
        with st.container(border=True):
            st.caption("SYSTEM STATUS")

            st.success("● Intelligence Engine Online")

            st.caption("ACTIVE MODEL")
            st.markdown("#### SMOTE XGBoost")

            st.caption("TEST ACCURACY")
            st.markdown("#### 95.74%")

    st.divider()

    # -----------------------------------------------------
    # MODEL PERFORMANCE
    # -----------------------------------------------------
    st.markdown("### Model Performance Overview")

    accuracy = metadata.get("test_accuracy", 0.9574)
    macro_f1 = metadata.get("test_macro_f1", 0.4514)
    weighted_f1 = metadata.get("test_weighted_f1")

    feature_names = metadata.get("feature_names", [])
    class_mapping = metadata.get("class_mapping", {})

    first_row = st.columns(3)

    with first_row[0]:
        st.metric(
            label="Test Accuracy",
            value=_format_percentage(accuracy, 0.9574),
            help=(
                "Overall proportion of correctly classified "
                "transformer samples in the test set."
            ),
        )

    with first_row[1]:
        st.metric(
            label="Macro F1",
            value=_format_score(macro_f1, 0.4514),
            help=(
                "Balances precision and recall while giving "
                "every health class equal importance."
            ),
        )

    with first_row[2]:
        weighted_value = (
            _format_score(weighted_f1, 0.0)
            if weighted_f1 is not None
            else "Pending"
        )

        st.metric(
            label="Weighted F1",
            value=weighted_value,
            help=(
                "Balances precision and recall while accounting "
                "for the number of samples in each health class."
            ),
        )

    second_row = st.columns(3)

    with second_row[0]:
        st.metric(
            label="Transformer Samples",
            value=str(metadata.get("sample_count", 470)),
        )

    with second_row[1]:
        st.metric(
            label="Diagnostic Features",
            value=str(len(feature_names) if feature_names else 14),
        )

    with second_row[2]:
        st.metric(
            label="Health Classes",
            value=str(len(class_mapping) if class_mapping else 4),
        )

    # -----------------------------------------------------
    # SYSTEM CAPABILITIES
    # -----------------------------------------------------
    st.markdown("### System Capabilities")

    capability_columns = st.columns(3)

    capabilities = [
        (
            "⚡ Intelligent Assessment",
            "Classifies transformer condition as Critical, Poor, "
            "Good or Excellent from 14 diagnostic measurements.",
        ),
        (
            "🧠 Explainable Predictions",
            "Uses SHAP and LIME to reveal the measurements that "
            "influenced each model decision.",
        ),
        (
            "🛠 Maintenance Support",
            "Translates model results into clear condition-based "
            "maintenance guidance for technical users.",
        ),
    ]

    for column, (title, description) in zip(
        capability_columns,
        capabilities,
    ):
        with column:
            with st.container(border=True):
                st.markdown(f"#### {title}")
                st.write(description)

    # -----------------------------------------------------
    # MODEL AT A GLANCE
    # -----------------------------------------------------
    st.markdown("### Model at a Glance")

    glance_left, glance_right = st.columns(2)

    with glance_left:
        with st.container(border=True):
            st.markdown("#### Intelligence Engine")

            st.write(
                metadata.get(
                    "model_name",
                    "SMOTE XGBoost",
                )
            )

            st.markdown("#### Analytical Task")

            st.write(
                "Multiclass transformer health classification"
            )

    with glance_right:
        with st.container(border=True):
            st.markdown("#### Explainability Framework")

            st.write("SHAP and LIME")

            st.markdown("#### Developed By")

            st.write(
                metadata.get(
                    "developer",
                    "Teddy Boamah",
                )
            )