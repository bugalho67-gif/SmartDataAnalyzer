"""Dashboard overview component."""

import streamlit as st

from src.domain.entities.dataset import Dataset


def render_dashboard(dataset: Dataset, results: dict) -> None:
    """Render main dashboard with KPI cards."""
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", f"{dataset.row_count:,}")
    with col2:
        st.metric("Columns", dataset.column_count)
    with col3:
        st.metric("Memory", f"{dataset.memory_usage_mb:.2f} MB")
    with col4:
        if dataset.quality_report:
            missing = dataset.quality_report.missing_percentage
            st.metric("Missing Data", f"{missing:.1f}%", delta=None)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Quick preview
    with st.expander("👁️ Data Preview (first 10 rows)", expanded=False):
        st.dataframe(
            dataset.data.head(10),
            use_container_width=True,
            height=300,
        )
