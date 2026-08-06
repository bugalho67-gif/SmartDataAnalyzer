"""Sidebar component."""

import streamlit as st

from src.config.settings import get_settings


def render_sidebar() -> None:
    """Render application sidebar."""
    settings = get_settings()
    
    with st.sidebar:
        st.markdown(
            f"""
            <div style="margin-bottom: 2rem;">
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem;">
                    {settings.app_name}
                </h2>
                <p style="font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.1em;">
                    v{settings.app_version} • {settings.app_env}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("---")
        
        # Navigation / Settings
        st.subheader("⚙️ Settings")
        
        # AI Provider selection
        from src.application.services.ai_service import AIService
        available = AIService().get_available_providers()
        
        if available:
            selected = st.selectbox(
                "AI Provider",
                options=available,
                index=0,
            )
            st.session_state["ai_provider"] = selected
        
        # Theme toggle placeholder
        st.toggle("Dark Mode (Beta)", value=False, disabled=True)
        
        st.markdown("---")
        
        # Info
        st.markdown(
            """
            <div style="font-size: 0.75rem; color: #9ca3af; line-height: 1.5;">
                <p><strong>SmartDataAnalyzer</strong></p>
                <p>Privacy-first data analysis with AI assistance.</p>
                <p style="margin-top: 1rem;">
                    🔒 Data stays local<br>
                    🤖 Multiple AI providers<br>
                    📊 AutoML included
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
