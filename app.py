import streamlit as st

from config import APP_NAME

from modules.loader import DataLoader
from modules.cache import load_dataframe
from modules.logger import logger

from modules.sidebar import create_sidebar
from modules.filters import apply_filters
from modules.search import search_dataframe
from modules.ai import ai_summary
from modules.router import PAGES


st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

menu = create_sidebar()

st.title(APP_NAME)

st.write(
    "Faça o upload de um arquivo CSV, Excel ou JSON para iniciar a análise."
)

arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["csv", "xlsx", "json"]
)

if arquivo:

    try:

        with st.spinner("Processando arquivo..."):

            df = load_dataframe(
                DataLoader,
                arquivo
            )

        logger.info(
            f"Arquivo '{arquivo.name}' carregado."
        )

        progress = st.progress(0)

        for i in range(100):
            progress.progress(i + 1)

        progress.empty()

        df = apply_filters(df)

        df = search_dataframe(df)

        if menu == "Relatório IA":

            st.subheader("🤖 Relatório Inteligente")

            st.write(
                ai_summary(df)
            )

        elif menu in PAGES:

            PAGES[menu](df)

        else:

            st.warning(
                "Módulo ainda não implementado."
            )

    except Exception as erro:

        logger.exception("Erro durante o processamento do arquivo.")

        st.error(
            f"Erro ao carregar o arquivo:\n\n{erro}"
        )

else:

    st.info(
        "📁 Faça o upload de um arquivo para começar."
    )
