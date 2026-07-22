import streamlit as st

from config import APP_NAME
from modules.loader import DataLoader
from modules.sidebar import create_sidebar
from modules.dashboard import show_dashboard

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

menu = create_sidebar()

st.title(APP_NAME)

arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["csv","xlsx","json"]
)

if arquivo:

    df = DataLoader.load(arquivo)

    if menu == "Dashboard":

        show_dashboard(df)

    else:

        st.info(
            f"O módulo '{menu}' será implementado nas próximas etapas."
        )
