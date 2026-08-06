"""Export functionality component."""

import streamlit as st

from src.domain.enums.ml_enums import ExportFormat


def render_export_section(dataset, results, use_case) -> None:
    """Render export options."""
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dataset Export**")
        
        fmt = st.selectbox("Format", ["csv", "excel", "json", "html"])
        
        if st.button("📥 Export Dataset"):
            try:
                from src.application.services.export_service import ExportService
                service = ExportService()
                path = service.export_dataset(dataset, ExportFormat(fmt))
                st.success(f"Exported to: `{path}`")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    with col2:
        st.markdown("**PDF Report**")
        
        include_ai = st.checkbox("Include AI Insights", value=True)
        include_ml = st.checkbox("Include ML Results", value=True)
        
        if st.button("📄 Generate PDF Report"):
            with st.spinner("Generating report..."):
                try:
                    from src.application.services.export_service import ExportService
                    service = ExportService()
                    
                    ai_text = st.session_state.get("ai_insights") if include_ai else None
                    ml_res = st.session_state.get("ml_results") if include_ml else None
                    
                    path = service.generate_pdf_report(
                        dataset=dataset,
                        statistics=results.get("statistics"),
                        ml_results=ml_res,
                        ai_insights=ai_text,
                    )
                    st.success(f"Report saved: `{path}`")
                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
