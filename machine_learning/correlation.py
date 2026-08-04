"""Página de análise de correlação e cálculo de suporte."""

import pandas as pd
import plotly.express as px
import streamlit as st


def calculate_correlation_matrix(
    df: pd.DataFrame,
    method: str = "pearson",
) -> pd.DataFrame:
    """
    Calcula a matriz de correlação das colunas numéricas de um DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dados de origem.
    method : str, default "pearson"
        Método de correlação: "pearson", "spearman" ou "kendall".

    Returns
    -------
    pd.DataFrame
        Matriz de correlação (não arredondada).
    """
    numericas = df.select_dtypes(include="number")
    return numericas.corr(method=method)


def show_correlation(df: pd.DataFrame) -> None:
    """Renderiza a página de correlação no Streamlit."""
    st.header("🔥 Correlação")

    numericas = df.select_dtypes(include="number")

    if numericas.shape[1] < 2:
        st.warning("São necessárias pelo menos duas colunas numéricas.")
        return

    metodo = st.selectbox("Método", ["pearson", "spearman", "kendall"])

    matriz = calculate_correlation_matrix(df, method=metodo)

    st.dataframe(matriz.round(3), use_container_width=True)

    fig = px.imshow(
        matriz,
        text_auto=".2f",
        aspect="auto",
        title=f"Heatmap ({metodo.title()})",
    )

    st.plotly_chart(fig, use_container_width=True)
