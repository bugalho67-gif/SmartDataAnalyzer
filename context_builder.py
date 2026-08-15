import json

from ai.diagnostics import analyze_dataframe


def build_context(df):

    info = analyze_dataframe(df)

    contexto = {
        "dataset": {
            "rows": info["rows"],
            "columns": info["columns"],
            "memory": info["memory_mb"],
        },
        "quality": {"missing": info["missing"], "duplicates": info["duplicates"]},
        "numeric": info["numeric_summary"],
        "categorical": info["categorical_summary"],
        "recommendations": info["recommendations"],
    }

    return json.dumps(contexto, ensure_ascii=False, indent=4)
