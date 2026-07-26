from __future__ import annotations

import json

import pandas as pd

from ai.diagnostics import analyze_dataframe


def build_context(
    df: pd.DataFrame
) -> str:
    """
    Constrói um contexto compacto
    para ser enviado à IA.
    """

    info = analyze_dataframe(df)

    contexto = {

        "registros": info["rows"],

        "colunas": info["columns"],

        "nomes_colunas": info["column_names"],

        "nulos": info["missing"],

        "duplicados": info["duplicates"],

        "colunas_numericas": info["numeric_columns"],

        "colunas_categoricas": info["categorical_columns"],

        "estatisticas": info["numeric_summary"],

        "categorias": info["categorical_summary"],

        "amostra": df.head(5).to_dict(
            orient="records"
        )

    }

    return json.dumps(
        contexto,
        indent=4,
        ensure_ascii=False
    )
