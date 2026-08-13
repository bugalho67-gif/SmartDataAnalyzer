"""Página de detecção de outliers e cálculos de suporte."""

import pandas as pd
import plotly.express as px
import streamlit as st
from ui.theme import apply_plotly_theme


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Detecta outliers em uma coluna pelo método do IQR (intervalo interquartil).

    Parameters
    ----------
    df : pd.DataFrame
        Dados de origem.
    column : str
        Nome da coluna numérica a analisar.

    Returns
    -------
    pd.DataFrame
        Subconjunto de `df` com as linhas consideradas outliers.
    """
    serie = df[column].dropna()

    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1

    inferior = q1 - 1.5 * iqr
    superior = q3 + 1.5 * iqr

    return df[(df[column] < inferior) | (df[column] > superior)]


def detect_outliers_zscore(
    df: pd.DataFrame,
    column: str,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Detecta outliers em uma coluna pelo método do Z-Score.

    Parameters
    ----------
    df : pd.DataFrame
        Dados de origem.
    column : str
        Nome da coluna numérica a analisar.
    threshold : float, default 3.0
        Z-score acima do qual um valor é considerado outlier.

    Returns
    -------
    pd.DataFrame
        Subconjunto de `df` com as linhas consideradas outliers.
        Vazio se a coluna tiver desvio padrão zero.
    """
    serie = df[column].dropna()

    if serie.std() == 0:
        return df.iloc[0:0]

    z = ((serie - serie.mean()) / serie.std()).abs()
    indices = z[z > threshold].index

    return df.loc[indices]


def show_outliers(df: pd.DataFrame) -> None:
    """Renderiza a página de detecção de outliers no Streamlit."""
    st.header("🚨 Outliers")

    numericas = df.select_dtypes(include="number").columns

    if len(numericas) == 0:
        st.warning("Nenhuma coluna numérica encontrada.")
        return

    coluna = st.selectbox("Coluna", numericas)
    metodo = st.radio("Método", ["IQR", "Z-Score"])

    if metodo == "IQR":
        outliers = detect_outliers_iqr(df, coluna)
    else:
        if df[coluna].dropna().std() == 0:
            st.warning(
                "Não é possível calcular o Z-Score porque todos "
                "os valores da coluna são iguais."
            )
            return
        outliers = detect_outliers_zscore(df, coluna)

    st.metric("Outliers encontrados", len(outliers))
    st.dataframe(outliers, use_container_width=True)

    fig = px.box(df, y=coluna, points="all")
    st.plotly_chart(apply_plotly_theme(fig), use_container_width=True)
