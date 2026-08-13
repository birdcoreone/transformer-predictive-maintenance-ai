"""Global styling for the GridGuard AI application."""

import streamlit as st


def apply_global_styles() -> None:
    """Apply the GridGuard AI dark industrial interface theme."""

    st.markdown(
        """
        <style>
        /* --------------------------------------------------
           ROOT VARIABLES
        -------------------------------------------------- */
        :root {
            --background: #07111f;
            --sidebar: #051120;
            --surface: rgba(255, 255, 255, 0.055);
            --surface-hover: rgba(255, 255, 255, 0.085);
            --border: rgba(255, 255, 255, 0.10);
            --primary: #31b8ff;
            --secondary: #7cecff;
            --success: #34d399;
            --warning: #f59e0b;
            --critical: #ef4444;
            --text: #f8fafc;
            --muted: #a9bdd2;
        }

        /* --------------------------------------------------
           APPLICATION BACKGROUND
        -------------------------------------------------- */
        .stApp {
            background:
                radial-gradient(
                    circle at 90% 5%,
                    rgba(49, 184, 255, 0.13),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 10% 95%,
                    rgba(124, 236, 255, 0.08),
                    transparent 30%
                ),
                linear-gradient(
                    145deg,
                    #07111f 0%,
                    #081626 50%,
                    #06101d 100%
                );

            color: var(--text);
        }

        /* --------------------------------------------------
           MAIN CONTENT WIDTH
        -------------------------------------------------- */
        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* --------------------------------------------------
           SIDEBAR
        -------------------------------------------------- */
        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    rgba(5, 17, 32, 0.99),
                    rgba(6, 20, 36, 0.98)
                );

            border-right: 1px solid rgba(49, 184, 255, 0.17);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }

        /* --------------------------------------------------
           TYPOGRAPHY
        -------------------------------------------------- */
        h1, h2, h3 {
            color: var(--text);
            letter-spacing: -0.02em;
        }

        p {
            color: var(--muted);
        }

        /* --------------------------------------------------
           HERO SECTION
        -------------------------------------------------- */
        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 3rem;
            margin-bottom: 1.6rem;
            border-radius: 28px;

            background:
                linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.075),
                    rgba(255, 255, 255, 0.025)
                );

            border: 1px solid var(--border);

            box-shadow:
                0 25px 60px rgba(0, 0, 0, 0.32),
                inset 0 1px 0 rgba(255, 255, 255, 0.07);

            backdrop-filter: blur(18px);
        }

        .hero-card::before {
            content: "";
            position: absolute;
            width: 340px;
            height: 340px;
            top: -190px;
            right: -100px;
            border-radius: 50%;
            background: rgba(49, 184, 255, 0.15);
            filter: blur(15px);
        }

        .eyebrow {
            color: var(--secondary);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.18rem;
            text-transform: uppercase;
            margin-bottom: 0.9rem;
        }

        .hero-title {
            position: relative;
            z-index: 1;
            max-width: 900px;
            margin: 0;
            font-size: clamp(2.7rem, 6vw, 5.2rem);
            font-weight: 850;
            line-height: 1.02;

            background:
                linear-gradient(
                    90deg,
                    #ffffff 0%,
                    #dff9ff 42%,
                    #70deff 100%
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            position: relative;
            z-index: 1;
            max-width: 880px;
            margin-top: 1.35rem;
            color: var(--muted);
            font-size: 1.08rem;
            line-height: 1.8;
        }

        /* --------------------------------------------------
           STATUS BADGE
        -------------------------------------------------- */
        .system-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.6rem;

            margin-top: 1.7rem;
            padding: 0.65rem 1rem;
            border-radius: 999px;

            background: rgba(52, 211, 153, 0.09);
            border: 1px solid rgba(52, 211, 153, 0.23);

            color: #8af3ca;
            font-size: 0.86rem;
            font-weight: 650;
        }

        .pulse-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 0 rgba(52, 211, 153, 0.5);
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.5);
            }

            70% {
                box-shadow: 0 0 0 9px rgba(52, 211, 153, 0);
            }

            100% {
                box-shadow: 0 0 0 0 rgba(52, 211, 153, 0);
            }
        }

        /* --------------------------------------------------
           METRIC CARDS
        -------------------------------------------------- */
        div[data-testid="stMetric"] {
            min-height: 135px;
            padding: 1.3rem 1.35rem;
            border-radius: 20px;

            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.07),
                    rgba(255, 255, 255, 0.025)
                );

            border: 1px solid var(--border);

            box-shadow:
                0 14px 35px rgba(0, 0, 0, 0.23),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);

            transition:
                transform 180ms ease,
                border-color 180ms ease,
                background 180ms ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: rgba(49, 184, 255, 0.36);
            background: var(--surface-hover);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
            font-size: 0.86rem;
        }

        div[data-testid="stMetricValue"] {
            color: var(--secondary);
            font-size: 2rem;
            font-weight: 800;
        }

        /* --------------------------------------------------
           GENERIC GLASS PANEL
        -------------------------------------------------- */
        .glass-panel {
            padding: 1.6rem;
            border-radius: 22px;
            background: var(--surface);
            border: 1px solid var(--border);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.22);
        }

        .panel-title {
            margin-bottom: 0.7rem;
            color: var(--text);
            font-size: 1.08rem;
            font-weight: 750;
        }

        .panel-copy {
            color: var(--muted);
            line-height: 1.7;
        }

        /* --------------------------------------------------
           BUTTONS
        -------------------------------------------------- */
        .stButton > button {
            min-height: 46px;
            border: 1px solid rgba(49, 184, 255, 0.35);
            border-radius: 13px;

            background:
                linear-gradient(
                    90deg,
                    rgba(49, 184, 255, 0.20),
                    rgba(124, 236, 255, 0.12)
                );

            color: #eafaff;
            font-weight: 700;

            transition:
                transform 150ms ease,
                box-shadow 150ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            border-color: rgba(124, 236, 255, 0.7);
            box-shadow: 0 10px 25px rgba(49, 184, 255, 0.16);
        }

        /* --------------------------------------------------
           HIDE STREAMLIT CHROME
        -------------------------------------------------- */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        [data-testid="stHeader"] {
            background: transparent;
            height: 0;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stStatusWidget"] {
            display: none;
        }

        /* --------------------------------------------------
        NATIVE STREAMLIT HEADER AND CONTAINERS
        -------------------------------------------------- */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: rgba(255, 255, 255, 0.10);
            border-radius: 20px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.06),
                    rgba(255, 255, 255, 0.025)
                );
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.20);
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(49, 184, 255, 0.28);
        }

        .stMainBlockContainer > div > div > div:first-child h1 {
            font-size: clamp(2.7rem, 5vw, 4.8rem);
            line-height: 1.04;
            margin-bottom: 0.8rem;
            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #dff9ff,
                    #70deff
                );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stMainBlockContainer > div > div > div:first-child p {
            max-width: 900px;
            line-height: 1.75;
            color: #a9bdd2;
        }

        [data-testid="stCaptionContainer"] {
            color: #7cecff;
            letter-spacing: 0.08em;
            font-weight: 700;
        }

        /* --------------------------------------------------
        HERO BRANDING
        -------------------------------------------------- */
        .brand-kicker {
            margin-bottom: 0.65rem;
            color: #7cecff;
            font-size: clamp(1.2rem, 2vw, 1.75rem);
            font-weight: 850;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            text-shadow: 0 0 22px rgba(49, 184, 255, 0.28);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )