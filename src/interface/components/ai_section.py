"""AI insights component."""

import asyncio

import streamlit as st


def render_ai_section(dataset, use_case) -> None:
    """Render AI analysis interface."""
    st.subheader("🧠 AI-Powered Analysis")
    
    # Provider info
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
                # Run async in sync context
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if question:
                    response = loop.run_until_complete(
                        use_case.execute_ai_analysis(dataset, question)
                    )
                else:
                    response = loop.run_until_complete(
                        use_case.execute_ai_insights(dataset)
                    )
                
                loop.close()
                
                st.markdown("### Analysis Results")
                st.markdown(response)
                
                # Store for export
                st.session_state["ai_insights"] = response
                
            except Exception as e:
                st.error(f"AI analysis failed: {str(e)}")
                st.info("Check your API key configuration in .env file")
