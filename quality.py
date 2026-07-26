import streamlit as st
import pandas as pd


def show_quality(df: pd.DataFrame):

    st.header("📋 Qualidade dos Dados")

    linhas = len(df)

    celulas = linhas * len(df.columns)

    nulos = df.isnull().sum().sum()

    duplicados = df.duplicated().sum()

    porcentagem = round(
        ((celulas - nulos) / celulas) * 100,
        2
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Qualidade",
        f"{porcentagem}%"
    )

    c2.metric(
        "Valores Nulos",
        int(nulos)
    )

    c3.metric(
        "Duplicados",
        int(duplicados)
    )

    st.subheader("Valores ausentes")

    st.dataframe(
        df.isnull().sum(),
        use_container_width=True
    )
