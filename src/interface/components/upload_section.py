"""File upload component."""

import streamlit as st

from src.application.use_cases.analyze_dataset import AnalyzeDatasetUseCase
from src.config.settings import get_settings
from src.core.exceptions import FileUploadError


def render_upload_section():
    """Render file upload area and process files."""
    settings = get_settings()

    uploaded_file = st.file_uploader(
        "Upload your dataset",
        type=settings.allowed_extensions_list,
        help=f"Maximum file size: {settings.security.max_upload_size_mb}MB",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        try:
            use_case = st.session_state.get("use_case", AnalyzeDatasetUseCase())
            dataset = use_case.execute_upload(uploaded_file)

            st.success(
                f"✅ Loaded **{dataset.name}** — {dataset.row_count:,} rows × {dataset.column_count} columns"
            )
            return dataset

        except FileUploadError as e:
            st.error(f"❌ {e.message}")
            if e.details:
                st.json(e.details)
        except (OSError, RuntimeError, TypeError, ValueError) as e:
            st.error(f"❌ Unexpected error: {e!s}")

    return None
