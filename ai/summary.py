from __future__ import annotations

from ai.diagnostics import analyze_dataframe


def summarize(df) -> str:
    """
    Gera um resumo executivo do DataFrame.

    Todas as informações são obtidas do
    diagnostics.py para evitar processamento duplicado.
    """

    info = analyze_dataframe(df)

    linhas = [

        "# 📊 Resumo Executivo",

        "",

        "## Informações Gerais",

        f"• Registros: {info['rows']:,}",

        f"• Colunas: {info['columns']}",

        f"• Uso de memória: {info['memory_mb']} MB",

        "",

        "## Qualidade dos Dados",

        f"• Valores ausentes: {info['missing']}",

        f"• Registros duplicados: {info['duplicates']}",

        "",

        "## Tipos de Variáveis",

        f"• Numéricas: {len(info['numeric_columns'])}",

        f"• Categóricas: {len(info['categorical_columns'])}",

        f"• Booleanas: {len(info['boolean_columns'])}",

        f"• Datas: {len(info['datetime_columns'])}",

        ""

    ]

    # ------------------------------------
    # Colunas numéricas
    # ------------------------------------

    if info["numeric_summary"]:

        linhas.append("## Estatísticas Numéricas")
        linhas.append("")

        for coluna, dados in info["numeric_summary"].items():

            linhas.extend([

                f"### {coluna}",

                f"- Média: {dados['mean']:.2f}",

                f"- Mediana: {dados['median']:.2f}",

                f"- Desvio padrão: {dados['std']:.2f}",

                f"- Mínimo: {dados['min']:.2f}",

                f"- Máximo: {dados['max']:.2f}",

                ""

            ])

    # ------------------------------------
    # Colunas categóricas
    # ------------------------------------

    if info["categorical_summary"]:

        linhas.append("## Estatísticas Categóricas")
        linhas.append("")

        for coluna, dados in info["categorical_summary"].items():

            linhas.extend([

                f"### {coluna}",

                f"- Valores únicos: {dados['unique']}",

                f"- Valor mais frequente: {dados['top']}",

                f"- Frequência: {dados['frequency']}",

                f"- Valores ausentes: {dados['missing']}",

                ""

            ])

    # ------------------------------------
    # Outliers
    # ------------------------------------

    if info["outliers"]:

        linhas.append("## Possíveis Outliers")
        linhas.append("")

        encontrou = False

        for coluna, quantidade in info["outliers"].items():

            if quantidade > 0:

                encontrou = True

                linhas.append(
                    f"- {coluna}: {quantidade} possíveis outliers"
                )

        if not encontrou:

            linhas.append(
                "- Nenhum outlier relevante encontrado."
            )

        linhas.append("")

    # ------------------------------------
    # Recomendações
    # ------------------------------------

    if info["recommendations"]:

        linhas.append("## Recomendações")
        linhas.append("")

        for recomendacao in info["recommendations"]:

            linhas.append(
                f"- {recomendacao}"
            )

    return "\n".join(linhas)
