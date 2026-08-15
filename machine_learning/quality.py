"""Página de qualidade dos dados e cálculo de suporte."""

import pandas as pd
import streamlit as st


def calculate_quality_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas básicas de qualidade de um DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dados de origem.

    Returns
    -------
    dict
        Dicionário com as chaves "quality_pct", "nulls" e "duplicates".
    """
    linhas = len(df)
    celulas = linhas * len(df.columns)
    nulos = int(df.isnull().sum().sum())
    duplicados = int(df.duplicated().sum())

    porcentagem = round(((celulas - nulos) / celulas) * 100, 2) if celulas > 0 else 0.0

    return {
        "quality_pct": porcentagem,
        "nulls": nulos,
        "duplicates": duplicados,
    }


def show_quality(df: pd.DataFrame) -> None:
    """Renderiza a página de qualidade dos dados no Streamlit."""
    st.header("📋 Qualidade dos Dados")

    metrics = calculate_quality_metrics(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Qualidade", f"{metrics['quality_pct']}%")
    c2.metric("Valores Nulos", metrics["nulls"])
    c3.metric("Duplicados", metrics["duplicates"])

    st.subheader("Valores ausentes")
    st.dataframe(df.isnull().sum(), use_container_width=True)
