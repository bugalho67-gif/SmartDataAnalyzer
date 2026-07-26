import pandas as pd
import numpy as np


def insights(df: pd.DataFrame) -> list[str]:
    """
    Gera insights automáticos sobre o DataFrame.
    """

    texto = []

    # Informações gerais
    texto.append(f"📄 A base possui {len(df):,} registros.")
    texto.append(f"📊 Foram encontradas {len(df.columns)} colunas.")

    # Valores ausentes
    nulos = int(df.isnull().sum().sum())

    if nulos == 0:
        texto.append("✅ Não foram encontrados valores ausentes.")
    else:
        texto.append(f"⚠️ Foram encontrados {nulos:,} valores ausentes.")

    # Duplicados
    duplicados = int(df.duplicated().sum())

    if duplicados == 0:
        texto.append("✅ Não existem registros duplicados.")
    else:
        texto.append(f"⚠️ Existem {duplicados:,} registros duplicados.")

    # Numéricas
    numericas = df.select_dtypes(include=np.number)

    if not numericas.empty:

        texto.append(
            f"🔢 Existem {len(numericas.columns)} variáveis numéricas."
        )

        for coluna in numericas.columns:

            texto.append(
                f"• {coluna}: média = {numericas[coluna].mean():.2f}"
            )

    # Categóricas
    categoricas = df.select_dtypes(include=["object", "category", "bool"])

    if not categoricas.empty:

        texto.append(
            f"🏷️ Existem {len(categoricas.columns)} variáveis categóricas."
        )

        for coluna in categoricas.columns:

            moda = categoricas[coluna].mode()

            if len(moda) > 0:

                texto.append(
                    f"• {coluna}: valor mais frequente = {moda.iloc[0]}"
                )

    return texto
