from ai.diagnostics import analyze_dataframe


def insights(df):

    info = analyze_dataframe(df)

    texto = []

    texto.append(
        f"A base possui {info['rows']:,} registros."
    )

    texto.append(
        f"Foram encontradas {info['columns']} colunas."
    )

    texto.append(
        f"O dataset ocupa {info['memory_mb']} MB."
    )

    texto.append("")

    texto.append("Colunas Numéricas")

    for coluna, dados in info["numeric_summary"].items():

        texto.append(

            f"""
{coluna}

• Média: {dados['mean']:.2f}

• Mediana: {dados['median']:.2f}

• Desvio: {dados['std']:.2f}

• Min: {dados['min']:.2f}

• Max: {dados['max']:.2f}
"""

        )

    return texto
