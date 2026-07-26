from __future__ import annotations

from ai.diagnostics import analyze_dataframe


def recommendations(df) -> list[str]:
    """
    Gera recomendações automáticas com base
    na análise do DataFrame.
    """

    info = analyze_dataframe(df)

    dicas = []

    # ==========================================
    # Recomendações do diagnostics.py
    # ==========================================

    dicas.extend(info["recommendations"])

    # ==========================================
    # Tamanho do dataset
    # ==========================================

    if info["rows"] < 100:

        dicas.append(
            "O conjunto de dados possui poucos registros. Alguns modelos de Machine Learning podem não apresentar bom desempenho."
        )

    elif info["rows"] > 100_000:

        dicas.append(
            "O dataset é grande. Utilize filtros e cache para melhorar o desempenho da aplicação."
        )

    # ==========================================
    # Quantidade de colunas
    # ==========================================

    if len(info["numeric_columns"]) > 20:

        dicas.append(
            "Considere utilizar técnicas de seleção de atributos ou redução de dimensionalidade (PCA)."
        )

    # ==========================================
    # Memória
    # ==========================================

    if info["memory_mb"] > 500:

        dicas.append(
            "O consumo de memória é elevado. Avalie remover colunas desnecessárias ou utilizar processamento em lotes."
        )

    # ==========================================
    # Valores ausentes
    # ==========================================

    if info["missing"] > 0:

        dicas.append(
            "Analise a possibilidade de tratar valores ausentes utilizando preenchimento, remoção ou interpolação."
        )

    # ==========================================
    # Duplicados
    # ==========================================

    if info["duplicates"] > 0:

        dicas.append(
            "Considere remover registros duplicados antes de realizar análises estatísticas ou treinar modelos."
        )

    # ==========================================
    # Outliers
    # ==========================================

    for coluna, quantidade in info["outliers"].items():

        if quantidade > 0:

            dicas.append(
                f"A coluna '{coluna}' possui {quantidade} possíveis outliers. Avalie se eles representam erros ou eventos reais."
            )

    # ==========================================
    # Correlação
    # ==========================================

    if info["correlation"] is not None:

        matriz = info["correlation"]

        fortes = []

        for coluna in matriz.columns:

            for outra in matriz.columns:

                if coluna == outra:
                    continue

                valor = abs(matriz.loc[coluna, outra])

                if valor >= 0.90:

                    par = tuple(sorted((coluna, outra)))

                    if par not in fortes:

                        fortes.append(par)

        if fortes:

            dicas.append(
                "Existem variáveis altamente correlacionadas. Considere remover redundâncias antes do treinamento de modelos."
            )

    # ==========================================
    # Caso nenhuma recomendação exista
    # ==========================================

    if not dicas:

        dicas.append(
            "Nenhuma recomendação importante foi identificada. O conjunto de dados apresenta boa qualidade inicial."
        )

    # ==========================================
    # Remove duplicatas preservando ordem
    # ==========================================

    dicas = list(dict.fromkeys(dicas))

    return dicas
