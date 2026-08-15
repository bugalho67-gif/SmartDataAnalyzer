import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame):

    st.sidebar.subheader("Filtros")

    dataframe = df.copy()

    for coluna in dataframe.columns:
        if dataframe[coluna].dtype == "object":
            valores = dataframe[coluna].dropna().unique()

            if len(valores) <= 30:
                selecionados = st.sidebar.multiselect(coluna, valores, default=valores)

                dataframe = dataframe[dataframe[coluna].isin(selecionados)]

    return dataframe
