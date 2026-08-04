"""Página de insights automáticos e lógica de suporte."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def build_insights(df: pd.DataFrame) -> list[dict]:
    """
    Calcula uma lista de insights automáticos sobre um DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dados de origem.

    Returns
    -------
    list[dict]
        Cada item tem "type" ("success", "warning" ou "info") e
        "message" (str), na ordem em que devem ser exibidos.
    """
    insights = []

    linhas = len(df)
    colunas = len(df.columns)

    insights.append({
        "type": "success",
        "message": f"O conjunto possui {linhas:,} registros e {colunas} colunas.",
    })

    nulos = df.isnull().sum()
    if nulos.sum():
        coluna = nulos.idxmax()
        insights.append({
            "type": "warning",
            "message": f"A coluna '{coluna}' possui {nulos.max()} valores ausentes.",
        })

    duplicados = df.duplicated().sum()
    if duplicados:
        insights.append({
            "type": "warning",
            "message": f"Foram encontrados {duplicados} registros duplicados.",
        })

    numericas = df.select_dtypes(include="number")
    if len(numericas.columns):
        maior = numericas.std().idxmax()
        insights.append({
            "type": "info",
            "message": f"A coluna '{maior}' apresenta a maior dispersão.",
        })

        if len(numericas.columns) >= 2:
            correlacao = numericas.corr()
            correlacao.values[
                range(len(correlacao)),
                range(len(correlacao)),
            ] = 0

            maior_corr = correlacao.abs().stack().idxmax()
            insights.append({
                "type": "success",
                "message": f"Maior correlação entre {maior_corr[0]} e {maior_corr[1]}.",
            })

    return insights


def generate_insights(df: pd.DataFrame) -> None:
    """Renderiza a página de insights automáticos no Streamlit."""
    st.header("🧠 Insights Automáticos")

    renderers = {
        "success": st.success,
        "warning": st.warning,
        "info": st.info,
    }

    for item in build_insights(df):
        renderers[item["type"]](item["message"])
