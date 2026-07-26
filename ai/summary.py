import pandas as pd


def summarize(df):

    texto = f"""

    A base possui

    {len(df)} registros.

    Existem

    {len(df.columns)}

    colunas.

    Foram encontrados

    {df.isnull().sum().sum()}

    valores ausentes.

    """

    return texto
