"""AI insights component using AsyncRunner."""

import streamlit as st

from src.core.async_runner import run_async


def render_ai_section(dataset, use_case) -> None:
    """Render AI analysis interface."""
    st.subheader("🧠 AI-Powered Analysis")

    from src.application.services.ai_service import AIService

    providers = AIService().get_available_providers()

    if not providers:
        st.warning("No AI providers configured. Set API keys in .env file.")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input(
            "Ask a question about your data (optional)",
            placeholder="e.g., What are the main patterns in this dataset?",
        )
    with col2:
        provider = st.selectbox("Provider", providers)

    if st.button("✨ Generate AI Analysis", type="primary"):
        with st.spinner(f"Consulting {provider.title()}..."):
            try:
                if question:
                    response = run_async(
                        use_case.execute_ai_analysis(dataset, question)
                    )
                else:
                    response = run_async(use_case.execute_ai_insights(dataset))

                st.markdown("### Analysis Results")
                st.markdown(response)
                st.session_state["ai_insights"] = response

            except (KeyError, OSError, RuntimeError, TypeError, ValueError) as e:
                st.error(f"AI analysis failed: {e!s}")
                st.info("Check your API key configuration in .env file")
