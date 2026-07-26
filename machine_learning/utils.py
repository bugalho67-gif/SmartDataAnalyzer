import pandas as pd

def get_numeric_columns(df: pd.DataFrame):
    return df.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(df: pd.DataFrame):
    return df.select_dtypes(include="object").columns.tolist()


def get_datetime_columns(df: pd.DataFrame):
    return df.select_dtypes(include="datetime").columns.tolist()
