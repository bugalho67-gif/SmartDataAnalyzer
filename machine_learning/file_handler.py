import streamlit as st

from modules.loader import DataLoader
from modules.cache import load_dataframe
from modules.logger import logger


def process_uploaded_file(arquivo):

    with st.spinner("Processando arquivo..."):

        df = load_dataframe(
            DataLoader,
            arquivo
        )

    logger.info(
        f"Arquivo '{arquivo.name}' carregado."
    )

    return df
