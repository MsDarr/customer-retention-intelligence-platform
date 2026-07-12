
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_predictions
)


def render():

    st.title("Risk Scoring Engine")

    st.caption(
        "Explore customer churn risk, retention priority, "
        "and customer value across the portfolio."
    )

    data = load_predictions().copy()

    required_columns = [
        "CustomerRiskRank",
        "ChurnProbabilityPercent",
        "RiskCategory",
        "RetentionPriority"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:

        st.error(
            "The prediction dataset is missing "
            "required risk-scoring columns."
        )

        st.write(missing_columns)
        return

    # --------------------------------------------------------
    # Sidebar filters
    # --------------------------------------------------------

    st.sidebar.subheader("Risk Filters")

    risk_options = [
        "All",
        "Low",
        "Moderate",
        "High",
        "Critical"
    ]

    selected_risk = st.sidebar.selectbox(
        "Risk Category",
        risk_options
    )

    priority_options = [
        "All",
        "Low Priority",
        "Monitor",
        "High Priority",
        "Immediate Action"
    ]

    selected_priority = st.sidebar.selectbox(
        "Retention Priority",
        priority_options
    )

    minimum_probability = st.sidebar.slider(
        "Minimum Churn Probability (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )

    filtered = data.copy()

    if selected_risk != "All":

        filtered = filtered[
            filtered["RiskCategory"]
            == selected_risk
        ]

    if selected_priority != "All":

        filtered = filtered[
            filtered["RetentionPriority"]
            == selected_priority
        ]

    filtered = filtered[
        filtered["ChurnProbabilityPercent"]
        >= minimum_probability
    ]

    # --------------------------------------------------------
    # KPI summary
    # --------------------------------------------------------

    total_customers = len(data)

    critical_customers = (
        data["RiskCategory"] == "Critical"
    ).sum()

    high_customers = (
        data["RiskCategory"] == "High"
    ).sum()

    immediate_action = (
        data["RetentionPriority"]
        == "Immediate Action"
    ).sum()

    average_probability = (
        data["ChurnProbabilityPercent"]
        .mean()
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:

        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with kpi2:

        st.metric(
            "Critical Risk",
            f"{critical_customers:,}"
        )

    with kpi3:

        st.metric(
            "High Risk",
            f"{high_customers:,}"
        )

    with kpi4:

        st.metric(
            "Average Risk",
            f"{average_probability:.2f}%"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Risk distribution
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        risk_summary = (
            data["RiskCategory"]
            .value_counts()
            .reindex(
                [
                    "Low",
                    "Moderate",
                    "High",
                    "Critical"
                ],
                fill_value=0
            )
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
            color_discrete_map={
                "Low": "#059669",
                "Moderate": "#F59E0B",
                "High": "#F97316",
                "Critical": "#DC2626"
            },
            title="Customer Risk Distribution"
        )

        fig_risk.update_layout(
            showlegend=False,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

    with right:

        priority_summary = (
            data["RetentionPriority"]
            .value_counts()
            .reindex(
                [
                    "Low Priority",
                    "Monitor",
                    "High Priority",
                    "Immediate Action"
                ],
                fill_value=0
            )
            .reset_index()
        )

        priority_summary.columns = [
            "Retention Priority",
            "Customers"
        ]

        fig_priority = px.pie(
            priority_summary,
            names="Retention Priority",
            values="Customers",
            hole=0.55,
            title="Retention Priority Distribution"
        )

        fig_priority.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_priority,
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # High-risk portfolio
    # --------------------------------------------------------

    st.subheader("Customer Risk Portfolio")

    st.write(
        f"Showing {len(filtered):,} customers "
        f"after applying filters."
    )

    preferred_columns = [
        "CustomerRiskRank",
        "ChurnProbabilityPercent",
        "RiskCategory",
        "RetentionPriority",
        "CustomerValueScore",
        "CustomerRiskScore",
        "CustomerLifetimeValue",
        "BusinessSegment"
    ]

    display_columns = [
        column
        for column in preferred_columns
        if column in filtered.columns
    ]

    filtered_display = (
        filtered[display_columns]
        .sort_values(
            by="ChurnProbabilityPercent",
            ascending=False
        )
    )

    st.dataframe(
        filtered_display,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Value vs risk scatter plot
    # --------------------------------------------------------

    if (
        "CustomerValueScore" in data.columns
        and "BusinessSegment" in data.columns
    ):

        st.subheader(
            "Customer Value vs Churn Risk"
        )

        fig_scatter = px.scatter(
            data,
            x="CustomerValueScore",
            y="ChurnProbabilityPercent",
            color="BusinessSegment",
            hover_data=[
                "RiskCategory",
                "RetentionPriority"
            ],
            title=(
                "Customer Value and "
                "Predicted Churn Risk"
            ),
            opacity=0.65
        )

        fig_scatter.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Download filtered risk report
    # --------------------------------------------------------

    csv_data = filtered_display.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Risk Report",
        data=csv_data,
        file_name=(
            "filtered_customer_risk_report.csv"
        ),
        mime="text/csv",
        use_container_width=True
    )
