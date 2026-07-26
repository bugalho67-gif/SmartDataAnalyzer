from ai.diagnostics import analyze_dataframe


def insights(df):

    info = analyze_dataframe(df)

    texto = []

    texto.append(
        f"📄 A base possui {info['rows']:,} registros."
    )

    texto.append(
        f"📊 Existem {info['columns']} colunas."
    )

    texto.append(
        f"🔢 Foram identificadas {len(info['numeric_columns'])} colunas numéricas."
    )

    texto.append(
        f"🏷️ Foram identificadas {len(info['categorical_columns'])} colunas categóricas."
    )

    if info["missing"] == 0:

        texto.append(
            "✅ Não existem valores ausentes."
        )

    else:

        texto.append(
            f"⚠️ Existem {info['missing']:,} valores ausentes."
        )

    if info["duplicates"] == 0:

        texto.append(
            "✅ Não existem registros duplicados."
        )

    else:

        texto.append(
            f"⚠️ Existem {info['duplicates']:,} registros duplicados."
        )

    texto.append("")

    texto.append("### Estatísticas Numéricas")

    for coluna, dados in info["numeric_summary"].items():

        texto.append(
            f"• **{coluna}**"
        )

        texto.append(
            f"  Média: {dados['mean']:.2f}"
        )

        texto.append(
            f"  Mediana: {dados['median']:.2f}"
        )

        texto.append(
            f"  Desvio Padrão: {dados['std']:.2f}"
        )

    return texto
