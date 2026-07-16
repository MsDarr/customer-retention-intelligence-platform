from os import link

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
    risk_scoring,
)

from utils.data_loader import (
    load_model_assets,
    load_predictions,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retention Intelligence",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

def apply_custom_style() -> None:
    """Apply the global visual design for the Streamlit app."""

    st.markdown(
        """
<style>
@import url(
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded"
);

.material-symbols-rounded {
    font-family: "Material Symbols Rounded";
    font-weight: normal;
    font-style: normal;
    font-size: 1.55rem;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    direction: ltr;
    font-feature-settings: "liga";
    -webkit-font-feature-settings: "liga";
    -webkit-font-smoothing: antialiased;
}
.material-symbols-rounded {S
    font-family: "Material Symbols Rounded";
    font-weight: normal;
    font-style: normal;
    font-size: 1.6rem;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    direction: ltr;
    font-feature-settings: "liga";
    -webkit-font-feature-settings: "liga";
    -webkit-font-smoothing: antialiased;
}


/* =========================================================
   GLOBAL APPLICATION 
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(76, 29, 149, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 40% 10%,
            rgba(37, 99, 235, 0.08),
            transparent 30%
        ),
        #07101f;

    color: #f8fafc;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #050b17 0%,
            #071225 60%,
            #061020 100%
        );

    border-right: 1px solid rgba(99, 102, 241, 0.20);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}


/* Sidebar brand generated through CSS */

[data-testid="stSidebarNav"]::before {
    content:
        "◈"
        "\\A"
        "RETENTION INTELLIGENCE"
        "\\A"
        "AI-POWERED PLATFORM";

    white-space: pre-line;
    display: block;

    margin: 0.4rem 0.7rem 1.3rem;
    padding: 1rem 0.8rem 1.35rem;

    border-bottom: 1px solid rgba(100, 116, 139, 0.26);

    color: #f8fafc;
    text-align: center;

    font-size: 0.94rem;
    font-weight: 850;
    line-height: 1.6;
    letter-spacing: 0.055em;

    background:
        radial-gradient(
            circle at 50% 18%,
            rgba(99, 102, 241, 0.22),
            transparent 30%
        );
}


/* Navigation links */

[data-testid="stSidebarNav"] ul {
    gap: 0.20rem;
}

[data-testid="stSidebarNav"] a {
    min-height: 43px;
    padding: 0.60rem 0.8rem;

    border: 1px solid transparent;
    border-radius: 10px;

    color: #cbd5e1;
    font-weight: 620;

    transition:
        background 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease;
}

[data-testid="stSidebarNav"] a:hover {
    transform: translateX(3px);

    border-color: rgba(99, 102, 241, 0.30);

    background:
        linear-gradient(
            90deg,
            rgba(37, 99, 235, 0.16),
            rgba(124, 58, 237, 0.16)
        );
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #ffffff;

    border-color: rgba(129, 140, 248, 0.40);

    background:
        linear-gradient(
            90deg,
            rgba(51, 65, 85, 0.95),
            rgba(71, 85, 105, 0.85)
        );
}

[data-testid="stSidebarNav"] svg {
    width: 19px;
    height: 19px;
}


/* Sidebar message */

[data-testid="stSidebarNav"]::after {
    content: "Smarter decisions. Stronger relationships.";

    display: block;

    margin: 1.5rem 0.9rem 0;
    padding: 0.95rem;

    border: 1px solid rgba(99, 102, 241, 0.24);
    border-radius: 14px;

    color: #94a3b8;
    text-align: center;

    font-size: 0.72rem;
    line-height: 1.55;

    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.60),
            rgba(15, 23, 42, 0.82)
        );
}


/* =========================================================
   TEXT-ONLY HERO
   ========================================================= */

.hero-shell {
    position: relative;
    overflow: hidden;

    min-height: 420px;
    padding: 3rem 3.2rem;

    border: 1px solid rgba(99, 102, 241, 0.30);
    border-radius: 26px;

    background:
        radial-gradient(
            circle at 82% 36%,
            rgba(37, 99, 235, 0.28),
            transparent 24%
        ),
        radial-gradient(
        circle at 74% 48%,
        rgba(126, 34, 206, 0.18),
        transparent 35%
        )
        linear-gradient(
            135deg,
            #091226 0%,
            #0b1530 48%,
            #1b0d4a 100%
        );

    box-shadow:
        0 25px 65px rgba(0, 0, 0, 0.34),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.hero-shell::before {
    content: "";

    position: absolute;
    width: 420px;
    height: 420px;

    right: -80px;
    top: -110px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(96, 165, 250, 0.20),
            rgba(124, 58, 237, 0.08) 45%,
            transparent 68%
        );
    filter: blur(5px);
}

.hero-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1.5fr 0.8fr;
    align-items: center;
    gap: 2rem;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    
    width: fit-content;

    padding: 0.55rem 0.95rem;
    margin-bottom: 1.25rem;

    border: 1px solid rgba(129, 140, 248, 0.40);
    border-radius: 999px;

    background: rgba(49, 46, 129, 0.18);

    color: #a5b4fc;

    font-size: 0.78rem;
    font-weight: 750;
    letter-spacing: 0.06em;
}

.hero-title {
    max-width: 780px;
    margin: 0;

    color: #f8fafc;

    font-size: clamp(2.5rem, 4.8vw, 4.4rem);
    font-weight: 900;

    line-height: 1.04;
    letter-spacing: -0.055em;
}

.hero-gradient {
    background:
        linear-gradient(
            90deg,
            #3b82f6 0%,
            #6366f1 38%,
            #a855f7 72%,
            #d946ef 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-description {
    max-width: 670px;

    margin-top: 1.35rem;
    padding-left: 1.15rem;

    border-left: 3px solid #7c3aed;

    color: #cbd5e1;

    font-size: 1.08rem;
    line-height: 1.75;
}
.hero-benefit {
    padding: 0.65rem 0.95rem;
    border: 1px solid rgba(71, 85, 105, 0.65);
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.62);
    color: #dbeafe;
    font-size: 0.82rem;
    font-weight: 650;
}
.hero-visual {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 300px;
}

.hero-buttons {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}


/* =========================================================
   SECTION HEADERS
   ========================================================= */

.section-header {
    margin-top: 1.6rem;
    margin-bottom: 0.9rem;
}

.section-title {
    margin: 0;

    color: #f8fafc;

    font-size: 1.35rem;
    font-weight: 820;
}

.section-caption {
    margin-top: 0.15rem;

    color: #94a3b8;

    font-size: 0.87rem;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

.kpi-card {
    min-height: 150px;
    padding: 1.2rem;

    border: 1px solid #293652;
    border-radius: 17px;

    background:
        linear-gradient(
            145deg,
            rgba(25, 37, 63, 0.96),
            rgba(10, 19, 36, 0.98)
        );

    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.20);

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        box-shadow 0.18s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);

    border-color: rgba(99, 102, 241, 0.55);

    box-shadow:
        0 16px 38px rgba(79, 70, 229, 0.14);
}

.kpi-top {
    display: flex;
    align-items: center;
    gap: 0.70rem;
}

.kpi-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 44px;
    height: 44px;

    border-radius: 13px;

    font-size: 1.35rem;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );
}

.kpi-label {
    color: #cbd5e1;

    font-size: 0.81rem;
    font-weight: 650;
}

.kpi-value {
    margin-top: 0.78rem;

    color: #f8fafc;

    font-size: 1.82rem;
    font-weight: 860;
}

.kpi-caption {
    margin-top: 0.35rem;

    color: #94a3b8;

    font-size: 0.77rem;
    line-height: 1.45;
}


/* =========================================================
   MODULE CARDS
   ========================================================= */

.module-card {
    min-height: 225px;
    padding: 1.15rem;

    border: 1px solid #293652;
    border-radius: 17px;

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
    margin-bottom: 0.8rem;

    font-size: 1.9rem;
}

.module-title {
    min-height: 48px;

    color: #f8fafc;

    font-size: 0.96rem;
    font-weight: 800;
}

.module-description {
    min-height: 78px;

    color: #aab8cc;

    font-size: 0.78rem;
    line-height: 1.55;
}

.module-action {
    margin-top: 0.7rem;

    color: #818cf8;

    font-size: 0.78rem;
    font-weight: 700;
}


/* =========================================================
   CHARTS AND TABLES
   ========================================================= */

[data-testid="stPlotlyChart"] {
    padding: 0.20rem;

    border: 1px solid #293652;
    border-radius: 17px;

    background: rgba(10, 19, 36, 0.92);
}

[data-testid="stDataFrame"] {
    overflow: hidden;

    border: 1px solid #293652;
    border-radius: 16px;
}


/* =========================================================
   PAGE LINKS
   ========================================================= */

[data-testid="stPageLink"] a {
    min-height: 50px;

    justify-content: center;

    border: 1px solid #3b4a69;
    border-radius: 11px;

    color: white !important;

    font-weight: 750;

    background:
        linear-gradient(
            135deg,
            #4338ca,
            #6d28d9
        );

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

[data-testid="stPageLink"] a:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 30px rgba(79, 70, 229, 0.28);
}


/* =========================================================
   CALL TO ACTION
   ========================================================= */

.cta-box {
    margin-top: 1.6rem;
    padding: 1.55rem 1.8rem;

    border: 1px solid rgba(129, 140, 248, 0.38);
    border-radius: 18px;

    background:
        linear-gradient(
            105deg,
            rgba(49, 46, 129, 0.85),
            rgba(76, 29, 149, 0.82)
        );

    box-shadow:
        0 16px 42px rgba(0, 0, 0, 0.24);
}

.cta-title {
    color: #ffffff;

    font-size: 1.28rem;
    font-weight: 850;
}

.cta-text {
    margin-top: 0.35rem;

    color: #d8dffc;

    line-height: 1.6;
}

.cta-link-space {
    height: 16px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    margin-top: 2rem;
    padding: 1.4rem 0;

    border-top: 1px solid #26334d;

    color: #8190a8;

    font-size: 0.77rem;
    text-align: center;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding-top: 1rem;
    }

    .hero-shell {
        min-height: auto;
        padding: 2rem;
    }

    .hero-title {
        font-size: 2.35rem;
    }

    .hero-description {
        font-size: 0.96rem;
    }

    .kpi-card {
        min-height: 135px;
    }
}

</style>
        """,
        unsafe_allow_html=True,
    )
# ============================================================
# HELPER COMPONENTS
# ============================================================

def section_header(title: str, caption: str) -> None:
    """Render a page-section heading."""

    st.markdown(
        f"""
<div class="section-header">
    <div class="section-title">{title}</div>
    <div class="section-caption">{caption}</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(
    icon: str,
    label: str,
    value: str,
    caption: str,
) -> None:
    """Render one KPI with Material icon."""

    card_html = (
        '<div class="kpi-card">'
        '<div class="kpi-top">'
        '<div class="kpi-icon">'
        f'<span class="material-symbols-rounded">{icon}</span>'
        '</div>'
        f'<div class="kpi-label">{label}</div>'
        '</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-caption">{caption}</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )

    #st.markdown(
     #   f"""
#<div class="kpi-card">
 #   <div class="kpi-top">
  #      <div class="kpi-icon">{icon}</div>
   #     <div class="kpi-label">{label}</div>
    #</div>

    #<div class="kpi-value">{value}</div>
    #<div class="kpi-caption">{caption}</div>
#</div>
 #       """,
  #      unsafe_allow_html=True,
   # )

def module_card(
    icon: str,
    title: str,
    description: str,
    action: str,
) -> None:
    """Render one platform-module card with a Material icon."""

    card_html = (
        '<div class="module-card">'
        '<div class="module-icon">'
        f'<span class="material-symbols-rounded">{icon}</span>'
        '</div>'
        f'<div class="module-title">{title}</div>'
        f'<div class="module-description">{description}</div>'
        f'<div class="module-action">{action} →</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )

def get_model_accuracy(metadata: dict) -> float:
    """Read model accuracy safely from metadata."""

    metrics = metadata.get("metrics", {})

    accuracy = (
        metrics.get("Accuracy")
        or metrics.get("accuracy")
        or metadata.get("accuracy")
        or 0
    )

    try:
        accuracy = float(accuracy)
    except (TypeError, ValueError):
        return 0.0

    if accuracy > 1:
        accuracy = accuracy / 100

    return accuracy


# ============================================================
# HOME PAGE HERO
# ============================================================

def render_home_hero() -> None:
    """Render the text-only homepage hero."""

    st.markdown(
        """
<div class="hero-shell">
    <div class="hero-content">

<div class="hero-badge">✦ PREMIUM AI PLATFORM</div><h1 class="hero-title">AI-Powered Customer<br>Retention<span class="hero-gradient">Intelligence Platform</span></h1>
<div class="hero-description">Predict customer churn, identify at-risk customers, protect recurring revenue, and make faster decisions using machine learning and business intelligence.</div></div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-buttons"></div>',
        unsafe_allow_html=True,
    )

    button_col1, button_col2, spacer = st.columns(
        [1.25, 1.55, 3.3]
    )

    with button_col1:
        st.page_link(
            prediction_page,
            label="Start Prediction",
            icon=":material/rocket_launch:",
            use_container_width=True,
        )

    with button_col2:
        st.page_link(
            executive_page,
            label="Executive Dashboard",
            icon=":material/analytics:",
            use_container_width=True,
        )


# ============================================================
# HOME PAGE
# ============================================================

def render_home() -> None:
    """Render the main customer-retention homepage."""

    data = load_predictions().copy()

    model, feature_names, metadata = load_model_assets()

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

    model_accuracy = get_model_accuracy(metadata)

    model_name = metadata.get(
        "model_name",
        type(model).__name__,
    )

    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    render_home_hero()

    # --------------------------------------------------------
    # KPI cards
    # --------------------------------------------------------

    section_header(
        "Live Business Metrics",
        "Current customer portfolio and model performance",
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "groups",
            "Total Customers",
            f"{total_customers:,}",
            "Customer records analyzed",
        )

    with col2:
        metric_card(
            "gpp_bad",
            "High-Risk Customers",
            f"{high_risk_customers:,}",
            (
                f"{high_risk_customers / total_customers:.1%} "
                "of the customer base"
            ),
        )

    with col3:
        metric_card(
            "account_balance_wallet",
            "Revenue at Risk",
            f"${revenue_at_risk / 1_000_000:.2f}M",
            "Probability-weighted annual exposure",
        )

    with col4:
        metric_card(
            "analytics",
            "Model Accuracy",
            f"{model_accuracy:.1%}",
            model_name,
        )

    # --------------------------------------------------------
    # Platform modules
    # --------------------------------------------------------

    section_header(
        "Platform Modules",
        "AI and analytics tools for customer retention",
    )

    modules = [
    (
        "psychology","Customer Prediction",
        "Generate real-time churn probabilities for individual customer profiles.",
        "Predict Now",
    ),
    (
        "shield",
        "Risk Scoring",
        "Identify, rank, and prioritize customers according to churn risk.",
        "View Risk Scores",
    ),
    (
        "smart_toy",
        "AI Recommendations",
        "Generate personalized retention actions and recommendations.",
        "Get Recommendations",
    ),
    (
        "monitoring",
        "Revenue Intelligence",
        "Estimate revenue exposure and potential customer loss.",
        "Explore Revenue",
    ),
    (
        "dashboard",
        "Executive Dashboard",
        "Review executive KPIs and customer retention performance.",
        "View Dashboard",
    ),
    (
        "description",
        "Reports",
        "Preview and download customer intelligence reports.",
        "View Reports",
    ),
]

    module_columns = st.columns(6)

    for column, module in zip(
        module_columns,
        modules,
    ):
        with column:
            module_card(*module)

    # --------------------------------------------------------
    # Key business insights
    # --------------------------------------------------------

    section_header(
        "Key Business Insights",
        "Overview of churn, risk, and revenue exposure",
    )

    chart1, chart2, chart3 = st.columns(3)

    # Churn chart
    with chart1:

        if "ActualChurnLabel" in data.columns:
            churn_column = "ActualChurnLabel"

        elif "PredictedChurnLabel" in data.columns:
            churn_column = "PredictedChurnLabel"

        elif "PredictedChurnClass" in data.columns:
            churn_column = "PredictedChurnClass"

        else:
            churn_column = None

        if churn_column:

            churn_summary = (
                data[churn_column]
                .value_counts()
                .reset_index()
            )

            churn_summary.columns = [
                "Customer Status",
                "Customers",
            ]

            churn_figure = px.pie(
                churn_summary,
                names="Customer Status",
                values="Customers",
                hole=0.64,
                title="Churn Distribution",
                color_discrete_sequence=[
                    "#22c55e",
                    "#ef4444",
                ],
            )

            churn_figure.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=25,
                    r=25,
                    t=55,
                    b=25,
                ),
                legend=dict(
                    orientation="h",
                    y=-0.08,
                ),
            )

            st.plotly_chart(
                churn_figure,
                use_container_width=True,
            )

        else:
            st.info(
                "No churn-label column is available."
            )

    # Risk chart
    with chart2:

        risk_order = [
            "Low",
            "Moderate",
            "High",
            "Critical",
        ]

        risk_summary = (
            data["RiskCategory"]
            .value_counts()
            .reindex(
                risk_order,
                fill_value=0,
            )
            .reset_index()
        )

        risk_summary.columns = [
            "Risk Category",
            "Customers",
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
                "Critical": "#ef4444",
            },
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
                b=25,
            ),
        )

        st.plotly_chart(
            risk_figure,
            use_container_width=True,
        )

    # Revenue chart
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
                observed=False,
            )["ExpectedAnnualRevenueLoss"]
            .sum()
            .sort_values(ascending=True)
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
                "#ef4444",
            ],
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
                b=25,
            ),
        )

        st.plotly_chart(
            revenue_figure,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Priority customer table
    # --------------------------------------------------------

    section_header(
        "Priority Customer Activity",
        "Customers requiring the greatest retention attention",
    )

    preferred_columns = [
        "CustomerRiskRank",
        "ChurnProbabilityPercent",
        "RiskCategory",
        "RetentionPriority",
        "CustomerValueScore",
        "CustomerRiskScore",
        "BusinessSegment",
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
            ascending=False,
        )
        .head(8)
    )

    st.dataframe(
        priority_customers[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # Call to action
    # --------------------------------------------------------

    st.markdown(
        """
<div class="cta-box">
    <div class="cta-title">
        🚀 Ready to reduce churn and protect revenue?
    </div>
<div class="cta-text">Use AI-powered customer intelligence to identify risk early and take targeted action.</div></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="cta-link-space"></div>',
        unsafe_allow_html=True,
    )

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:
        st.page_link(
            prediction_page,
            label="Get Started Now",
            icon=":material/rocket_launch:",
            use_container_width=True,
        )


# ============================================================
# NAVIGATION PAGES
# ============================================================

home_page = st.Page(
    render_home,
    title="Home",
    icon=":material/home:",
    default=True,
    url_path="home",
)

dashboard_page = st.Page(
    dashboard.render,
    title="Dashboard",
    icon=":material/dashboard:",
    url_path="dashboard",
)

prediction_page = st.Page(
    prediction.render,
    title="Customer Prediction",
    icon=":material/person_search:",
    url_path="prediction",
)

risk_page = st.Page(
    risk_scoring.render,
    title="Risk Scoring",
    icon=":material/gpp_bad:",
    url_path="risk-scoring",
)

recommendations_page = st.Page(
    recommendations.render,
    title="AI Recommendations",
    icon=":material/psychology:",
    url_path="recommendations",
)

revenue_page = st.Page(
    revenue_intelligence.render,
    title="Revenue Intelligence",
    icon=":material/monitoring:",
    url_path="revenue-intelligence",
)

executive_page = st.Page(
    executive_dashboard.render,
    title="Executive Dashboard",
    icon=":material/analytics:",
    url_path="executive-dashboard",
)

reports_page = st.Page(
    reports.render,
    title="Reports",
    icon=":material/description:",
    url_path="reports",
)

about_page = st.Page(
    about.render,
    title="About",
    icon=":material/info:",
    url_path="about",
)


# ============================================================
# RUN APPLICATION
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
        about_page,
    ],
    position="sidebar",
)

navigation.run()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    © 2026 <strong>Retention Intelligence Platform</strong><br>
    Powered by Artificial Intelligence • Machine Learning • Business Intelligence
</div>
    """,
    unsafe_allow_html=True,
)