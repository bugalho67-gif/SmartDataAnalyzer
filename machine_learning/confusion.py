import streamlit as st

from sklearn.metrics import confusion_matrix

import plotly.express as px
from ui.theme import apply_plotly_theme


def show_confusion(y, pred):

    matriz = confusion_matrix(y, pred)

    fig = px.imshow(matriz, text_auto=True)

    st.plotly_chart(apply_plotly_theme(fig))
