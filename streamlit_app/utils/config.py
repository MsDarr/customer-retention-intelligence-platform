
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

MODELS_DIR = os.path.join(
    PROJECT_DIR,
    "models"
)

PROCESSED_DATA_DIR = os.path.join(
    PROJECT_DIR,
    "data",
    "processed"
)

EXPORTS_DIR = os.path.join(
    PROJECT_DIR,
    "exports"
)

REPORTS_DIR = os.path.join(
    PROJECT_DIR,
    "reports"
)

ASSETS_DIR = os.path.join(
    BASE_DIR,
    "assets"
)

MODEL_PATH = os.path.join(
    MODELS_DIR,
    "customer_churn_model.pkl"
)

FEATURE_NAMES_PATH = os.path.join(
    MODELS_DIR,
    "model_feature_names.pkl"
)

MODEL_METADATA_PATH = os.path.join(
    MODELS_DIR,
    "model_metadata.pkl"
)

FEATURE_ENGINEERED_DATA_PATH = os.path.join(
    PROCESSED_DATA_DIR,
    "customer_churn_feature_engineered.csv"
)

ML_READY_DATA_PATH = os.path.join(
    PROCESSED_DATA_DIR,
    "customer_churn_ml_ready.csv"
)

PREDICTIONS_PATH = os.path.join(
    EXPORTS_DIR,
    "customer_predictions.csv"
)

RISK_RANKING_PATH = os.path.join(
    EXPORTS_DIR,
    "customer_risk_ranking.csv"
)

RECOMMENDATIONS_PATH = os.path.join(
    EXPORTS_DIR,
    "customer_retention_recommendations.csv"
)

EXECUTIVE_KPIS_PATH = os.path.join(
    EXPORTS_DIR,
    "executive_dashboard_kpis.csv"
)

BUSINESS_SEGMENTS_PATH = os.path.join(
    EXPORTS_DIR,
    "business_segments.csv"
)

MODEL_RESULTS_PATH = os.path.join(
    REPORTS_DIR,
    "model_comparison_results.csv"
)
