import pandas as pd


def ai_summary(df: pd.DataFrame):

    texto = []

    texto.append(
        f"O conjunto possui {len(df)} registros."
    )

    texto.append(
        f"Foram encontradas {len(df.columns)} colunas."
    )

    texto.append(
        f"Há {df.isnull().sum().sum()} valores ausentes."
    )

    texto.append(
        f"Foram encontrados {df.duplicated().sum()} registros duplicados."
    )

    numericas = df.select_dtypes(include="number")

    if len(numericas.columns):

        maior = numericas.mean().idxmax()

        texto.append(
            f"A coluna '{maior}' apresenta a maior média."
        )

    return "\n".join(texto)
