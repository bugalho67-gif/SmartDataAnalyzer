import streamlit as st

from sklearn.metrics import roc_curve, auc

import plotly.graph_objects as go


def show_roc(y, prob):

    fpr, tpr, _ = roc_curve(
        y,
        prob
    )

    area = auc(
        fpr,
        tpr
    )

    fig = go.Figure()

    fig.add_scatter(
        x=fpr,
        y=tpr,
        name=f"AUC={area:.3f}"
    )

    st.plotly_chart(fig)
