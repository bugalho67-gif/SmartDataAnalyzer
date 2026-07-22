import pandas as pd

def overview(df: pd.DataFrame):

    memoria = df.memory_usage(deep=True).sum()

    return {

        "rows": df.shape[0],

        "columns": df.shape[1],

        "memory": memoria / 1024,

        "missing": int(df.isnull().sum().sum()),

        "duplicates": int(df.duplicated().sum())

    }
