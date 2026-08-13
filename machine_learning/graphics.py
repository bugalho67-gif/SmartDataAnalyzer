import streamlit as st
import plotly.express as px
import pandas as pd
from ui.theme import apply_plotly_theme


def show_graphics(df: pd.DataFrame):

    st.header("📊 Gráficos")

    numericas = df.select_dtypes(include="number").columns

    categoricas = df.select_dtypes(include="object").columns

    if len(numericas):

        coluna = st.selectbox(
            "Coluna Numérica",
            numericas
        )

        fig = px.histogram(
            df,
            x=coluna,
            nbins=30,
            title=f"Distribuição de {coluna}"
        )

        st.plotly_chart(
            apply_plotly_theme(fig),
            use_container_width=True
        )

        fig = px.box(
            df,
            y=coluna,
            title=f"BoxPlot de {coluna}"
        )

        st.plotly_chart(
            apply_plotly_theme(fig),
            use_container_width=True
        )

    if len(categoricas):

        categoria = st.selectbox(
            "Coluna Categórica",
            categoricas
        )

        valores = df[categoria].value_counts().reset_index()

        valores.columns = [categoria, "Quantidade"]

        fig = px.bar(
            valores,
            x=categoria,
            y="Quantidade",
            title=f"Distribuição de {categoria}"
        )

        st.plotly_chart(
            apply_plotly_theme(fig),
            use_container_width=True
        )

        fig = px.pie(
            valores,
            names=categoria,
            values="Quantidade",
            title=f"Proporção de {categoria}"
        )

        st.plotly_chart(
            apply_plotly_theme(fig),
            use_container_width=True
        )

    if len(numericas) >= 2:

        st.subheader("Dispersão")

        x = st.selectbox(
            "Eixo X",
            numericas,
            key="scatter_x"
        )

        y = st.selectbox(
            "Eixo Y",
            numericas,
            key="scatter_y"
        )

        fig = px.scatter(
            df,
            x=x,
            y=y,
            trendline="ols",
            title=f"{x} × {y}"
        )

        st.plotly_chart(
            apply_plotly_theme(fig),
            use_container_width=True
        )
