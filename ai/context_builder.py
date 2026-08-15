"""Constrói o contexto enviado ao modelo de IA a partir do DataFrame."""

import pandas as pd

from app_config import MAX_AI_CONTEXT_ROWS


def build_context(df: pd.DataFrame) -> str:
    """
    Gera um resumo textual do DataFrame para ser usado
    como contexto pelo modelo de IA.

    Parameters
    ----------
    df : pd.DataFrame
        Conjunto de dados carregado pelo usuário.

    Returns
    -------
    str
        Texto com estatísticas e amostra dos dados.
    """
    linhas = len(df)
    colunas = len(df.columns)
    amostra = df.head(MAX_AI_CONTEXT_ROWS).to_string(index=False)

    resumo = f"""
Resumo do conjunto de dados:
- Registros: {linhas}
- Colunas: {colunas}
- Colunas disponíveis: {", ".join(df.columns)}
- Tipos de dados:
{df.dtypes.to_string()}

Amostra dos primeiros {min(linhas, MAX_AI_CONTEXT_ROWS)} registros:
{amostra}
"""
    return resumo.strip()
