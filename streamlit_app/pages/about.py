
import streamlit as st

from utils.data_loader import (
    load_model_assets
)


def render():

    st.title("About the Platform")

    st.caption(
        "AI-powered customer churn prediction, "
        "risk intelligence, and retention decision support."
    )

    model, feature_names, metadata = (
        load_model_assets()
    )

    st.markdown(
        """
        ## Project Overview

        The AI-Powered Customer Retention Intelligence
        Platform is an end-to-end machine learning and
        business intelligence solution designed to identify
        customers at risk of churn and translate predictions
        into actionable retention strategies.

        The platform integrates:

        - Customer churn prediction
        - Customer risk scoring
        - Personalized retention recommendations
        - Revenue intelligence
        - Executive dashboards
        - Downloadable business reports
        """
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Production Model",
            metadata.get(
                "model_name",
                type(model).__name__
            )
        )

    with col2:
        st.metric(
            "Predictor Features",
            len(feature_names)
        )

    with col3:
        st.metric(
            "Classification Threshold",
            metadata.get(
                "classification_threshold",
                0.50
            )
        )

    st.markdown("---")

    st.markdown(
        """
        ## Technology Stack

        - Python
        - Pandas and NumPy
        - Scikit-learn
        - XGBoost
        - Plotly
        - Streamlit
        - Joblib
        - Google Colab
        - GitHub

        ## Analytical Workflow

        1. Data cleaning and preprocessing  
        2. Exploratory data analysis  
        3. Feature engineering  
        4. Machine learning development  
        5. Model evaluation and selection  
        6. Explainable AI and business intelligence  
        7. Interactive platform deployment  

        ## Responsible Use

        Predictions should support—not replace—human
        judgment. Customer-retention actions should be
        reviewed for fairness, relevance, financial impact,
        and customer experience before implementation.
        """
    )
