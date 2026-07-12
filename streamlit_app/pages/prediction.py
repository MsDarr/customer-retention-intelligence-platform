
import streamlit as st

from utils.prediction_engine import (
    predict_customer
)

from utils.risk_engine import (
    assign_risk_category,
    assign_retention_priority,
    get_risk_message
)


def render_probability_bar(probability):

    st.progress(
        min(
            max(float(probability), 0.0),
            1.0
        )
    )


def render():

    st.title("Customer Churn Prediction")

    st.caption(
        "Enter customer information to generate "
        "a real-time churn probability and risk assessment."
    )

    with st.form(
        "customer_prediction_form"
    ):

        st.subheader("Customer Demographics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            gender = st.selectbox(
                "Gender",
                ["Female", "Male"]
            )

        with col2:

            senior_label = st.selectbox(
                "Senior Citizen",
                ["No", "Yes"]
            )

        with col3:

            partner = st.selectbox(
                "Partner",
                ["No", "Yes"]
            )

        with col4:

            dependents = st.selectbox(
                "Dependents",
                ["No", "Yes"]
            )

        st.subheader("Customer Relationship")

        col1, col2, col3 = st.columns(3)

        with col1:

            tenure = st.number_input(
                "Tenure in Months",
                min_value=0,
                max_value=72,
                value=12,
                step=1
            )

        with col2:

            contract = st.selectbox(
                "Contract",
                [
                    "Month-to-month",
                    "One year",
                    "Two year"
                ]
            )

        with col3:

            paperless_billing = st.selectbox(
                "Paperless Billing",
                ["No", "Yes"]
            )

        st.subheader("Phone and Internet Services")

        col1, col2, col3 = st.columns(3)

        with col1:

            phone_service = st.selectbox(
                "Phone Service",
                ["No", "Yes"]
            )

        with col2:

            if phone_service == "No":

                multiple_lines = (
                    "No phone service"
                )

                st.selectbox(
                    "Multiple Lines",
                    ["No phone service"],
                    disabled=True
                )

            else:

                multiple_lines = st.selectbox(
                    "Multiple Lines",
                    ["No", "Yes"]
                )

        with col3:

            internet_service = st.selectbox(
                "Internet Service",
                [
                    "DSL",
                    "Fiber optic",
                    "No"
                ]
            )

        internet_disabled = (
            internet_service == "No"
        )

        no_internet_value = (
            "No internet service"
        )

        st.subheader("Internet Add-On Services")

        col1, col2, col3, col4 = st.columns(4)

        def internet_option(label):

            if internet_disabled:

                st.selectbox(
                    label,
                    [no_internet_value],
                    disabled=True,
                    key=f"{label}_disabled"
                )

                return no_internet_value

            return st.selectbox(
                label,
                ["No", "Yes"],
                key=label
            )

        with col1:

            online_security = internet_option(
                "Online Security"
            )

            online_backup = internet_option(
                "Online Backup"
            )

        with col2:

            device_protection = internet_option(
                "Device Protection"
            )

            tech_support = internet_option(
                "Tech Support"
            )

        with col3:

            streaming_tv = internet_option(
                "Streaming TV"
            )

            streaming_movies = internet_option(
                "Streaming Movies"
            )

        with col4:

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )

        st.subheader("Customer Charges")

        col1, col2 = st.columns(2)

        with col1:

            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                max_value=200.0,
                value=70.0,
                step=0.50,
                format="%.2f"
            )

        with col2:

            default_total = (
                monthly_charges * tenure
            )

            total_charges = st.number_input(
                "Total Charges",
                min_value=0.0,
                value=float(default_total),
                step=1.0,
                format="%.2f"
            )

        submitted = st.form_submit_button(
            "Generate Churn Prediction",
            type="primary",
            use_container_width=True
        )

    if submitted:

        customer = {
            "gender": gender,
            "SeniorCitizen": int(
                senior_label == "Yes"
            ),
            "Partner": partner,
            "Dependents": dependents,
            "tenure": int(tenure),
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": (
                paperless_billing
            ),
            "PaymentMethod": payment_method,
            "MonthlyCharges": float(
                monthly_charges
            ),
            "TotalCharges": float(
                total_charges
            )
        }

        try:

            result = predict_customer(
                customer
            )

            probability = result[
                "churn_probability"
            ]

            risk_category = (
                assign_risk_category(
                    probability
                )
            )

            retention_priority = (
                assign_retention_priority(
                    probability
                )
            )

            engineered = result[
                "engineered_customer"
            ].iloc[0]

            st.markdown("---")

            st.subheader("Prediction Result")

            metric1, metric2, metric3 = (
                st.columns(3)
            )

            with metric1:

                st.metric(
                    "Predicted Status",
                    result["predicted_label"]
                )

            with metric2:

                st.metric(
                    "Churn Probability",
                    (
                        f"{result[
                            'churn_probability_percent'
                        ]:.2f}%"
                    )
                )

            with metric3:

                st.metric(
                    "Risk Category",
                    risk_category
                )

            render_probability_bar(
                probability
            )

            if risk_category == "Critical":

                st.error(
                    get_risk_message(
                        risk_category
                    )
                )

            elif risk_category == "High":

                st.warning(
                    get_risk_message(
                        risk_category
                    )
                )

            elif risk_category == "Moderate":

                st.info(
                    get_risk_message(
                        risk_category
                    )
                )

            else:

                st.success(
                    get_risk_message(
                        risk_category
                    )
                )

            st.subheader("Customer Intelligence")

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            with col1:

                st.metric(
                    "Customer Value Score",
                    f"{engineered[
                        'CustomerValueScore'
                    ]:.2f}"
                )

            with col2:

                st.metric(
                    "Business Risk Score",
                    f"{engineered[
                        'CustomerRiskScore'
                    ]:.2f}"
                )

            with col3:

                st.metric(
                    "Service Count",
                    int(
                        engineered[
                            "ServiceCount"
                        ]
                    )
                )

            with col4:

                st.metric(
                    "Retention Priority",
                    retention_priority
                )

            with st.expander(
                "View Engineered Customer Features"
            ):

                display_columns = [
                    "CustomerLifetimeValue",
                    "EstimatedAnnualRevenue",
                    "LoyaltyScore",
                    "TenureCategory",
                    "ServiceCount",
                    "SupportUsageScore",
                    "RetentionScore",
                    "HighValueCustomer",
                    "PremiumCustomer",
                    "CustomerValueScore",
                    "CustomerRiskScore"
                ]

                st.dataframe(
                    result[
                        "engineered_customer"
                    ][display_columns].T,
                    use_container_width=True
                )

        except Exception as error:

            st.error(
                "Prediction could not be generated."
            )

            st.exception(error)
