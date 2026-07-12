
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_predictions
)

from utils.revenue_engine import (
    validate_revenue_columns,
    calculate_revenue_metrics,
    calculate_revenue_kpis,
    summarize_revenue_by_category
)


def format_currency(value):

    return f"${value:,.2f}"


def render():

    st.title("Revenue Intelligence")

    st.caption(
        "Measure revenue exposure, expected financial "
        "loss, and potential recovery associated with "
        "predicted customer churn."
    )

    data = load_predictions().copy()

    missing_columns = validate_revenue_columns(
        data
    )

    if missing_columns:

        st.error(
            "The prediction dataset is missing "
            "required revenue-intelligence columns."
        )

        st.write(missing_columns)
        return

    # --------------------------------------------------------
    # Revenue assumptions
    # --------------------------------------------------------

    st.sidebar.subheader(
        "Revenue Assumptions"
    )

    recovery_rate_percent = st.sidebar.slider(
        "Expected Retention Recovery Rate (%)",
        min_value=0,
        max_value=100,
        value=30,
        step=5,
        help=(
            "Estimated percentage of expected annual "
            "revenue loss that could be recovered "
            "through successful retention campaigns."
        )
    )

    recovery_rate = (
        recovery_rate_percent / 100
    )

    selected_risk_categories = (
        st.sidebar.multiselect(
            "Risk Categories",
            [
                "Low",
                "Moderate",
                "High",
                "Critical"
            ],
            default=[
                "Low",
                "Moderate",
                "High",
                "Critical"
            ]
        )
    )

    revenue_data = calculate_revenue_metrics(
        data,
        recovery_rate=recovery_rate
    )

    filtered_data = revenue_data[
        revenue_data["RiskCategory"].isin(
            selected_risk_categories
        )
    ].copy()

    if filtered_data.empty:

        st.warning(
            "No customers match the selected filters."
        )
        return

    kpis = calculate_revenue_kpis(
        filtered_data,
        recovery_rate=recovery_rate
    )

    # --------------------------------------------------------
    # Executive KPIs
    # --------------------------------------------------------

    st.subheader(
        "Executive Revenue Overview"
    )

    row1 = st.columns(4)

    with row1[0]:

        st.metric(
            "Monthly Revenue",
            format_currency(
                kpis["Total Monthly Revenue"]
            )
        )

    with row1[1]:

        st.metric(
            "Annual Revenue",
            format_currency(
                kpis["Total Annual Revenue"]
            )
        )

    with row1[2]:

        st.metric(
            "Expected Annual Loss",
            format_currency(
                kpis[
                    "Expected Annual Revenue Loss"
                ]
            )
        )

    with row1[3]:

        st.metric(
            "Potential Recovery",
            format_currency(
                kpis[
                    "Potential Annual Revenue Recovery"
                ]
            ),
            delta=(
                f"{recovery_rate_percent}% "
                "recovery assumption"
            )
        )

    row2 = st.columns(3)

    with row2[0]:

        st.metric(
            "Lifetime Value at Risk",
            format_currency(
                kpis["Lifetime Value at Risk"]
            )
        )

    with row2[1]:

        st.metric(
            "High-Risk Revenue Exposure",
            format_currency(
                kpis[
                    "High-Risk Annual Revenue Exposure"
                ]
            )
        )

    with row2[2]:

        st.metric(
            "High-Value Revenue at Risk",
            format_currency(
                kpis[
                    "High-Value Annual Revenue at Risk"
                ]
            )
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Revenue by risk category
    # --------------------------------------------------------

    st.subheader(
        "Revenue Exposure by Risk Category"
    )

    risk_summary = summarize_revenue_by_category(
        filtered_data,
        "RiskCategory"
    )

    risk_order = [
        "Low",
        "Moderate",
        "High",
        "Critical"
    ]

    risk_summary["RiskCategory"] = (
        pd.Categorical(
            risk_summary["RiskCategory"],
            categories=risk_order,
            ordered=True
        )
    )

    risk_summary = risk_summary.sort_values(
        "RiskCategory"
    )

    left, right = st.columns(2)

    with left:

        fig_risk_loss = px.bar(
            risk_summary,
            x="RiskCategory",
            y="ExpectedAnnualRevenueLoss",
            color="RiskCategory",
            color_discrete_map={
                "Low": "#059669",
                "Moderate": "#F59E0B",
                "High": "#F97316",
                "Critical": "#DC2626"
            },
            title=(
                "Expected Annual Revenue Loss "
                "by Risk Category"
            ),
            labels={
                "ExpectedAnnualRevenueLoss":
                "Expected Annual Revenue Loss",
                "RiskCategory":
                "Risk Category"
            }
        )

        fig_risk_loss.update_layout(
            showlegend=False,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_risk_loss,
            use_container_width=True
        )

    with right:

        fig_recovery = px.bar(
            risk_summary,
            x="RiskCategory",
            y="PotentialRevenueRecovery",
            color="RiskCategory",
            color_discrete_map={
                "Low": "#059669",
                "Moderate": "#F59E0B",
                "High": "#F97316",
                "Critical": "#DC2626"
            },
            title=(
                "Potential Revenue Recovery "
                "by Risk Category"
            ),
            labels={
                "PotentialRevenueRecovery":
                "Potential Revenue Recovery",
                "RiskCategory":
                "Risk Category"
            }
        )

        fig_recovery.update_layout(
            showlegend=False,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_recovery,
            use_container_width=True
        )

    st.dataframe(
        risk_summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Revenue by business segment
    # --------------------------------------------------------

    if "BusinessSegment" in filtered_data.columns:

        st.subheader(
            "Revenue Exposure by Business Segment"
        )

        segment_summary = (
            summarize_revenue_by_category(
                filtered_data,
                "BusinessSegment"
            )
        )

        fig_segment = px.bar(
            segment_summary,
            x="BusinessSegment",
            y="ExpectedAnnualRevenueLoss",
            color="BusinessSegment",
            title=(
                "Expected Annual Revenue Loss "
                "by Business Segment"
            ),
            labels={
                "ExpectedAnnualRevenueLoss":
                "Expected Annual Revenue Loss",
                "BusinessSegment":
                "Business Segment"
            }
        )

        fig_segment.update_layout(
            template="plotly_dark",
            showlegend=False
        )

        st.plotly_chart(
            fig_segment,
            use_container_width=True
        )

        st.dataframe(
            segment_summary,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Top revenue-risk customers
    # --------------------------------------------------------

    st.subheader(
        "Top Customers by Expected Revenue Loss"
    )

    top_n = st.slider(
        "Number of Customers to Display",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )

    top_revenue_risk = (
        filtered_data
        .sort_values(
            by="ExpectedAnnualRevenueLoss",
            ascending=False
        )
        .head(top_n)
    )

    preferred_columns = [
        "CustomerRiskRank",
        "ChurnProbabilityPercent",
        "RiskCategory",
        "RetentionPriority",
        "MonthlyCharges",
        "CustomerLifetimeValue",
        "CustomerValueScore",
        "BusinessSegment",
        "ExpectedAnnualRevenueLoss",
        "PotentialAnnualRevenueRecovery"
    ]

    display_columns = [
        column
        for column in preferred_columns
        if column in top_revenue_risk.columns
    ]

    st.dataframe(
        top_revenue_risk[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Revenue-risk scatter plot
    # --------------------------------------------------------

    if "CustomerValueScore" in filtered_data.columns:

        st.subheader(
            "Customer Value and Expected Revenue Loss"
        )

        color_column = (
            "BusinessSegment"
            if "BusinessSegment"
            in filtered_data.columns
            else "RiskCategory"
        )

        fig_scatter = px.scatter(
            filtered_data,
            x="CustomerValueScore",
            y="ExpectedAnnualRevenueLoss",
            color=color_column,
            size="MonthlyCharges",
            hover_data=[
                "ChurnProbabilityPercent",
                "RiskCategory"
            ],
            title=(
                "Customer Value vs Expected "
                "Annual Revenue Loss"
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
    # Download revenue report
    # --------------------------------------------------------

    revenue_report = (
        filtered_data
        .sort_values(
            by="ExpectedAnnualRevenueLoss",
            ascending=False
        )
    )

    csv_data = revenue_report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Revenue Intelligence Report",
        data=csv_data,
        file_name=(
            "customer_revenue_intelligence.csv"
        ),
        mime="text/csv",
        use_container_width=True
    )
