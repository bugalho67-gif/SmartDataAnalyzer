from ai.diagnostics import analyze_dataframe


def recommendations(df):

    info = analyze_dataframe(df)

    dicas = []

    if info["recommendations"]:

        dicas.extend(info["recommendations"])

    else:

        dicas.append(
            "A base apresenta boa qualidade inicial."
        )

    if len(info["numeric_columns"]) > 15:

        dicas.append(
            "Considere utilizar PCA ou seleção de variáveis para reduzir dimensionalidade."
        )

    if info["rows"] > 100000:

        dicas.append(
            "Utilize cache e filtros antes de gerar gráficos pesados."
        )

    if info["rows"] < 100:

        dicas.append(
            "A quantidade de registros é pequena para alguns modelos de Machine Learning."
        )

    return dicas
