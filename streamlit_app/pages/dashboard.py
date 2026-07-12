
import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_predictions
)


def render():

    st.title("Customer Retention Dashboard")

    st.caption(
        "Portfolio overview of predicted churn, "
        "customer risk, value, and retention priorities."
    )

    data = load_predictions().copy()

    total_customers = len(data)

    predicted_churn = (
        data["PredictedChurnClass"] == 1
    ).sum()

    high_risk = (
        data["RiskCategory"]
        .isin(["High", "Critical"])
    ).sum()

    immediate_action = (
        data["RetentionPriority"]
        == "Immediate Action"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col2:
        st.metric(
            "Predicted Churn",
            f"{predicted_churn:,}"
        )

    with col3:
        st.metric(
            "High/Critical Risk",
            f"{high_risk:,}"
        )

    with col4:
        st.metric(
            "Immediate Action",
            f"{immediate_action:,}"
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        risk_summary = (
            data["RiskCategory"]
            .value_counts()
            .reset_index()
        )

        risk_summary.columns = [
            "Risk Category",
            "Customers"
        ]

        fig_risk = px.bar(
            risk_summary,
            x="Risk Category",
            y="Customers",
            color="Risk Category",
            title="Customer Risk Distribution",
            color_discrete_map={
                "Low": "#059669",
                "Moderate": "#F59E0B",
                "High": "#F97316",
                "Critical": "#DC2626"
            }
        )

        fig_risk.update_layout(
            template="plotly_dark",
            showlegend=False
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

    with right:

        segment_summary = (
            data["BusinessSegment"]
            .value_counts()
            .reset_index()
        )

        segment_summary.columns = [
            "Business Segment",
            "Customers"
        ]

        fig_segment = px.pie(
            segment_summary,
            names="Business Segment",
            values="Customers",
            hole=0.55,
            title="Strategic Business Segments"
        )

        fig_segment.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_segment,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("Highest-Risk Customers")

    preferred_columns = [
        "CustomerRiskRank",
        "ChurnProbabilityPercent",
        "RiskCategory",
        "RetentionPriority",
        "CustomerValueScore",
        "CustomerRiskScore",
        "BusinessSegment"
    ]

    display_columns = [
        column
        for column in preferred_columns
        if column in data.columns
    ]

    top_customers = (
        data
        .sort_values(
            "ChurnProbabilityPercent",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        top_customers[display_columns],
        use_container_width=True,
        hide_index=True
    )
