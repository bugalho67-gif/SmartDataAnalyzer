"""SHAP explainability dashboard component."""

import pandas as pd
import streamlit as st

from src.application.services.shap_service import SHAPService
from src.core.exceptions import MLTrainingError


def render_shap_section(dataset) -> None:
    """Render SHAP explanation interface."""
    st.subheader("🔮 Model Explainability (SHAP)")

    ml_results = st.session_state.get("ml_results")
    if not ml_results:
        st.info(
            "Train a model in the Machine Learning tab first to enable SHAP explanations."
        )
        return

    model_id = ml_results.get("model_id")
    if not model_id:
        st.warning("No model ID found in training results.")
        return

    shap_service = SHAPService()

    action = st.radio(
        "Action", ["Global Explanation", "Single Prediction"], horizontal=True
    )

    if action == "Global Explanation":
        sample_size = st.slider("Sample size for SHAP", 10, 500, 100)
        if st.button("🔍 Explain Model", type="primary"):
            with st.spinner("Computing SHAP values..."):
                try:
                    results = shap_service.explain_model(model_id, dataset, sample_size)
                    st.session_state["shap_results"] = results

                    st.success(f"Explained using {results['sample_size']} samples")

                    # Feature importance chart
                    fi_df = pd.DataFrame(
                        [
                            {"Feature": k, "Mean |SHAP|": v}
                            for k, v in results["feature_importance"].items()
                        ]
                    )
                    st.bar_chart(fi_df.set_index("Feature"))

                    # Detailed table
                    with st.expander("Detailed SHAP Values"):
                        details_df = pd.DataFrame(results["feature_details"])
                        st.dataframe(details_df, use_container_width=True)

                except (KeyError, MLTrainingError, OSError, TypeError, ValueError) as e:
                    st.error(f"SHAP failed: {e!s}")
                    st.info("Ensure SHAP is installed: pip install shap")

    else:
        st.markdown("Enter values for a single prediction explanation:")
        feature_columns = ml_results.get("features", [])
        input_data = {}
        cols = st.columns(min(3, len(feature_columns)))
        for i, feat in enumerate(feature_columns):
            with cols[i % 3]:
                val = dataset.data[feat].median() if feat in dataset.data.columns else 0
                input_data[feat] = st.number_input(feat, value=float(val))

        if st.button("🔍 Explain Prediction", type="primary"):
            with st.spinner("Computing local explanation..."):
                try:
                    result = shap_service.explain_prediction(model_id, input_data)
                    st.metric("Prediction", f"{result['prediction']:.4f}")
                    if result.get("confidence"):
                        st.metric("Confidence", f"{result['confidence']:.2%}")

                    st.subheader("Top Positive Contributors")
                    for c in result["top_positive"]:
                        st.markdown(f"🟢 **{c['feature']}**: +{c['shap_value']:.4f}")

                    st.subheader("Top Negative Contributors")
                    for c in result["top_negative"]:
                        st.markdown(f"🔴 **{c['feature']}**: {c['shap_value']:.4f}")

                except (KeyError, MLTrainingError, OSError, TypeError, ValueError) as e:
                    st.error(f"Explanation failed: {e!s}")
