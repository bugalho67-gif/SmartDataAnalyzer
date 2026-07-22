import streamlit as st

from config import APP_NAME
from modules.loader import DataLoader

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart Data Analyzer")

st.write(
    "Faça upload de um arquivo CSV, Excel ou JSON."
)

arquivo = st.file_uploader(
    "Escolha um arquivo",
    type=["csv", "xlsx", "json"]
)

if arquivo:

    try:

        df = DataLoader.load(arquivo)

        st.success("Arquivo carregado com sucesso!")

        st.dataframe(df)

    except Exception as erro:

        st.error(erro)
