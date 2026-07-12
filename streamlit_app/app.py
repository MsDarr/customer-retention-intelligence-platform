# ============================================================
# Redesign Main Streamlit Application
# ============================================================

APP_FILE_PATH = os.path.join(
    APP_PATH,
    "app.py"
)

app_content = r'''
import pandas as pd
import plotly.express as px
import streamlit as st

from pages import (
    about,
    dashboard,
    executive_dashboard,
    prediction,
    recommendations,
    reports,
    revenue_intelligence,
    risk_scoring
)

from utils.data_loader import (
    load_model_assets,
    load_predictions
)


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Retention Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# Global Styling
# ============================================================

def apply_custom_style():

    st.markdown(
        """
        <style>

        /* Main application */
        .stApp {
            background:
                radial-gradient(
                    circle at 80% 0%,
                    rgba(76, 29, 149, 0.18),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 40% 10%,
                    rgba(37, 99, 235, 0.10),
                    transparent 30%
                ),
                #07101f;
            color: #f8fafc;
        }

        /* Main page spacing */
        .block-container {
            max-width: 1450px;
            padding-top: 1.4rem;
            padding-bottom: 3rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #050b17 0%,
                    #081225 100%
                );
            border-right: 1px solid #25304a;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }

        [data-testid="stSidebar"] * {
            color: #e2e8f0;
        }

        /* Navigation links */
        [data-testid="stSidebarNav"] a {
            border-radius: 10px;
            margin-bottom: 0.25rem;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(79, 70, 229, 0.20);
        }

        /* Hero */
        .hero {
            position: relative;
            overflow: hidden;
            min-height: 315px;
            padding: 2.4rem 2.6rem;
            margin-bottom: 1rem;
            border: 1px solid #283550;
            border-radius: 22px;
            background:
                radial-gradient(
                    circle at 83% 46%,
                    rgba(37, 99, 235, 0.32),
                    transparent 23%
                ),
                radial-gradient(
                    circle at 76% 45%,
                    rgba(124, 58, 237, 0.30),
                    transparent 38%
                ),
                linear-gradient(
                    135deg,
                    #101a31 0%,
                    #0c1630 47%,
                    #211153 100%
                );
            box-shadow: 0 22px 55px rgba(0, 0, 0, 0.30);
        }

        .hero::after {
            content: "🧠";
            position: absolute;
            right: 7%;
            top: 14%;
            font-size: 9.5rem;
            filter:
                drop-shadow(0 0 24px #2563eb)
                drop-shadow(0 0 48px #7c3aed);
            opacity: 0.94;
        }

        .welcome {
            color: #a78bfa;
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .hero-title {
            max-width: 720px;
            font-size: 3rem;
            line-height: 1.08;
            font-weight: 850;
            letter-spacing: -0.045em;
            margin-bottom: 1rem;
        }

        .gradient-text {
            background:
                linear-gradient(
                    90deg,
                    #60a5fa,
                    #8b5cf6,
                    #c084fc
                );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-description {
            max-width: 620px;
            color: #cbd5e1;
            font-size: 1.06rem;
            line-height: 1.7;
        }

        /* Section title */
        .section-header {
            margin-top: 1.3rem;
            margin-bottom: 0.9rem;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 800;
            margin: 0;
        }

        .section-caption {
            color: #94a3b8;
            font-size: 0.88rem;
            margin-top: 0.15rem;
        }

        /* KPI cards */
        .kpi-card {
            min-height: 150px;
            padding: 1.25rem;
            border-radius: 17px;
            border: 1px solid #293652;
            background:
                linear-gradient(
                    145deg,
                    rgba(25, 37, 63, 0.96),
                    rgba(10, 19, 36, 0.98)
                );
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.22);
        }

        .kpi-top {
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }

        .kpi-icon {
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            font-size: 1.45rem;
            background:
                linear-gradient(
                    135deg,
                    #4f46e5,
                    #7c3aed
                );
        }

        .kpi-label {
            color: #cbd5e1;
            font-size: 0.83rem;
            font-weight: 600;
        }

        .kpi-value {
            margin-top: 0.75rem;
            font-size: 1.8rem;
            font-weight: 850;
        }

        .kpi-caption {
            margin-top: 0.35rem;
            color: #94a3b8;
            font-size: 0.78rem;
        }

        /* Module cards */
        .module-card {
            min-height: 228px;
            padding: 1.2rem;
            border-radius: 17px;
            border: 1px solid #293652;
            background:
                linear-gradient(
                    160deg,
                    rgba(24, 37, 62, 0.98),
                    rgba(9, 18, 34, 0.98)
                );
            transition:
                transform 0.20s ease,
                border-color 0.20s ease,
                box-shadow 0.20s ease;
        }

        .module-card:hover {
            transform: translateY(-4px);
            border-color: #6366f1;
            box-shadow:
                0 15px 32px rgba(79, 70, 229, 0.15);
        }

        .module-icon {
            font-size: 2.1rem;
            margin-bottom: 0.8rem;
        }

        .module-title {
            font-size: 1rem;
            font-weight: 800;
            min-height: 48px;
        }

        .module-description {
            color: #aab8cc;
            font-size: 0.80rem;
            line-height: 1.55;
            min-height: 78px;
        }

        .module-action {
            margin-top: 0.7rem;
            color: #818cf8;
            font-size: 0.80rem;
            font-weight: 700;
        }

        /* Chart and table containers */
        [data-testid="stPlotlyChart"] {
            padding: 0.25rem;
            border: 1px solid #293652;
            border-radius: 17px;
            background: rgba(10, 19, 36, 0.92);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #293652;
            border-radius: 16px;
            overflow: hidden;
        }

        /* CTA */
        .cta-box {
            margin-top: 1.5rem;
            padding: 1.5rem 1.8rem;
            border-radius: 18px;
            border: 1px solid #4f46e5;
            background:
                linear-gradient(
                    100deg,
                    rgba(49, 46, 129, 0.82),
                    rgba(76, 29, 149, 0.78)
                );
        }

        .cta-title {
            font-size: 1.3rem;
            font-weight: 850;
        }

        .cta-text {
            color: #d8dffc;
            margin-top: 0.3rem;
        }

        /* Page link buttons */
        [data-testid="stPageLink"] a {
            border-radius: 11px;
            border: 1px solid #3b4a69;
            background:
                linear-gradient(
                    135deg,
                    #4338ca,
                    #6d28d9
                );
            color: white !important;
            font-weight: 750;
        }

        /* Footer */
        .footer {
            margin-top: 2rem;
            padding: 1.4rem 0;
            border-top: 1px solid #26334d;
            color: #8190a8;
            font-size: 0.8rem;
            text-align: center;
        }

        /* Mobile */
        @media (max-width: 900px) {

            .hero {
                min-height: 430px;
                padding: 1.7rem;
            }

            .hero::after {
                top: 52%;
                right: 31%;
                font-size: 7rem;
            }

            .hero-title {
                font-size: 2.15rem;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# Helper Components
# ============================================================

def metric_card(
    icon,
    label,
    value,
    caption
):

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def module_card(
    icon,
    title,
    description,
    action
):

    st.markdown(
        f"""
        <div class="module-card">
            <div class="module-icon">{icon}</div>
            <div class="module-title">{title}</div>
            <div class="module-description">
                {description}
            </div>
            <div class="module-action">
                {action} →
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(
    title,
    caption
):

    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-title">{title}</div>
            <div class="section-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# Home Page
# ============================================================

def render_home():

    data = load_predictions()

    model, feature_names, metadata = (
        load_model_assets()
    )

    metrics = metadata.get(
        "metrics",
        {}
    )

    total_customers = len(data)

    high_risk_customers = (
        data["RiskCategory"]
        .isin(["High", "Critical"])
        .sum()
    )

    revenue_at_risk = (
        data["MonthlyCharges"]
        .mul(12)
        .mul(data["ChurnProbability"])
        .sum()
    )

    model_accuracy = metrics.get(
        "Accuracy",
        0
    )

    model_name = metadata.get(
        "model_name",
        type(model).__name__
    )

    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hero">
            <div class="welcome">
                ✦ Welcome to Retention Intelligence
            </div>

            <div class="hero-title">
                AI-Powered Customer
                <span class="gradient-text">
                    Retention Intelligence
                </span>
            </div>

            <div class="hero-description">
                Predict customer churn, identify customers
                at risk, protect revenue, and generate
                intelligent retention strategies through
                one unified business platform.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    action1, action2, spacer = st.columns(
        [1.15, 1.25, 4]
    )

    with action1:

        st.page_link(
            prediction_page,
            label="Start Prediction",
            icon="🚀",
            width="stretch"
        )

    with action2:

        st.page_link(
            executive_page,
            label="Executive Dashboard",
            icon="📊",
            width="stretch"
        )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    section_header(
        "Live Business Metrics",
        "Current customer portfolio and model performance"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        metric_card(
            "👥",
            "Total Customers",
            f"{total_customers:,}",
            "Customer records analyzed"
        )

    with col2:

        metric_card(
            "⚠️",
            "High-Risk Customers",
            f"{high_risk_customers:,}",
            (
                f"{high_risk_customers / total_customers:.1%} "
                "of the customer base"
            )
        )

    with col3:

        metric_card(
            "💰",
            "Revenue at Risk",
            f"${revenue_at_risk / 1_000_000:.2f}M",
            "Probability-weighted annual exposure"
        )

    with col4:

        metric_card(
            "🎯",
            "Model Accuracy",
            f"{model_accuracy:.1%}",
            model_name
        )

    # --------------------------------------------------------
    # Modules
    # --------------------------------------------------------

    section_header(
        "Platform Modules",
        "AI and analytics tools for customer retention"
    )

    modules = [
        (
            "🔮",
            "Customer Prediction",
            "Generate real-time churn probabilities for individual customer profiles.",
            "Predict Now"
        ),
        (
            "🛡️",
            "Risk Scoring",
            "Identify, rank, and prioritize customers according to churn risk.",
            "View Risk Scores"
        ),
        (
            "🤖",
            "AI Recommendations",
            "Generate personalized retention actions, offers, and communication channels.",
            "Get Recommendations"
        ),
        (
            "💹",
            "Revenue Intelligence",
            "Estimate revenue exposure, expected loss, and potential recovery.",
            "Explore Revenue"
        ),
        (
            "📈",
            "Executive Dashboard",
            "Review high-level business KPIs and customer-retention performance.",
            "View Dashboard"
        ),
        (
            "📄",
            "Reports",
            "Preview and download operational customer-intelligence reports.",
            "View Reports"
        )
    ]

    module_columns = st.columns(6)

    for column, module in zip(
        module_columns,
        modules
    ):

        with column:

            module_card(*module)

    # --------------------------------------------------------
    # Business Insights
    # --------------------------------------------------------

    section_header(
        "Key Business Insights",
        "Overview of churn, risk, and revenue exposure"
    )

    chart1, chart2, chart3 = st.columns(3)

    with chart1:

        churn_column = (
            "ActualChurnLabel"
            if "ActualChurnLabel" in data.columns
            else "PredictedChurnLabel"
        )

        churn_summary = (
            data[churn_column]
            .value_counts()
            .reset_index()
        )

        churn_summary.columns = [
            "Customer Status",
            "Customers"
        ]

        churn_figure = px.pie(
            churn_summary,
            names="Customer Status",
            values="Customers",
            hole=0.64,
            title="Churn Distribution",
            color="Customer Status",
            color_discrete_sequence=[
                "#22c55e",
                "#ef4444"
            ]
        )

        churn_figure.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=25,
                r=25,
                t=55,
                b=25
            ),
            legend=dict(
                orientation="h",
                y=-0.08
            )
        )

        st.plotly_chart(
            churn_figure,
            use_container_width=True
        )

    with chart2:

        risk_order = [
            "Low",
            "Moderate",
            "High",
            "Critical"
        ]

        risk_summary = (
            data["RiskCategory"]
            .value_counts()
            .reindex(
                risk_order,
                fill_value=0
            )
            .reset_index()
        )

        risk_summary.columns = [
            "Risk Category",
            "Customers"
        ]

        risk_figure = px.bar(
            risk_summary,
            x="Risk Category",
            y="Customers",
            title="Customers by Risk Level",
            color="Risk Category",
            color_discrete_map={
                "Low": "#22c55e",
                "Moderate": "#eab308",
                "High": "#f97316",
                "Critical": "#ef4444"
            }
        )

        risk_figure.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(
                l=25,
                r=25,
                t=55,
                b=25
            )
        )

        st.plotly_chart(
            risk_figure,
            use_container_width=True
        )

    with chart3:

        revenue_summary = data.copy()

        revenue_summary[
            "ExpectedAnnualRevenueLoss"
        ] = (
            revenue_summary["MonthlyCharges"]
            * 12
            * revenue_summary["ChurnProbability"]
        )

        revenue_summary = (
            revenue_summary
            .groupby(
                "BusinessSegment",
                observed=False
            )[
                "ExpectedAnnualRevenueLoss"
            ]
            .sum()
            .sort_values(
                ascending=True
            )
            .reset_index()
        )

        revenue_figure = px.bar(
            revenue_summary,
            x="ExpectedAnnualRevenueLoss",
            y="BusinessSegment",
            orientation="h",
            title="Revenue at Risk by Segment",
            color="ExpectedAnnualRevenueLoss",
            color_continuous_scale=[
                "#22c55e",
                "#eab308",
                "#f97316",
                "#ef4444"
            ]
        )

        revenue_figure.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            margin=dict(
                l=25,
                r=25,
                t=55,
                b=25
            )
        )

        st.plotly_chart(
            revenue_figure,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Priority Activity
    # --------------------------------------------------------

    section_header(
        "Priority Customer Activity",
        "Customers requiring the greatest retention attention"
    )

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

    priority_customers = (
        data
        .sort_values(
            by="ChurnProbabilityPercent",
            ascending=False
        )
        .head(8)
    )

    st.dataframe(
        priority_customers[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # CTA
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="cta-box">
            <div class="cta-title">
                🚀 Ready to reduce churn and protect revenue?
            </div>
            <div class="cta-text">
                Use AI-powered customer intelligence to
                identify risk early and take targeted action.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        prediction_page,
        label="Get Started Now",
        icon="✨",
        width="stretch"
    )


# ============================================================
# Navigation Pages
# ============================================================

prediction_page = st.Page(
    prediction.render,
    title="Customer Prediction",
    icon="🔮",
    url_path="prediction"
)

risk_page = st.Page(
    risk_scoring.render,
    title="Risk Scoring",
    icon="⚠️",
    url_path="risk-scoring"
)

recommendations_page = st.Page(
    recommendations.render,
    title="AI Recommendations",
    icon="🤖",
    url_path="recommendations"
)

revenue_page = st.Page(
    revenue_intelligence.render,
    title="Revenue Intelligence",
    icon="💰",
    url_path="revenue-intelligence"
)

dashboard_page = st.Page(
    dashboard.render,
    title="Dashboard",
    icon="📊",
    url_path="dashboard"
)

executive_page = st.Page(
    executive_dashboard.render,
    title="Executive Dashboard",
    icon="📈",
    url_path="executive-dashboard"
)

reports_page = st.Page(
    reports.render,
    title="Reports",
    icon="📄",
    url_path="reports"
)

about_page = st.Page(
    about.render,
    title="About",
    icon="ℹ️",
    url_path="about"
)

home_page = st.Page(
    render_home,
    title="Home",
    icon="🏠",
    default=True,
    url_path="home"
)


# ============================================================
# Run Navigation
# ============================================================

apply_custom_style()

navigation = st.navigation(
    [
        home_page,
        dashboard_page,
        prediction_page,
        risk_page,
        recommendations_page,
        revenue_page,
        executive_page,
        reports_page,
        about_page
    ],
    position="sidebar"
)

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 0.4rem 0 1.1rem 0;
            text-align: center;
        ">
            <div style="
                font-size: 3rem;
                filter: drop-shadow(
                    0 0 12px #4f46e5
                );
            ">
                📈
            </div>

            <div style="
                font-weight: 850;
                font-size: 1.15rem;
                letter-spacing: 0.04em;
            ">
                RETENTION
                <br>
                INTELLIGENCE
            </div>

            <div style="
                color: #818cf8;
                font-size: 0.68rem;
                margin-top: 0.35rem;
            ">
                AI-POWERED PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

navigation.run()

st.markdown(
    """
    <div class="footer">
        AI-Powered Customer Retention Intelligence Platform
        &nbsp; | &nbsp;
        Built with Python, Machine Learning, and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
'''

with open(
    APP_FILE_PATH,
    "w",
    encoding="utf-8"
) as file:
    file.write(app_content)

print("New SaaS-style homepage created successfully.")
print(APP_FILE_PATH)


import py_compile

try:
    py_compile.compile(
        APP_FILE_PATH,
        doraise=True
    )

    print("✓ New app.py syntax validation passed.")

except py_compile.PyCompileError as error:
    print("✗ Syntax validation failed.")
    print(error)