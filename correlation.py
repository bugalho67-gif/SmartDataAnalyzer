import streamlit as st
import pandas as pd
import plotly.express as px


def show_correlation(df: pd.DataFrame):

    st.header("🔥 Correlação")

    numericas = df.select_dtypes(include="number")

    if numericas.shape[1] < 2:
        st.warning("São necessárias pelo menos duas colunas numéricas.")
        return

    metodo = st.selectbox(
        "Método",
        [
            "pearson",
            "spearman",
            "kendall"
        ]
    )

    matriz = numericas.corr(method=metodo)

    st.dataframe(
        matriz.round(3),
        use_container_width=True
    )

    fig = px.imshow(
        matriz,
        text_auto=".2f",
        aspect="auto",
        title=f"Heatmap ({metodo.title()})"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
