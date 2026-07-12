
import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_predictions,
    load_executive_kpis
)


def format_currency(value):

    return f"${value:,.2f}"


def render():

    st.title("Executive Dashboard")

    st.caption(
        "Enterprise overview of customer retention, "
        "financial exposure, and business intelligence."
    )

    data = load_predictions()

    kpi_data = load_executive_kpis()

    # =====================================================
    # Executive KPIs
    # =====================================================

    total_customers = len(data)

    predicted_churn = (
        data["PredictedChurnClass"] == 1
    ).sum()

    churn_rate = (
        predicted_churn
        / total_customers
        * 100
    )

    average_probability = (
        data["ChurnProbabilityPercent"]
        .mean()
    )

    annual_revenue = (
        data["MonthlyCharges"].sum() * 12
    )

    annual_loss = (
        (
            data["MonthlyCharges"]
            * 12
            * data["ChurnProbability"]
        ).sum()
    )

    immediate_action = (
        data["RetentionPriority"]
        == "Immediate Action"
    ).sum()

    row1 = st.columns(4)

    with row1[0]:

        st.metric(
            "Customers",
            f"{total_customers:,}"
        )

    with row1[1]:

        st.metric(
            "Predicted Churn",
            f"{churn_rate:.2f}%"
        )

    with row1[2]:

        st.metric(
            "Annual Revenue",
            format_currency(
                annual_revenue
            )
        )

    with row1[3]:

        st.metric(
            "Expected Annual Loss",
            format_currency(
                annual_loss
            )
        )

    row2 = st.columns(4)

    with row2[0]:

        st.metric(
            "Average Risk",
            f"{average_probability:.2f}%"
        )

    with row2[1]:

        st.metric(
            "Immediate Action",
            f"{immediate_action:,}"
        )

    with row2[2]:

        st.metric(
            "High Risk",
            (
                data["RiskCategory"]
                .isin(["High","Critical"])
            ).sum()
        )

    with row2[3]:

        st.metric(
            "High Value Customers",
            (
                data["CustomerValueGroup"]
                == "High Value"
            ).sum()
        )

    st.markdown("---")

    # =====================================================
    # Dashboard Charts
    # =====================================================

    left,right = st.columns(2)

    with left:

        fig = px.pie(
            data,
            names="RiskCategory",
            title="Customer Risk Distribution",
            hole=.55
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(

            data.groupby(
                "BusinessSegment"
            )["MonthlyCharges"]
            .sum()
            .reset_index(),

            x="BusinessSegment",

            y="MonthlyCharges",

            color="BusinessSegment",

            title="Monthly Revenue by Business Segment"

        )

        fig.update_layout(
            template="plotly_dark",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    # =====================================================
    # Revenue Exposure
    # =====================================================

    st.subheader(
        "Revenue Exposure by Risk Category"
    )

    revenue = (

        data.groupby(
            "RiskCategory"
        )

        .agg(

            Customers=("MonthlyCharges","count"),

            AnnualRevenue=(

                "MonthlyCharges",

                lambda x:(x*12).sum()

            ),

            ExpectedLoss=(

                "ChurnProbability",

                "mean"

            )

        )

        .reset_index()

    )

    fig = px.bar(

        revenue,

        x="RiskCategory",

        y="AnnualRevenue",

        color="RiskCategory",

        title="Annual Revenue Exposure"

    )

    fig.update_layout(

        template="plotly_dark",

        showlegend=False

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.dataframe(

        revenue,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    # =====================================================
    # Top Priority Customers
    # =====================================================

    st.subheader(

        "Top Customers Requiring Immediate Attention"

    )

    top_customers = (

        data

        .sort_values(

            by="ChurnProbabilityPercent",

            ascending=False

        )

        .head(20)

    )

    preferred_columns = [

        "CustomerRiskRank",

        "ChurnProbabilityPercent",

        "RiskCategory",

        "CustomerValueScore",

        "BusinessSegment",

        "RecommendationPriorityScore",

        "ExpectedAnnualRevenueLoss"

    ]

    display_columns = [

        c

        for c in preferred_columns

        if c in top_customers.columns

    ]

    st.dataframe(

        top_customers[display_columns],

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    csv = data.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        "Download Executive Dashboard Data",

        csv,

        "executive_dashboard.csv",

        "text/csv",

        use_container_width=True

    )
