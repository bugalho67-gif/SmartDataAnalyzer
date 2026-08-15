from __future__ import annotations

import pandas as pd
import numpy as np


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """
    Analisa completamente um DataFrame e retorna todas
    as informações utilizadas pelo restante da aplicação.

    Returns
    -------
    dict
        Dicionário contendo estatísticas, métricas e
        recomendações.
    """

    resultado = {}

    # ======================================================
    # Informações gerais
    # ======================================================

    resultado["rows"] = len(df)

    resultado["columns"] = len(df.columns)

    resultado["column_names"] = list(df.columns)

    resultado["shape"] = df.shape

    resultado["memory_mb"] = round(df.memory_usage(deep=True).sum() / 1024**2, 2)

    # ======================================================
    # Qualidade
    # ======================================================

    resultado["missing"] = int(df.isna().sum().sum())

    resultado["duplicates"] = int(df.duplicated().sum())

    resultado["missing_per_column"] = (
        df.isna().sum().sort_values(ascending=False).to_dict()
    )

    # ======================================================
    # Tipos
    # ======================================================

    numericas = list(df.select_dtypes(include=np.number).columns)

    booleanas = list(df.select_dtypes(include="bool").columns)

    datas = list(df.select_dtypes(include="datetime").columns)

    categoricas = [
        c
        for c in df.columns
        if c not in numericas and c not in booleanas and c not in datas
    ]

    resultado["numeric_columns"] = numericas

    resultado["boolean_columns"] = booleanas

    resultado["datetime_columns"] = datas

    resultado["categorical_columns"] = categoricas

    # ======================================================
    # Estatísticas Numéricas
    # ======================================================

    numeric_summary = {}

    for coluna in numericas:
        serie = df[coluna].dropna()

        if serie.empty:
            continue

        numeric_summary[coluna] = {
            "count": int(serie.count()),
            "mean": float(serie.mean()),
            "median": float(serie.median()),
            "std": float(serie.std()) if len(serie) > 1 else 0,
            "min": float(serie.min()),
            "max": float(serie.max()),
            "q1": float(serie.quantile(0.25)),
            "q3": float(serie.quantile(0.75)),
            "variance": float(serie.var()) if len(serie) > 1 else 0,
            "skew": float(serie.skew()) if len(serie) > 2 else 0,
            "kurtosis": float(serie.kurtosis()) if len(serie) > 3 else 0,
        }

    resultado["numeric_summary"] = numeric_summary

    # ======================================================
    # Estatísticas Categóricas
    # ======================================================

    categorical_summary = {}

    for coluna in categoricas:
        serie = df[coluna]

        moda = serie.mode()

        categorical_summary[coluna] = {
            "unique": int(serie.nunique(dropna=True)),
            "missing": int(serie.isna().sum()),
            "top": (str(moda.iloc[0]) if not moda.empty else None),
            "frequency": (
                int(serie.value_counts(dropna=False).iloc[0]) if len(serie) > 0 else 0
            ),
        }

    resultado["categorical_summary"] = categorical_summary

    # ======================================================
    # Correlação
    # ======================================================

    if len(numericas) >= 2:
        resultado["correlation"] = df[numericas].corr(numeric_only=True).round(3)

    else:
        resultado["correlation"] = None

    # ======================================================
    # Outliers (IQR)
    # ======================================================

    outliers = {}

    for coluna in numericas:
        serie = df[coluna].dropna()

        if serie.empty:
            continue

        q1 = serie.quantile(0.25)

        q3 = serie.quantile(0.75)

        iqr = q3 - q1

        inferior = q1 - 1.5 * iqr

        superior = q3 + 1.5 * iqr

        quantidade = int(((serie < inferior) | (serie > superior)).sum())

        outliers[coluna] = quantidade

    resultado["outliers"] = outliers

    # ======================================================
    # Recomendações
    # ======================================================

    recomendacoes = []

    if resultado["missing"] > 0:
        recomendacoes.append("Existem valores ausentes que podem afetar as análises.")

    if resultado["duplicates"] > 0:
        recomendacoes.append("Foram encontrados registros duplicados.")

    if len(numericas) == 0:
        recomendacoes.append("Não existem colunas numéricas.")

    if len(categoricas) == 0:
        recomendacoes.append("Não existem colunas categóricas.")

    if resultado["memory_mb"] > 300:
        recomendacoes.append("Dataset grande. Considere utilizar cache.")

    for coluna, qtd in outliers.items():
        if qtd > 0:
            recomendacoes.append(f"{coluna} possui {qtd} possíveis outliers.")

    resultado["recommendations"] = recomendacoes

    return resultado
