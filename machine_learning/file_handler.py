import streamlit as st

from machine_learning.loader import DataLoader
from core.cache import load_dataframe
from core.logger import logger


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
