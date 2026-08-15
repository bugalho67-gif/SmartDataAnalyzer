import streamlit as st
import pandas as pd

from core.exceptions import DataLoadError
from machine_learning.loader import DataLoader


def compare(df: pd.DataFrame):
    """
    Compara o conjunto de dados atual com um segundo arquivo.
    """

    st.header("📂 Comparação de Arquivos")

    arquivo2 = st.file_uploader(
        "Selecione o segundo arquivo",
        type=["csv", "xlsx", "json"],
        key="comparison_file",
    )

    if arquivo2 is None:
        st.info("Faça o upload de um segundo arquivo para iniciar a comparação.")
        return

    try:
        df2 = DataLoader.load(arquivo2)

        st.subheader("📊 Resumo da Comparação")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Diferença de Linhas", abs(len(df) - len(df2)))

        c2.metric("Diferença de Colunas", abs(df.shape[1] - df2.shape[1]))

        c3.metric("Linhas Arquivo 1", len(df))

        c4.metric("Linhas Arquivo 2", len(df2))

        st.divider()

        st.subheader("📋 Informações Gerais")

        resumo = pd.DataFrame(
            {
                "Arquivo 1": [
                    len(df),
                    df.shape[1],
                    int(df.isnull().sum().sum()),
                    int(df.duplicated().sum()),
                ],
                "Arquivo 2": [
                    len(df2),
                    df2.shape[1],
                    int(df2.isnull().sum().sum()),
                    int(df2.duplicated().sum()),
                ],
            },
            index=["Linhas", "Colunas", "Valores Nulos", "Duplicados"],
        )

        st.dataframe(resumo, use_container_width=True)

        st.divider()

        st.subheader("📑 Comparação das Colunas")

        somente_arquivo1 = sorted(set(df.columns) - set(df2.columns))

        somente_arquivo2 = sorted(set(df2.columns) - set(df.columns))

        comuns = sorted(set(df.columns).intersection(df2.columns))

        c1, c2 = st.columns(2)

        with c1:
            st.write("### Apenas no Arquivo 1")

            if somente_arquivo1:
                st.write(somente_arquivo1)
            else:
                st.success("Nenhuma")

        with c2:
            st.write("### Apenas no Arquivo 2")

            if somente_arquivo2:
                st.write(somente_arquivo2)
            else:
                st.success("Nenhuma")

        st.write("### Colunas em Comum")

        st.write(comuns)

        st.divider()

        st.subheader("🔍 Comparação dos Tipos de Dados")

        tipos = pd.DataFrame(
            {"Arquivo 1": df.dtypes.astype(str), "Arquivo 2": df2.dtypes.astype(str)}
        )

        st.dataframe(tipos, use_container_width=True)

    except (DataLoadError, KeyError, TypeError, ValueError) as erro:
        st.error(f"Erro ao comparar os arquivos:\n\n{erro}")
