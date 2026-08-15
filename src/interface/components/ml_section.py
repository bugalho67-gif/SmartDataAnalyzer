"""Machine Learning training component with Optuna support."""

import streamlit as st

from src.application.services.optuna_service import OptunaService
from src.domain.enums.ml_enums import MLTaskType


def render_ml_section(dataset, use_case) -> None:
    """Render ML training interface with AutoML and Optuna."""
    numeric_cols = dataset.get_numeric_columns()
    all_cols = dataset.data.columns.tolist()

    if not numeric_cols:
        st.warning("Machine Learning requires numeric features")
        return

    st.subheader("🤖 AutoML Training")

    col1, col2 = st.columns(2)
    with col1:
        target = st.selectbox("Target Column", all_cols)
    with col2:
        task = st.selectbox(
            "Task Type",
            [MLTaskType.CLASSIFICATION.value, MLTaskType.REGRESSION.value],
        )

    # Auto-detect suggestion
    if dataset.data[target].dtype == "object" or dataset.data[target].nunique() < 10:
        st.caption("💡 This looks like a classification problem")
    else:
        st.caption("💡 This looks like a regression problem")

    features = st.multiselect(
        "Feature Columns (leave empty for auto-select)",
        options=[c for c in numeric_cols if c != target],
        default=[c for c in numeric_cols if c != target][:10],
    )

    use_optuna = st.toggle("🔮 Use Optuna Hyperparameter Optimization", value=False)

    if st.button("🚀 Train Models", type="primary"):
        with st.spinner(
            "Training..." if not use_optuna else "Optimizing with Optuna..."
        ):
            try:
                task_type = (
                    MLTaskType.CLASSIFICATION
                    if task == "classification"
                    else MLTaskType.REGRESSION
                )

                if use_optuna:
                    optuna_service = OptunaService(n_trials=15)
                    results = optuna_service.optimize(
                        dataset=dataset,
                        target_column=target,
                        task_type=task_type,
                        model_family="xgboost",
                        feature_columns=features if features else None,
                    )
                    st.success(
                        f"🏆 Best params found! Score: {results['test_score']:.4f}"
                    )
                    st.json(results["best_params"])
                    with st.expander("Optimization History"):
                        st.dataframe(results["optimization_history"])
                else:
                    results = use_case.execute_ml_training(
                        dataset=dataset,
                        target_column=target,
                        task_type=task_type,
                        feature_columns=features if features else None,
                    )
                    st.success(
                        f"🏆 Best: **{results['best_model']}** (CV: {results['cv_score']:.4f})"
                    )

                # Feature importance
                if results.get("feature_importance"):
                    st.subheader("Feature Importance")
                    import pandas as pd

                    fi_df = pd.DataFrame(
                        [
                            {"Feature": k, "Importance": v}
                            for k, v in results["feature_importance"].items()
                        ]
                    )
                    st.bar_chart(fi_df.set_index("Feature"))

                st.session_state["ml_results"] = results

            except (KeyError, OSError, RuntimeError, TypeError, ValueError) as e:
                st.error(f"Training failed: {e!s}")
