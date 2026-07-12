
import numpy as np
import pandas as pd

from utils.data_loader import (
    load_model_assets,
    load_business_data
)


CONTRACT_WEIGHT_MAP = {
    "Month-to-month": 1,
    "One year": 2,
    "Two year": 3
}

INTERNET_USAGE_MAP = {
    "Fiber optic": "High-Speed Internet",
    "DSL": "Standard Internet",
    "No": "No Internet Service"
}

SERVICE_COLUMNS = [
    "PhoneService",
    "MultipleLines",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]

SUPPORT_COLUMNS = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport"
]


def _safe_minmax(value, minimum, maximum):
    """Scale one value to the 0–1 range safely."""

    if maximum == minimum:
        return 0.0

    return (value - minimum) / (maximum - minimum)


def _create_tenure_category(tenure):
    """Reproduce Notebook 4 tenure categories."""

    if tenure <= 12:
        return "New Customer"

    if tenure <= 24:
        return "Developing Customer"

    if tenure <= 48:
        return "Established Customer"

    return "Loyal Customer"


def engineer_customer_features(customer):
    """
    Recreate all business features used during model training.

    Parameters
    ----------
    customer : dict
        Raw customer information submitted through Streamlit.

    Returns
    -------
    pandas.DataFrame
        One-row business-readable feature dataframe.
    """

    reference_data = load_business_data()

    row = customer.copy()

    # --------------------------------------------------------
    # Financial features
    # --------------------------------------------------------

    row["CustomerLifetimeValue"] = round(
        row["MonthlyCharges"] * row["tenure"],
        2
    )

    row["EstimatedAnnualRevenue"] = round(
        row["MonthlyCharges"] * 12,
        2
    )

    row["AverageMonthlySpend"] = round(
        row["MonthlyCharges"],
        2
    )

    # --------------------------------------------------------
    # Loyalty features
    # --------------------------------------------------------

    row["ContractWeight"] = CONTRACT_WEIGHT_MAP[
        row["Contract"]
    ]

    row["LoyaltyScore"] = round(
        row["tenure"] * 0.7
        + row["ContractWeight"] * 10,
        2
    )

    row["TenureCategory"] = _create_tenure_category(
        row["tenure"]
    )

    # --------------------------------------------------------
    # Service features
    # --------------------------------------------------------

    row["ServiceCount"] = sum(
        row[column] == "Yes"
        for column in SERVICE_COLUMNS
    )

    row["SupportUsageScore"] = sum(
        row[column] == "Yes"
        for column in SUPPORT_COLUMNS
    )

    row["InternetUsageCategory"] = INTERNET_USAGE_MAP[
        row["InternetService"]
    ]

    row["RetentionScore"] = round(
        row["tenure"] * 0.6
        + row["ServiceCount"] * 5,
        2
    )

    # --------------------------------------------------------
    # Customer segmentation features
    # --------------------------------------------------------

    high_value_threshold = (
        reference_data["CustomerLifetimeValue"]
        .quantile(0.75)
    )

    row["HighValueCustomer"] = int(
        row["CustomerLifetimeValue"]
        >= high_value_threshold
    )

    premium_charge_threshold = (
        reference_data["MonthlyCharges"]
        .quantile(0.75)
    )

    premium_service_threshold = (
        reference_data["ServiceCount"]
        .median()
    )

    row["PremiumCustomer"] = int(
        row["MonthlyCharges"]
        >= premium_charge_threshold
        and row["ServiceCount"]
        >= premium_service_threshold
    )

    # --------------------------------------------------------
    # Customer Value Score
    # --------------------------------------------------------

    scaled_clv = _safe_minmax(
        row["CustomerLifetimeValue"],
        reference_data[
            "CustomerLifetimeValue"
        ].min(),
        reference_data[
            "CustomerLifetimeValue"
        ].max()
    )

    scaled_loyalty = _safe_minmax(
        row["LoyaltyScore"],
        reference_data["LoyaltyScore"].min(),
        reference_data["LoyaltyScore"].max()
    )

    scaled_service = _safe_minmax(
        row["ServiceCount"],
        reference_data["ServiceCount"].min(),
        reference_data["ServiceCount"].max()
    )

    row["CustomerValueScore"] = round(
        (
            scaled_clv * 0.50
            + scaled_loyalty * 0.30
            + scaled_service * 0.20
        )
        * 100,
        2
    )

    # --------------------------------------------------------
    # Customer Risk Score
    # --------------------------------------------------------

    scaled_contract = _safe_minmax(
        row["ContractWeight"],
        reference_data["ContractWeight"].min(),
        reference_data["ContractWeight"].max()
    )

    row["CustomerRiskScore"] = round(
        (
            (1 - scaled_loyalty) * 0.50
            + (1 - scaled_service) * 0.30
            + (1 - scaled_contract) * 0.20
        )
        * 100,
        2
    )

    return pd.DataFrame([row])


def encode_customer_features(customer_df, feature_names):
    """
    One-hot encode and align one customer with model columns.
    """

    categorical_columns = customer_df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    encoded = pd.get_dummies(
        customer_df,
        columns=categorical_columns,
        drop_first=False,
        dtype=int
    )

    encoded = encoded.reindex(
        columns=feature_names,
        fill_value=0
    )

    return encoded


def get_positive_class_index(model):
    """
    Identify the probability column corresponding to churn = 1.
    """

    classes = list(model.classes_)

    if 1 not in classes:
        raise ValueError(
            "The trained model does not contain "
            "the positive churn class 1."
        )

    return classes.index(1)


def predict_customer(customer):
    """
    Generate churn prediction and business scores.
    """

    model, feature_names, metadata = (
        load_model_assets()
    )

    engineered_customer = engineer_customer_features(
        customer
    )

    encoded_customer = encode_customer_features(
        engineered_customer,
        feature_names
    )

    positive_index = get_positive_class_index(
        model
    )

    probability = float(
        model.predict_proba(
            encoded_customer
        )[0, positive_index]
    )

    threshold = float(
        metadata.get(
            "classification_threshold",
            0.50
        )
    )

    predicted_class = int(
        probability >= threshold
    )

    predicted_label = (
        "Predicted Churn"
        if predicted_class == 1
        else "Predicted Stay"
    )

    return {
        "predicted_class": predicted_class,
        "predicted_label": predicted_label,
        "churn_probability": probability,
        "churn_probability_percent": round(
            probability * 100,
            2
        ),
        "threshold": threshold,
        "engineered_customer": engineered_customer,
        "encoded_customer": encoded_customer
    }
