
import joblib
import pandas as pd
import streamlit as st

from utils.config import (
    MODEL_PATH,
    FEATURE_NAMES_PATH,
    MODEL_METADATA_PATH,
    FEATURE_ENGINEERED_DATA_PATH,
    ML_READY_DATA_PATH,
    PREDICTIONS_PATH,
    RISK_RANKING_PATH,
    RECOMMENDATIONS_PATH,
    EXECUTIVE_KPIS_PATH,
    BUSINESS_SEGMENTS_PATH,
    MODEL_RESULTS_PATH
)


@st.cache_resource
def load_model_assets():
    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(
        FEATURE_NAMES_PATH
    )
    metadata = joblib.load(
        MODEL_METADATA_PATH
    )

    return model, feature_names, metadata


@st.cache_data
def load_business_data():
    return pd.read_csv(
        FEATURE_ENGINEERED_DATA_PATH
    )


@st.cache_data
def load_ml_data():
    return pd.read_csv(
        ML_READY_DATA_PATH
    )


@st.cache_data
def load_predictions():
    return pd.read_csv(
        PREDICTIONS_PATH
    )


@st.cache_data
def load_risk_ranking():
    return pd.read_csv(
        RISK_RANKING_PATH
    )


@st.cache_data
def load_recommendations():
    return pd.read_csv(
        RECOMMENDATIONS_PATH
    )


@st.cache_data
def load_executive_kpis():
    return pd.read_csv(
        EXECUTIVE_KPIS_PATH
    )


@st.cache_data
def load_business_segments():
    return pd.read_csv(
        BUSINESS_SEGMENTS_PATH
    )


@st.cache_data
def load_model_results():
    return pd.read_csv(
        MODEL_RESULTS_PATH
    )
