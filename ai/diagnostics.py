from __future__ import annotations

import pandas as pd
import numpy as np


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """
    Analisa um DataFrame e retorna um dicionário
    com informações utilizadas pelos módulos de IA.
    """

    numericas = df.select_dtypes(include=np.number)
    categoricas = df.select_dtypes(
        include=["object", "category", "bool"]
    )

    resultado = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "numeric_columns": list(numericas.columns),
        "categorical_columns": list(categoricas.columns),
        "numeric_summary": {},
        "categorical_summary": {},
        "recommendations": [],
    }

    # -----------------------------
    # Estatísticas numéricas
    # -----------------------------

    for coluna in numericas.columns:

        resultado["numeric_summary"][coluna] = {
            "mean": float(numericas[coluna].mean()),
            "median": float(numericas[coluna].median()),
            "std": float(numericas[coluna].std()),
            "min": float(numericas[coluna].min()),
            "max": float(numericas[coluna].max()),
        }

    # -----------------------------
    # Estatísticas categóricas
    # -----------------------------

    for coluna in categoricas.columns:

        moda = categoricas[coluna].mode()

        resultado["categorical_summary"][coluna] = {
            "unique": int(categoricas[coluna].nunique()),
            "most_common": (
                str(moda.iloc[0])
                if len(moda) > 0
                else "N/A"
            )
        }

    # -----------------------------
    # Recomendações
    # -----------------------------

    if resultado["missing"] > 0:
        resultado["recommendations"].append(
            "Existem valores ausentes que podem afetar a análise."
        )

    if resultado["duplicates"] > 0:
        resultado["recommendations"].append(
            "Existem registros duplicados."
        )

    if len(resultado["numeric_columns"]) == 0:
        resultado["recommendations"].append(
            "Nenhuma variável numérica encontrada."
        )

    if len(resultado["categorical_columns"]) == 0:
        resultado["recommendations"].append(
            "Nenhuma variável categórica encontrada."
        )

    return resultado
