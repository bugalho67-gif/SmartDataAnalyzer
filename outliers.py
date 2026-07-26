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

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)

        iqr = q3 - q1

        inferior = q1 - 1.5 * iqr
        superior = q3 + 1.5 * iqr

        outliers = df[
            (df[coluna] < inferior) |
            (df[coluna] > superior)
        ]

    else:

        if serie.std() == 0:
            st.warning(
                "Não é possível calcular o Z-Score porque todos os valores da coluna são iguais."
            )
            return

        z = ((serie - serie.mean()) / serie.std()).abs()

        indices = z[z > 3].index

        outliers = df.loc[indices]

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
