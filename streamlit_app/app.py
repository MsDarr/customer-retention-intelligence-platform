
import streamlit as st

from pages import (
    dashboard,
    prediction,
    risk_scoring,
    recommendations,
    revenue_intelligence,
    executive_dashboard,
    reports,
    about
)


st.set_page_config(
    page_title=(
        "AI-Powered Customer Retention "
        "Intelligence Platform"
    ),
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def apply_custom_style():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0F172A;
            color: #F8FAFC;
        }

        [data-testid="stSidebar"] {
            background-color: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #F8FAFC;
        }

        .main-header {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .sub-header {
            font-size: 1.05rem;
            color: #CBD5E1;
            margin-bottom: 1.8rem;
        }

        .metric-card {
            background: linear-gradient(
                135deg,
                #1E293B,
                #0F172A
            );
            padding: 1.2rem;
            border-radius: 14px;
            border: 1px solid #334155;
            box-shadow: 0 8px 24px
                rgba(0, 0, 0, 0.20);
        }

        .feature-card {
            background-color: #1E293B;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #334155;
            min-height: 160px;
        }

        .footer {
            text-align: center;
            color: #94A3B8;
            padding-top: 2rem;
            padding-bottom: 1rem;
            font-size: 0.85rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def render_home():

    st.markdown(
        """
        <div class="main-header">
        AI-Powered Customer Retention
        Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-header">
        Predict customer churn, assess business risk,
        generate retention recommendations, and monitor
        revenue exposure through one intelligent platform.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Machine Learning",
            value="Production Ready"
        )

    with col2:
        st.metric(
            label="Risk Scoring",
            value="Enabled"
        )

    with col3:
        st.metric(
            label="Recommendations",
            value="Automated"
        )

    with col4:
        st.metric(
            label="Revenue Intelligence",
            value="Integrated"
        )

    st.markdown("---")

    st.subheader("Platform Capabilities")

    feature_columns = st.columns(4)

    features = [
        (
            "🔍 Customer Prediction",
            "Generate real-time churn probabilities "
            "for individual customers."
        ),
        (
            "⚠️ Risk Scoring",
            "Classify customers into low, moderate, "
            "high, and critical risk groups."
        ),
        (
            "💡 Recommendations",
            "Generate personalized retention actions, "
            "offers, and communication channels."
        ),
        (
            "💰 Revenue Intelligence",
            "Measure monthly and annual revenue "
            "exposure associated with churn risk."
        )
    ]

    for column, (title, description) in zip(
        feature_columns,
        features
    ):

        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.subheader("How the Platform Works")

    st.markdown(
        """
        1. Customer information is processed through
        the production machine learning model.

        2. The platform calculates churn probability
        and assigns a customer risk category.

        3. Customer value and service engagement are
        combined with model predictions.

        4. The recommendation engine proposes
        personalized retention actions.

        5. Revenue intelligence estimates the financial
        impact associated with customer churn.
        """
    )


def render_sidebar():

    with st.sidebar:

        st.title("Retention AI")

        st.caption(
            "Customer Intelligence Platform"
        )

        st.markdown("---")

        selected_page = st.radio(
            "Navigation",
            [
                "Home",
                "Dashboard",
                "Customer Prediction",
                "Risk Scoring",
                "Recommendations",
                "Revenue Intelligence",
                "Executive Dashboard",
                "Reports",
                "About"
            ]
        )

        st.markdown("---")

        st.success(
            "Production model loaded"
        )

        st.caption(
            "AI-Powered Customer Retention "
            "Intelligence Platform"
        )

    return selected_page


def main():

    apply_custom_style()

    selected_page = render_sidebar()

    if selected_page == "Home":
        render_home()

    elif selected_page == "Dashboard":
        dashboard.render()

    elif selected_page == "Customer Prediction":
        prediction.render()

    elif selected_page == "Risk Scoring":
        risk_scoring.render()

    elif selected_page == "Recommendations":
        recommendations.render()

    elif selected_page == "Revenue Intelligence":
        revenue_intelligence.render()

    elif selected_page == "Executive Dashboard":
        executive_dashboard.render()

    elif selected_page == "Reports":
        reports.render()

    elif selected_page == "About":
        about.render()

    st.markdown(
        """
        <div class="footer">
        AI-Powered Customer Retention Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
