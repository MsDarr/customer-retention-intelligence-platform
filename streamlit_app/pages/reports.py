
import streamlit as st

from utils.data_loader import (
    load_predictions,
    load_risk_ranking,
    load_recommendations,
    load_executive_kpis,
    load_business_segments
)


def create_download(data, filename):

    csv = data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label=f"Download {filename}",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv",
        use_container_width=True
    )


def render():

    st.title("Reports & Downloads")

    st.caption(
        "Export customer intelligence reports for "
        "business analysis and executive reporting."
    )

    reports = {

        "Customer Predictions":
            load_predictions(),

        "Risk Ranking":
            load_risk_ranking(),

        "Retention Recommendations":
            load_recommendations(),

        "Executive KPIs":
            load_executive_kpis(),

        "Business Segments":
            load_business_segments()

    }

    for report_name, dataframe in reports.items():

        st.markdown("---")

        st.subheader(report_name)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Rows",
                f"{len(dataframe):,}"
            )

        with col2:
            st.metric(
                "Columns",
                dataframe.shape[1]
            )

        with col3:
            memory = (
                dataframe.memory_usage(
                    deep=True
                ).sum() / 1024
            )

            st.metric(
                "Size (KB)",
                f"{memory:.2f}"
            )

        st.dataframe(
            dataframe.head(10),
            use_container_width=True
        )

        create_download(
            dataframe,
            report_name.lower().replace(
                " ",
                "_"
            )
        )
