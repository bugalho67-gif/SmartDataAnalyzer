import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def show_outliers(df: pd.DataFrame):

    st.header("🚨 Outliers")

    numericas = df.select_dtypes(include="number").columns

    if len(numericas) == 0:
        st.warning("Nenhuma coluna numérica encontrada.")
        return

    coluna = st.selectbox(
        "Coluna",
        numericas
    )

    metodo = st.radio(
        "Método",
        [
            "IQR",
            "Z-Score"
        ]
    )

    serie = df[coluna].dropna()

    if metodo == "IQR":

        q1 = serie.quantile(.25)
        q3 = serie.quantile(.75)

        iqr = q3 - q1

        inferior = q1 - 1.5 * iqr
        superior = q3 + 1.5 * iqr

        outliers = df[
            (df[coluna] < inferior) |
            (df[coluna] > superior)
        ]

    else:

        z = np.abs(
            (serie - serie.mean()) /
            serie.std()
        )

        outliers = df.loc[z > 3]

    st.metric(
        "Outliers encontrados",
        len(outliers)
    )

    st.dataframe(
        outliers,
        use_container_width=True
    )

    fig = px.box(
        df,
        y=coluna,
        points="all"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
