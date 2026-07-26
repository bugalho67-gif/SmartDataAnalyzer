import pandas as pd


def build_context(df: pd.DataFrame) -> str:

    texto = f"""

A base possui:

- {len(df)} linhas

- {len(df.columns)} colunas

Colunas:

"""

    for coluna in df.columns:

        texto += f"\n• {coluna}"

    texto += "\n\nPrimeiras linhas:\n"

    texto += df.head(10).to_string()

    return texto
