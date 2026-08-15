"""Main Streamlit application orchestrator."""

import streamlit as st

from src.application.use_cases.analyze_dataset import AnalyzeDatasetUseCase
from src.core.logging_config import logger
from src.core.security import get_rate_limiter
from src.interface.components.ai_section import render_ai_section
from src.interface.components.dashboard import render_dashboard
from src.interface.components.export_section import render_export_section
from src.interface.components.ml_section import render_ml_section
from src.interface.components.quality_section import render_quality_section
from src.interface.components.sidebar import render_sidebar
from src.interface.components.stats_section import render_stats_section
from src.interface.components.upload_section import render_upload_section
from src.interface.components.viz_section import render_viz_section
from src.interface.styles.custom_css import inject_custom_css


def initialize_session() -> None:
    """Initialize Streamlit session state variables."""
    if "dataset" not in st.session_state:
        st.session_state.dataset = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "session_id" not in st.session_state:
        import secrets

        st.session_state.session_id = secrets.token_hex(16)
    if "use_case" not in st.session_state:
        st.session_state.use_case = AnalyzeDatasetUseCase()


def run_app() -> None:
    """Main application entry point."""
    inject_custom_css()
    initialize_session()

    rate_limiter = get_rate_limiter()

    # Rate limiting check
    try:
        rate_limiter.check_or_raise(st.session_state.session_id)
    except Exception:
        st.error("⏱️ Too many requests. Please wait a moment.")
        st.stop()

    # Sidebar
    render_sidebar()

    # Main content
    st.title("📊 SmartDataAnalyzer")
    st.markdown(
        "<p style='color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;'>"
        "Intelligent data analysis powered by AI & Machine Learning</p>",
        unsafe_allow_html=True,
    )

    # Upload Section
    dataset = render_upload_section()
    if dataset:
        st.session_state.dataset = dataset

        # Auto-run analysis on new upload
        if (
            st.session_state.analysis_results is None
            or st.session_state.analysis_results.get("dataset") != dataset
        ):
            with st.spinner("🔍 Analyzing your dataset..."):
                try:
                    results = st.session_state.use_case.execute_full_analysis(dataset)
                    st.session_state.analysis_results = results
                    logger.info(f"Analysis completed for dataset: {dataset.id}")
                except Exception as e:
                    logger.error(f"Analysis failed: {e}")
                    st.error(f"Analysis failed: {str(e)}")

    # Dashboard & Analysis
    if st.session_state.dataset and st.session_state.analysis_results:
        dataset = st.session_state.dataset
        results = st.session_state.analysis_results

        # Dashboard Overview
        render_dashboard(dataset, results)

        # Tabs for detailed analysis
        tabs = st.tabs(
            [
                "📈 Statistics",
                "📉 Visualizations",
                "🔍 Data Quality",
                "🤖 Machine Learning",
                "🧠 AI Insights",
                "💾 Export",
            ]
        )

        with tabs[0]:
            render_stats_section(results.get("statistics"))

        with tabs[1]:
            render_viz_section(dataset, results)

        with tabs[2]:
            render_quality_section(dataset)

        with tabs[3]:
            render_ml_section(dataset, st.session_state.use_case)

        with tabs[4]:
            render_ai_section(dataset, st.session_state.use_case)

        with tabs[5]:
            render_export_section(dataset, results, st.session_state.use_case)

    elif not st.session_state.dataset:
        # Empty state
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem; color: #9ca3af;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📂</div>
                <h3 style="color: #6b7280; font-weight: 600;">Upload a dataset to begin</h3>
                <p>Supported formats: CSV, Excel (.xlsx, .xls), JSON</p>
                <p style="font-size: 0.875rem; margin-top: 1rem;">
                    Your data is processed locally and never stored without permission.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
