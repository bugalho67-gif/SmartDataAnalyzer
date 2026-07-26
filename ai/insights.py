from ai.diagnostics import analyze_dataframe


def insights(df):

    info = analyze_dataframe(df)

    texto = []

    # ==========================================
    # Resumo geral
    # ==========================================

    texto.append(f"📄 A base possui {info['rows']:,} registros.")
    texto.append(f"📊 Foram encontradas {info['columns']} colunas.")
    texto.append(f"💾 O dataset ocupa {info['memory_mb']} MB.")
    texto.append(f"❗ Valores ausentes: {info['missing']}")
    texto.append(f"📦 Registros duplicados: {info['duplicates']}")

    texto.append("")

    # ==========================================
    # Estatísticas numéricas
    # ==========================================

    if info["numeric_summary"]:

        texto.append("## 🔢 Colunas Numéricas")

        for coluna, dados in info["numeric_summary"].items():

            texto.append(
                f"""
### {coluna}

• Média: {dados['mean']:.2f}

• Mediana: {dados['median']:.2f}

• Desvio padrão: {dados['std']:.2f}

• Mínimo: {dados['min']:.2f}

• Máximo: {dados['max']:.2f}
"""
            )

    # ==========================================
    # Colunas categóricas
    # ==========================================

    if info["categorical_summary"]:

        texto.append("")
        texto.append("## 🏷️ Colunas Categóricas")

        for coluna, dados in info["categorical_summary"].items():

            texto.append(
                f"""
### {coluna}

• Valores únicos: {dados['unique']}

• Valor mais frequente: {dados['top']}

• Frequência: {dados['frequency']}

• Valores ausentes: {dados['missing']}
"""
            )

    # ==========================================
    # Recomendações
    # ==========================================

    if info["recommendations"]:

        texto.append("")
        texto.append("## 💡 Recomendações")

        for recomendacao in info["recommendations"]:

            texto.append(f"• {recomendacao}")

    return texto
