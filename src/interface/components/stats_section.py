"""Statistics display component."""

from typing import Any, Dict

import pandas as pd
import streamlit as st


def render_stats_section(statistics: Dict[str, Any]) -> None:
    """Render descriptive statistics."""
    if not statistics:
        st.info("No statistics available")
        return

    # Remove internal keys
    display_stats = {k: v for k, v in statistics.items() if not k.startswith("_")}

    if not display_stats:
        st.info("No numeric columns found for statistical analysis")
        return

    # Create DataFrame for display
    stats_rows = []
    for col_name, col_stats in display_stats.items():
        row = {"Column": col_name}
        row.update(col_stats)
        stats_rows.append(row)

    df = pd.DataFrame(stats_rows)

    # Column selector
    selected_cols = st.multiselect(
        "Select columns to display",
        options=df["Column"].tolist(),
        default=df["Column"].tolist()[:5],
    )

    if selected_cols:
        filtered = df[df["Column"].isin(selected_cols)]
        st.dataframe(
            filtered.style.background_gradient(subset=["mean", "std"], cmap="Blues"),
            use_container_width=True,
            height=400,
        )

    # Download stats
    csv = df.to_csv(index=False)
    st.download_button(
        "📥 Download Statistics (CSV)",
        data=csv,
        file_name="statistics.csv",
        mime="text/csv",
    )
