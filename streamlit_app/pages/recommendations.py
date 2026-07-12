
import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_recommendations
)


def render():

    st.title("AI Recommendation Engine")

    st.caption(
        "Review personalized customer retention actions, "
        "offers, communication channels, and recommendation priorities."
    )

    data = load_recommendations().copy()

    required_columns = [
        "RecommendedAction",
        "RecommendedOffer",
        "RecommendedChannel",
        "RecommendationReason",
        "RecommendationPriorityScore",
        "BusinessSegment",
        "RiskCategory"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:

        st.error(
            "The recommendation dataset is missing "
            "required columns."
        )

        st.write(missing_columns)
        return

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.sidebar.subheader("Recommendation Filters")

    segment_options = [
        "All"
    ] + sorted(
        data["BusinessSegment"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_segment = st.sidebar.selectbox(
        "Business Segment",
        segment_options
    )

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

    minimum_priority = st.sidebar.slider(
        "Minimum Recommendation Priority Score",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )

    filtered = data.copy()

    if selected_segment != "All":
        filtered = filtered[
            filtered["BusinessSegment"]
            == selected_segment
        ]

    if selected_risk != "All":
        filtered = filtered[
            filtered["RiskCategory"]
            == selected_risk
        ]

    filtered = filtered[
        filtered["RecommendationPriorityScore"]
        >= minimum_priority
    ]

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_recommendations = len(data)

    immediate_actions = (
        data["RecommendedAction"]
        == "Immediate personalized retention outreach"
    ).sum()

    retention_offers = (
        data["RecommendedOffer"]
        != "No immediate financial incentive required"
    ).sum()

    average_priority = (
        data["RecommendationPriorityScore"]
        .mean()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Recommendations",
            f"{total_recommendations:,}"
        )

    with col2:
        st.metric(
            "Immediate Outreach",
            f"{immediate_actions:,}"
        )

    with col3:
        st.metric(
            "Customers with Offers",
            f"{retention_offers:,}"
        )

    with col4:
        st.metric(
            "Average Priority Score",
            f"{average_priority:.2f}"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Recommendation summaries
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        action_summary = (
            data["RecommendedAction"]
            .value_counts()
            .reset_index()
        )

        action_summary.columns = [
            "Recommended Action",
            "Customers"
        ]

        fig_actions = px.bar(
            action_summary,
            x="Customers",
            y="Recommended Action",
            orientation="h",
            color="Recommended Action",
            title="Recommended Action Distribution"
        )

        fig_actions.update_layout(
            template="plotly_dark",
            showlegend=False
        )

        st.plotly_chart(
            fig_actions,
            use_container_width=True
        )

    with right:

        channel_summary = (
            data["RecommendedChannel"]
            .value_counts()
            .reset_index()
        )

        channel_summary.columns = [
            "Communication Channel",
            "Customers"
        ]

        fig_channels = px.pie(
            channel_summary,
            names="Communication Channel",
            values="Customers",
            hole=0.55,
            title="Recommended Communication Channels"
        )

        fig_channels.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_channels,
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Recommendation portfolio
    # --------------------------------------------------------

    st.subheader("Customer Recommendation Portfolio")

    st.write(
        f"Showing {len(filtered):,} customers "
        f"after applying filters."
    )

    preferred_columns = [
        "RecommendationRank",
        "RecommendationPriorityScore",
        "ChurnProbabilityPercent",
        "RiskCategory",
        "CustomerValueScore",
        "BusinessSegment",
        "RecommendedAction",
        "RecommendedOffer",
        "RecommendedChannel",
        "RecommendationReason"
    ]

    display_columns = [
        column
        for column in preferred_columns
        if column in filtered.columns
    ]

    filtered_display = (
        filtered[display_columns]
        .sort_values(
            by="RecommendationPriorityScore",
            ascending=False
        )
    )

    st.dataframe(
        filtered_display,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Offer summary
    # --------------------------------------------------------

    st.subheader("Retention Offer Distribution")

    offer_summary = (
        data["RecommendedOffer"]
        .value_counts()
        .reset_index()
    )

    offer_summary.columns = [
        "Recommended Offer",
        "Customers"
    ]

    fig_offers = px.bar(
        offer_summary,
        x="Customers",
        y="Recommended Offer",
        orientation="h",
        color="Recommended Offer",
        title="Recommended Retention Offers"
    )

    fig_offers.update_layout(
        template="plotly_dark",
        showlegend=False
    )

    st.plotly_chart(
        fig_offers,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Top priority customers
    # --------------------------------------------------------

    st.subheader("Highest-Priority Recommendations")

    top_n = st.slider(
        "Number of Recommendations to Display",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )

    top_priority = (
        filtered
        .sort_values(
            by="RecommendationPriorityScore",
            ascending=False
        )
        .head(top_n)
    )

    st.dataframe(
        top_priority[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    csv_data = filtered_display.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Recommendations",
        data=csv_data,
        file_name=(
            "filtered_customer_recommendations.csv"
        ),
        mime="text/csv",
        use_container_width=True
    )
