import streamlit as st

from modules.loader import DataLoader


def compare():

    st.header("📂 Comparar Arquivos")

    arquivo2 = st.file_uploader(
        "Segundo arquivo",
        type=["csv","xlsx","json"]
    )

    if arquivo2:

        df2 = DataLoader.load(
            arquivo2
        )

        st.metric(
            "Diferença de linhas",
            abs(len(df2))
        )

        st.metric(
            "Diferença de colunas",
            abs(len(df2.columns))
        )
