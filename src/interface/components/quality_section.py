"""Data quality report component."""

import streamlit as st


def render_quality_section(dataset) -> None:
    """Render data quality assessment."""
    if not dataset.quality_report:
        st.info("No quality report available")
        return
    
    report = dataset.quality_report
    
    # Summary metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cells", f"{report.total_cells:,}")
    c2.metric("Missing Cells", f"{report.missing_percentage:.2f}%")
    c3.metric("Duplicate Rows", f"{report.duplicate_percentage:.2f}%")
    c4.metric("Memory Usage", f"{report.memory_usage_mb:.2f} MB")
    
    # Column profiles
    st.subheader("Column Profiles")
    
    profile_data = []
    for p in report.column_profiles:
        profile_data.append({
            "Column": p.name,
            "Type": p.dtype,
            "Nulls": f"{p.null_percentage:.1f}%",
            "Unique": p.unique_count,
            "Cardinality": f"{p.cardinality_ratio:.2f}",
            "High Card": "⚠️" if p.is_high_cardinality else "✅",
        })
    
    import pandas as pd
    df = pd.DataFrame(profile_data)
    st.dataframe(df, use_container_width=True, height=400)
    
    # Warnings
    if report.warnings:
        st.subheader("⚠️ Warnings")
        for warning in report.warnings:
            st.warning(warning)
    
    if report.recommendations:
        st.subheader("💡 Recommendations")
        for rec in report.recommendations:
            st.info(rec)
