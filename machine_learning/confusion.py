import streamlit as st

from sklearn.metrics import confusion_matrix

import plotly.express as px


def show_confusion(y, pred):

    matriz = confusion_matrix(
        y,
        pred
    )

    fig = px.imshow(
        matriz,
        text_auto=True
    )

    st.plotly_chart(fig)
