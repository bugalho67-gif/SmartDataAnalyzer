import streamlit as st
import plotly.express as px
from ui.theme import apply_plotly_theme


def auto_chart(df):

    st.header("📊 Gráfico Inteligente")

    coluna = st.selectbox(
        "Coluna",
        df.columns
    )

    if df[coluna].dtype == "object":

        fig = px.bar(
            df[coluna].value_counts().reset_index(),
            x="index",
            y=coluna
        )

    else:

        fig = px.histogram(
            df,
            x=coluna
        )

    st.plotly_chart(
        apply_plotly_theme(fig),
        use_container_width=True
    )
