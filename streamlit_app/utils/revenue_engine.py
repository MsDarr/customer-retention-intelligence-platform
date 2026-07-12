
import pandas as pd


def validate_revenue_columns(data):
    """
    Confirm that all columns required for revenue
    calculations are available.
    """

    required_columns = [
        "MonthlyCharges",
        "ChurnProbability",
        "RiskCategory",
        "BusinessSegment"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    return missing_columns


def calculate_revenue_metrics(
    data,
    recovery_rate=0.30
):
    """
    Add customer-level revenue intelligence metrics.

    Parameters
    ----------
    data : pandas.DataFrame
        Customer prediction and business dataset.

    recovery_rate : float
        Assumed percentage of expected revenue loss
        recoverable through retention intervention.

    Returns
    -------
    pandas.DataFrame
        Dataset containing revenue-risk metrics.
    """

    revenue_data = data.copy()

    revenue_data["MonthlyRevenueExposure"] = (
        revenue_data["MonthlyCharges"]
    ).round(2)

    revenue_data["AnnualRevenueExposure"] = (
        revenue_data["MonthlyCharges"] * 12
    ).round(2)

    revenue_data["ExpectedMonthlyRevenueLoss"] = (
        revenue_data["MonthlyCharges"]
        * revenue_data["ChurnProbability"]
    ).round(2)

    revenue_data["ExpectedAnnualRevenueLoss"] = (
        revenue_data["MonthlyCharges"]
        * 12
        * revenue_data["ChurnProbability"]
    ).round(2)

    if "CustomerLifetimeValue" in revenue_data.columns:

        revenue_data["ExpectedLifetimeValueLoss"] = (
            revenue_data["CustomerLifetimeValue"]
            * revenue_data["ChurnProbability"]
        ).round(2)

    else:

        revenue_data["ExpectedLifetimeValueLoss"] = (
            revenue_data["ExpectedAnnualRevenueLoss"]
        ).round(2)

    revenue_data["PotentialAnnualRevenueRecovery"] = (
        revenue_data["ExpectedAnnualRevenueLoss"]
        * recovery_rate
    ).round(2)

    revenue_data["NetAnnualRevenueRiskAfterRetention"] = (
        revenue_data["ExpectedAnnualRevenueLoss"]
        - revenue_data[
            "PotentialAnnualRevenueRecovery"
        ]
    ).round(2)

    return revenue_data


def calculate_revenue_kpis(
    revenue_data,
    recovery_rate=0.30
):
    """
    Calculate executive revenue-intelligence KPIs.
    """

    high_risk_mask = (
        revenue_data["RiskCategory"]
        .isin(["High", "Critical"])
    )

    high_value_mask = (
        revenue_data.get(
            "CustomerValueGroup",
            pd.Series(
                "Unknown",
                index=revenue_data.index
            )
        )
        == "High Value"
    )

    kpis = {
        "Total Monthly Revenue": (
            revenue_data["MonthlyCharges"].sum()
        ),
        "Total Annual Revenue": (
            revenue_data["AnnualRevenueExposure"].sum()
        ),
        "Expected Monthly Revenue Loss": (
            revenue_data[
                "ExpectedMonthlyRevenueLoss"
            ].sum()
        ),
        "Expected Annual Revenue Loss": (
            revenue_data[
                "ExpectedAnnualRevenueLoss"
            ].sum()
        ),
        "Lifetime Value at Risk": (
            revenue_data[
                "ExpectedLifetimeValueLoss"
            ].sum()
        ),
        "High-Risk Annual Revenue Exposure": (
            revenue_data.loc[
                high_risk_mask,
                "AnnualRevenueExposure"
            ].sum()
        ),
        "High-Value Annual Revenue at Risk": (
            revenue_data.loc[
                high_risk_mask & high_value_mask,
                "ExpectedAnnualRevenueLoss"
            ].sum()
        ),
        "Potential Annual Revenue Recovery": (
            revenue_data[
                "PotentialAnnualRevenueRecovery"
            ].sum()
        ),
        "Recovery Rate": recovery_rate
    }

    return kpis


def summarize_revenue_by_category(
    revenue_data,
    category_column
):
    """
    Aggregate financial exposure by a business category.
    """

    summary = (
        revenue_data
        .groupby(
            category_column,
            observed=False
        )
        .agg(
            Customers=(
                "MonthlyCharges",
                "size"
            ),
            MonthlyRevenue=(
                "MonthlyCharges",
                "sum"
            ),
            AnnualRevenueExposure=(
                "AnnualRevenueExposure",
                "sum"
            ),
            ExpectedAnnualRevenueLoss=(
                "ExpectedAnnualRevenueLoss",
                "sum"
            ),
            PotentialRevenueRecovery=(
                "PotentialAnnualRevenueRecovery",
                "sum"
            ),
            AverageChurnProbability=(
                "ChurnProbability",
                "mean"
            )
        )
        .reset_index()
    )

    summary["AverageChurnProbabilityPercent"] = (
        summary["AverageChurnProbability"]
        * 100
    ).round(2)

    financial_columns = [
        "MonthlyRevenue",
        "AnnualRevenueExposure",
        "ExpectedAnnualRevenueLoss",
        "PotentialRevenueRecovery"
    ]

    summary[financial_columns] = (
        summary[financial_columns]
        .round(2)
    )

    return summary
