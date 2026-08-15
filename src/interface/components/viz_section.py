"""Visualization gallery component."""

import streamlit as st

from src.application.services.visualization_service import VisualizationService
from src.domain.entities.dataset import Dataset


def render_viz_section(dataset: Dataset, results: dict) -> None:
    """Render interactive visualizations."""
    viz_service = VisualizationService()
    numeric_cols = dataset.get_numeric_columns()
    categorical_cols = dataset.get_categorical_columns()

    if not numeric_cols and not categorical_cols:
        st.warning("No suitable columns for visualization")
        return

    viz_type = st.selectbox(
        "Chart Type",
        [
            "Histogram",
            "Bar Chart",
            "Pie Chart",
            "Box Plot",
            "Scatter Plot",
            "Correlation Heatmap",
        ],
    )

    try:
        if viz_type == "Histogram" and numeric_cols:
            col = st.selectbox("Column", numeric_cols, key="hist_col")
            fig = viz_service.create_histogram(dataset, col)
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Bar Chart" and categorical_cols:
            x_col = st.selectbox("X Axis", categorical_cols, key="bar_x")
            y_col = st.selectbox(
                "Y Axis (optional)", ["Count"] + numeric_cols, key="bar_y"
            )
            y_col = None if y_col == "Count" else y_col
            fig = viz_service.create_bar_chart(dataset, x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Pie Chart" and categorical_cols:
            col = st.selectbox("Column", categorical_cols, key="pie_col")
            fig = viz_service.create_pie_chart(dataset, col)
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Box Plot" and numeric_cols:
            col = st.selectbox("Column", numeric_cols, key="box_col")
            group = st.selectbox(
                "Group by (optional)", ["None"] + categorical_cols, key="box_group"
            )
            group = None if group == "None" else group
            fig = viz_service.create_box_plot(dataset, col, group)
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
            x_col = st.selectbox("X Axis", numeric_cols, key="scatter_x")
            y_col = st.selectbox(
                "Y Axis", [c for c in numeric_cols if c != x_col], key="scatter_y"
            )
            color = st.selectbox(
                "Color (optional)", ["None"] + categorical_cols, key="scatter_color"
            )
            color = None if color == "None" else color
            fig = viz_service.create_scatter_plot(dataset, x_col, y_col, color)
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Correlation Heatmap" and len(numeric_cols) >= 2:
            method = st.selectbox("Method", ["pearson", "spearman", "kendall"])
            fig = viz_service.create_heatmap(dataset, method)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
