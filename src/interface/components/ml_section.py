"""Machine Learning training component."""

import streamlit as st

from src.application.use_cases.analyze_dataset import AnalyzeDatasetUseCase
from src.domain.enums.ml_enums import MLTaskType, MetricType


def render_ml_section(dataset, use_case: AnalyzeDatasetUseCase) -> None:
    """Render ML training interface."""
    numeric_cols = dataset.get_numeric_columns()
    categorical_cols = dataset.get_categorical_columns()
    
    if not numeric_cols:
        st.warning("Machine Learning requires numeric features")
        return
    
    st.subheader("🤖 AutoML Training")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target = st.selectbox("Target Column", dataset.data.columns.tolist())
    
    with col2:
        task = st.selectbox(
            "Task Type",
            [MLTaskType.CLASSIFICATION.value, MLTaskType.REGRESSION.value],
        )
    
    # Auto-detect task type suggestion
    if dataset.data[target].dtype == "object" or dataset.data[target].nunique() < 10:
        st.caption("💡 This looks like a classification problem")
    else:
        st.caption("💡 This looks like a regression problem")
    
    features = st.multiselect(
        "Feature Columns (leave empty for auto-select)",
        options=[c for c in numeric_cols if c != target],
        default=[c for c in numeric_cols if c != target][:10],
    )
    
    if st.button("🚀 Train Models", type="primary"):
        with st.spinner("Training multiple models... This may take a minute"):
            try:
                task_type = MLTaskType.CLASSIFICATION if task == "classification" else MLTaskType.REGRESSION
                
                results = use_case.execute_ml_training(
                    dataset=dataset,
                    target_column=target,
                    task_type=task_type,
                    feature_columns=features if features else None,
                )
                
                st.success(f"🏆 Best Model: **{results['best_model']}** (CV Score: {results['cv_score']:.4f})")
                
                # Results table
                import pandas as pd
                results_df = pd.DataFrame(results["all_results"])
                st.dataframe(results_df, use_container_width=True)
                
                # Feature importance
                if results.get("feature_importance"):
                    st.subheader("Feature Importance")
                    fi_df = pd.DataFrame([
                        {"Feature": k, "Importance": v}
                        for k, v in results["feature_importance"].items()
                    ])
                    st.bar_chart(fi_df.set_index("Feature"))
                
                # Store results
                st.session_state["ml_results"] = results
                
            except Exception as e:
                st.error(f"Training failed: {str(e)}")
