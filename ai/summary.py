from ai.diagnostics import analyze_dataframe


def summarize(df):

    info = analyze_dataframe(df)

    return f"""
## Resumo da Base

📄 Registros: {info["rows"]:,}

📊 Colunas: {info["columns"]}

💾 Memória: {info["memory_mb"]} MB

❗ Valores ausentes: {info["missing"]}

📦 Duplicados: {info["duplicates"]}

🔢 Numéricas: {len(info["numeric_columns"])}

🏷️ Categóricas: {len(info["categorical_columns"])}
"""
