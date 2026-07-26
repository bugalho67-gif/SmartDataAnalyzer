import streamlit as st
import pandas as pd


def generate_insights(df: pd.DataFrame):

    st.header("🧠 Insights Automáticos")

    linhas = len(df)

    colunas = len(df.columns)

    st.success(
        f"O conjunto possui {linhas:,} registros e {colunas} colunas."
    )

    nulos = df.isnull().sum()

    if nulos.sum():

        coluna = nulos.idxmax()

        st.warning(
            f"A coluna '{coluna}' possui "
            f"{nulos.max()} valores ausentes."
        )

    duplicados = df.duplicated().sum()

    if duplicados:

        st.warning(
            f"Foram encontrados {duplicados} registros duplicados."
        )

    numericas = df.select_dtypes(include="number")

    if len(numericas.columns):

        maior = numericas.std().idxmax()

        st.info(
            f"A coluna '{maior}' apresenta a maior dispersão."
        )

        correlacao = numericas.corr()

        correlacao.values[
            range(len(correlacao)),
            range(len(correlacao))
        ] = 0

        maior_corr = correlacao.abs().stack().idxmax()

        st.success(
            f"Maior correlação entre "
            f"{maior_corr[0]} e {maior_corr[1]}."
        )
