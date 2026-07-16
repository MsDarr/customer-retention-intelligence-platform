import streamlit as st

from utils.data_loader import load_model_assets


# ============================================================
# ABOUT PAGE STYLES
# ============================================================

def apply_about_styles() -> None:
    """Apply styling used only on the About page."""

    st.markdown(
        """
<style>

.about-hero {
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;

    border: 1px solid rgba(99, 102, 241, 0.30);
    border-radius: 22px;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(124, 58, 237, 0.22),
            transparent 34%
        ),
        linear-gradient(
            135deg,
            rgba(15, 23, 42, 0.98),
            rgba(30, 41, 59, 0.96)
        );

    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.24);
}

.about-badge {
    display: inline-flex;
    align-items: center;

    padding: 0.45rem 0.80rem;
    margin-bottom: 1rem;

    border: 1px solid rgba(129, 140, 248, 0.38);
    border-radius: 999px;

    color: #a5b4fc;

    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
}

.about-title {
    margin: 0;

    color: #f8fafc;

    font-size: clamp(2.2rem, 4vw, 3.7rem);
    font-weight: 900;

    line-height: 1.06;
    letter-spacing: -0.045em;
}

.about-gradient {
    background:
        linear-gradient(
            90deg,
            #3b82f6,
            #8b5cf6,
            #d946ef
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.about-subtitle {
    max-width: 800px;

    margin-top: 1rem;

    color: #cbd5e1;

    font-size: 1rem;
    line-height: 1.7;
}

.about-section {
    margin-top: 1.8rem;
    margin-bottom: 1rem;
}

.about-section-title {
    color: #f8fafc;

    font-size: 1.45rem;
    font-weight: 850;
}

.about-section-caption {
    margin-top: 0.2rem;

    color: #94a3b8;

    font-size: 0.86rem;
}

.about-panel {
    padding: 1.4rem 1.5rem;

    border: 1px solid rgba(71, 85, 105, 0.55);
    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(20, 31, 53, 0.96),
            rgba(9, 18, 34, 0.98)
        );
}

.about-panel p {
    color: #cbd5e1;

    line-height: 1.75;
}

.about-stat {
    min-height: 135px;
    padding: 1.2rem;

    border: 1px solid rgba(71, 85, 105, 0.58);
    border-radius: 17px;

    background:
        linear-gradient(
            145deg,
            rgba(25, 37, 63, 0.98),
            rgba(10, 19, 36, 0.98)
        );
}

.about-stat-label {
    color: #94a3b8;

    font-size: 0.78rem;
    font-weight: 700;
}

.about-stat-value {
    margin-top: 0.7rem;

    color: #f8fafc;

    font-size: 1.6rem;
    font-weight: 900;

    line-height: 1.15;
}

.about-stat-caption {
    margin-top: 0.4rem;

    color: #818cf8;

    font-size: 0.76rem;
}

.capability-card {
    min-height: 205px;
    height: 100%;

    padding: 1.2rem;

    border: 1px solid rgba(71, 85, 105, 0.55);
    border-radius: 17px;

    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(99, 102, 241, 0.12),
            transparent 35%
        ),
        linear-gradient(
            155deg,
            rgba(24, 37, 62, 0.98),
            rgba(9, 18, 34, 0.98)
        );
}

.capability-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 48px;
    height: 48px;

    margin-bottom: 0.9rem;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    font-size: 1.35rem;
}

.capability-title {
    color: #f8fafc;

    font-size: 0.98rem;
    font-weight: 800;
}

.capability-text {
    margin-top: 0.55rem;

    color: #aab8cc;

    font-size: 0.80rem;
    line-height: 1.6;
}

.workflow-step {
    padding: 0.9rem 1rem;
    margin-bottom: 0.65rem;

    border-left: 3px solid #7c3aed;
    border-radius: 10px;

    background: rgba(15, 23, 42, 0.68);

    color: #cbd5e1;
}

.tech-badge {
    display: inline-block;

    padding: 0.55rem 0.85rem;
    margin: 0.28rem;

    border: 1px solid rgba(99, 102, 241, 0.34);
    border-radius: 999px;

    background: rgba(49, 46, 129, 0.18);

    color: #c7d2fe;

    font-size: 0.78rem;
    font-weight: 700;
}

.responsible-box {
    padding: 1.3rem 1.4rem;

    border: 1px solid rgba(234, 179, 8, 0.28);
    border-radius: 17px;

    background:
        linear-gradient(
            145deg,
            rgba(66, 50, 15, 0.25),
            rgba(15, 23, 42, 0.85)
        );

    color: #d8dee9;

    line-height: 1.7;
}

</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SMALL COMPONENTS
# ============================================================

def section_header(
    title: str,
    caption: str,
) -> None:
    """Render an About-page section heading."""

    html = (
        '<div class="about-section">'
        f'<div class="about-section-title">{title}</div>'
        f'<div class="about-section-caption">{caption}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def stat_card(
    label: str,
    value: str,
    caption: str,
) -> None:
    """Render one model or platform statistic."""

    html = (
        '<div class="about-stat">'
        f'<div class="about-stat-label">{label}</div>'
        f'<div class="about-stat-value">{value}</div>'
        f'<div class="about-stat-caption">{caption}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def capability_card(
    icon: str,
    title: str,
    description: str,
) -> None:
    """Render one platform capability card."""

    html = (
        '<div class="capability-card">'
        f'<div class="capability-icon">{icon}</div>'
        f'<div class="capability-title">{title}</div>'
        f'<div class="capability-text">{description}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# ABOUT PAGE
# ============================================================

def render() -> None:
    """Render the platform About page."""

    apply_about_styles()

    model, feature_names, metadata = load_model_assets()

    model_name = metadata.get(
        "model_name",
        type(model).__name__,
    )

    classification_threshold = metadata.get(
        "classification_threshold",
        0.50,
    )

    metrics = metadata.get("metrics", {})

    model_accuracy = (
        metrics.get("Accuracy")
        or metrics.get("accuracy")
        or metadata.get("accuracy")
        or 0
    )

    try:
        model_accuracy = float(model_accuracy)
    except (TypeError, ValueError):
        model_accuracy = 0.0

    if model_accuracy > 1:
        model_accuracy /= 100

    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    hero_html = (
        '<div class="about-hero">'
        '<div class="about-badge">PLATFORM OVERVIEW</div>'
        '<h1 class="about-title">'
        'About the '
        '<span class="about-gradient">Retention Intelligence Platform</span>'
        '</h1>'
        '<div class="about-subtitle">'
        'An end-to-end machine learning and business intelligence '
        'solution for churn prediction, customer risk prioritization, '
        'retention recommendations, revenue protection, and executive reporting.'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Project overview
    # --------------------------------------------------------

    section_header(
        "Project Overview",
        "What the platform does and why it was developed",
    )

    overview_html = (
        '<div class="about-panel">'
        '<p>'
        'The AI-Powered Customer Retention Intelligence Platform '
        'transforms customer data into operational retention intelligence. '
        'It identifies customers who are likely to churn, prioritizes '
        'high-risk accounts, estimates potential revenue exposure, and '
        'supports targeted retention decisions through machine learning '
        'and business analytics.'
        '</p>'
        '<p>'
        'The platform was designed as a complete analytics workflow rather '
        'than a standalone prediction model. It connects data preparation, '
        'feature engineering, model deployment, risk scoring, personalized '
        'recommendations, executive dashboards, and downloadable reporting.'
        '</p>'
        '</div>'
    )

    st.markdown(
        overview_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Platform statistics
    # --------------------------------------------------------

    section_header(
        "Platform Statistics",
        "Production model and deployment details",
    )

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        stat_card(
            "Production Model",
            model_name,
            "Selected classification model",
        )

    with stat2:
        stat_card(
            "Model Accuracy",
            f"{model_accuracy:.1%}",
            "Current production performance",
        )

    with stat3:
        stat_card(
            "Predictor Features",
            str(len(feature_names)),
            "Features used during prediction",
        )

    with stat4:
        stat_card(
            "Decision Threshold",
            str(classification_threshold),
            "Churn classification threshold",
        )

    # --------------------------------------------------------
    # Capabilities
    # --------------------------------------------------------

    section_header(
        "Platform Capabilities",
        "Integrated AI, analytics, and decision-support modules",
    )

    capabilities = [
        (
            "🔮",
            "Customer Prediction",
            "Generates real-time churn probabilities for individual customer profiles.",
        ),
        (
            "🛡️",
            "Risk Intelligence",
            "Classifies and ranks customers according to their likelihood of churn.",
        ),
        (
            "🤖",
            "AI Recommendations",
            "Produces personalized retention actions and engagement strategies.",
        ),
        (
            "💹",
            "Revenue Intelligence",
            "Estimates revenue exposure, expected loss, and recovery opportunities.",
        ),
        (
            "📊",
            "Executive Analytics",
            "Provides decision-ready KPIs and customer-retention performance views.",
        ),
        (
            "📄",
            "Business Reporting",
            "Supports downloadable operational and executive intelligence reports.",
        ),
    ]

    capability_columns = st.columns(3)

    for index, capability in enumerate(capabilities):
        with capability_columns[index % 3]:
            capability_card(*capability)

    # --------------------------------------------------------
    # Analytical workflow
    # --------------------------------------------------------

    section_header(
        "Analytical Workflow",
        "How customer data moves through the platform",
    )

    workflow_steps = [
        "1. Data collection, validation, and preprocessing",
        "2. Exploratory analysis and customer-behavior profiling",
        "3. Feature engineering and business-variable creation",
        "4. Machine-learning development and model selection",
        "5. Customer churn prediction and probability scoring",
        "6. Risk ranking, segmentation, and retention prioritization",
        "7. AI recommendations and revenue-impact estimation",
        "8. Executive dashboards, reporting, and deployment",
    ]

    for step in workflow_steps:
        st.markdown(
            f'<div class="workflow-step">{step}</div>',
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Technology stack
    # --------------------------------------------------------

    section_header(
        "Technology Stack",
        "Core tools used to develop and deploy the platform",
    )

    technologies = [
        "Python",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "XGBoost",
        "Plotly",
        "Streamlit",
        "Joblib",
        "Google Colab",
        "Git",
        "GitHub",
        "VS Code",
    ]

    technology_html = "".join(
        f'<span class="tech-badge">{technology}</span>'
        for technology in technologies
    )

    st.markdown(
        technology_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Business value
    # --------------------------------------------------------

    section_header(
        "Business Value",
        "How the platform supports customer-retention decisions",
    )

    business_value_html = (
        '<div class="about-panel">'
        '<p>✓ Predicts potential churn before customer cancellation</p>'
        '<p>✓ Prioritizes customers requiring immediate retention attention</p>'
        '<p>✓ Estimates probability-weighted revenue exposure</p>'
        '<p>✓ Supports personalized offers and communication strategies</p>'
        '<p>✓ Provides executive visibility into customer-retention performance</p>'
        '<p>✓ Converts machine-learning predictions into business actions</p>'
        '</div>'
    )

    st.markdown(
        business_value_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Responsible use
    # --------------------------------------------------------

    section_header(
        "Responsible Use",
        "Guidance for applying model outputs in business operations",
    )

    responsible_html = (
        '<div class="responsible-box">'
        '<strong>Human review remains essential.</strong><br>'
        'Predictions should support—not replace—professional judgment. '
        'Retention actions should be reviewed for fairness, relevance, '
        'financial impact, privacy, and customer experience before implementation. '
        'Model performance should also be monitored regularly as customer behavior '
        'and business conditions change.'
        '</div>'
    )

    st.markdown(
        responsible_html,
        unsafe_allow_html=True,
    )