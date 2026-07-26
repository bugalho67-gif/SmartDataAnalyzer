from ai.diagnostics import analyze_dataframe


def summarize(df):

    info = analyze_dataframe(df)

    texto = f"""
## Resumo da Base

• Registros: {info["rows"]}

• Colunas: {info["columns"]}

• Valores ausentes: {info["missing"]}

• Registros duplicados: {info["duplicates"]}

• Variáveis numéricas: {len(info["numeric_columns"])}

• Variáveis categóricas: {len(info["categorical_columns"])}
"""

    return texto
