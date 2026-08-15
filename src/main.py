"""SmartDataAnalyzer - Entry Point."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from src.config.settings import get_settings
from src.core.logging_config import configure_logging
from src.interface.app import run_app


def main() -> None:
    """Initialize and run the Streamlit application."""
    settings = get_settings()
    configure_logging(settings)

    st.set_page_config(
        page_title=f"{settings.app_name} v{settings.app_version}",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/smartdataanalyzer/help",
            "Report a bug": "https://github.com/smartdataanalyzer/issues",
            "About": f"**{settings.app_name}** - Intelligent Data Analysis Platform",
        },
    )

    run_app()


if __name__ == "__main__":
    main()
