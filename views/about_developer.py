"""About page for GridGuard AI."""

import streamlit as st


def render_about_developer():
    """Render information about GridGuard AI and its developer."""

    st.title("About GridGuard AI")

    st.caption(
        "An intelligent transformer health assessment platform "
        "powered by Machine Learning and Explainable AI."
    )

    st.divider()

    # ---------------------------------------------------------
    # PROJECT OVERVIEW
    # ---------------------------------------------------------
    st.markdown("## Project Overview")

    st.write(
        "GridGuard AI is an intelligent transformer condition "
        "assessment system developed as a final-year Bachelor of "
        "Technology in Artificial Intelligence research project at "
        "Kumasi Technical University."
    )

    st.write(
        "The system combines dissolved gas analysis, machine learning "
        "and Explainable AI to classify transformer health conditions "
        "and provide transparent explanations for each prediction."
    )

    st.divider()

    # ---------------------------------------------------------
    # DEVELOPER PROFILE
    # ---------------------------------------------------------
    st.markdown("## Developer Profile")

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        with st.container(border=True):
            st.markdown("### 👨‍💻 Developer Information")

            st.markdown("**Name**")
            st.write("Teddy Boamah")

            st.markdown("**Research Area**")
            st.write("Artificial Intelligence for Predictive Maintenance")

            st.markdown("**Project Year**")
            st.write("2026")

    with right_col:
        with st.container(border=True):
            st.markdown("### 🎓 Academic Information")

            st.markdown("**Programme**")
            st.write("Bachelor of Technology (Artificial Intelligence)")

            st.markdown("**Institution**")
            st.write("Kumasi Technical University")

            st.markdown("**Project**")
            st.write("GridGuard AI")

    st.divider()

    # ---------------------------------------------------------
    # TECHNOLOGY STACK
    # ---------------------------------------------------------
    st.markdown("## Technology Stack")

    tech_col1, tech_col2 = st.columns(2, gap="large")

    with tech_col1:

        with st.container(border=True):

            st.markdown("### 🤖 AI & Machine Learning")

            st.markdown("""
            - XGBoost
            - Scikit-learn
            - SHAP
            - LIME
            """)

        with st.container(border=True):

            st.markdown("### 🐍 Programming")

            st.markdown("""
            - Python
            - Pandas
            - NumPy
            - Joblib
            """)

    with tech_col2:

        with st.container(border=True):

            st.markdown("### 💻 Frameworks & Visualization")

            st.markdown("""
            - Streamlit
            - Matplotlib
            - JSON
            """)

        with st.container(border=True):

            st.markdown("### ⚡ Power Systems")

            st.markdown("""
            - Transformer DGA
            - Predictive Maintenance
            - Condition Monitoring
            """)

    st.divider()

    # ---------------------------------------------------------
    # RESEARCH CONTRIBUTIONS
    # ---------------------------------------------------------
    st.markdown("## Research Contributions")

    contrib_col1, contrib_col2 = st.columns(2, gap="large")

    with contrib_col1:
        with st.container(border=True):
            st.markdown("### 🧠 Intelligent Diagnosis")

            st.write(
                "Predicts transformer health conditions using dissolved "
                "gas analysis and a trained XGBoost classification model."
            )

        with st.container(border=True):
            st.markdown("### 💻 Interactive Dashboard")

            st.write(
                "Provides a clear Streamlit-based interface for entering "
                "transformer measurements and reviewing prediction results."
            )

    with contrib_col2:
        with st.container(border=True):
            st.markdown("### 🔍 Explainable AI")

            st.write(
                "Uses SHAP and LIME to show how individual transformer "
                "measurements influenced each model prediction."
            )

        with st.container(border=True):
            st.markdown("### ⚡ Maintenance Decision Support")

            st.write(
                "Supports maintenance teams by presenting transformer "
                "health predictions and interpretable diagnostic insights."
            )

    st.divider()

    # ---------------------------------------------------------
    # ACKNOWLEDGEMENTS
    # ---------------------------------------------------------
    st.markdown("## Acknowledgements")

    with st.container(border=True):

        st.write(
            "This project was completed as partial fulfillment of the "
            "requirements for the award of **Bachelor of Technology "
            "(Artificial Intelligence)** at **Kumasi Technical University**."
        )

        st.write(
            "The developer expresses sincere appreciation to "
            "**Dr. Umar Farouk**, Project Supervisor, for his guidance, "
            "constructive feedback and continuous support throughout the "
            "research and development of GridGuard AI."
        )

        st.write(
            "Special appreciation is extended to **Nana Gyamfi**, "
            "Academic Advisor and mentor, whose encouragement, guidance "
            "and unwavering belief in the developer's potential have been "
            "a constant source of motivation throughout the academic journey."
        )

        st.write(
            "The developer also expresses heartfelt gratitude to the "
            "lecturers and staff of the **Department of Computer Science, "
            "Kumasi Technical University**, for imparting the knowledge, "
            "skills and academic foundation that made this project possible."
        )
    
    st.divider()

    # ---------------------------------------------------------
    # CONTACT AND FOOTER
    # ---------------------------------------------------------
    st.markdown("## Professional Contact")

    contact_col1, contact_col2 = st.columns(2, gap="large")

    with contact_col1:
        with st.container(border=True):

            st.markdown("### 📬 Contact Information")

            st.markdown("**📧 Email**")
            st.markdown(
                "[hello@teddyboamah.com](mailto:hello@teddyboamah.com)"
            )

            st.markdown("**🌐 Portfolio**")
            st.markdown(
                "[teddyboamah.com](https://teddyboamah.com)"
            )

    with contact_col2:
        with st.container(border=True):

            st.markdown("### 💻 Professional Profiles")

            st.markdown("**GitHub**")
            st.markdown(
                "[github.com/birdcoreone](https://github.com/birdcoreone)"
            )

            st.markdown("**LinkedIn**")
            st.markdown(
                "[linkedin.com/in/teddyboamah](https://linkedin.com/in/teddyboamah)"
            )

    st.divider()

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    st.markdown(
        """
        <div style="text-align:center;">

        <h4>
        Empowering reliable transformer maintenance through
        trustworthy Artificial Intelligence.
        </h4>

        <br>

        <span style="
            display:inline-block;
            padding:8px 16px;
            border-radius:25px;
            border:1px solid #3a4a5a;
            background-color:#162231;
            color:#d6d6d6;
            font-size:14px;
            font-weight:600;
        ">
        🚀 Powered by Python • Streamlit • XGBoost • SHAP • LIME
        </span>

        <br><br>

        <p style="color:#9aa5b1; font-size:14px;">
        <strong>GridGuard AI Version 1.0</strong><br>
        © 2026 Teddy Boamah<br>
        Bachelor of Technology (Artificial Intelligence)<br>
        Kumasi Technical University
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )