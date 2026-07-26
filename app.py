import streamlit as st

from config import APP_NAME

from modules.sidebar import create_sidebar

from modules.filters import apply_filters

from modules.search import search_dataframe

from modules.file_handler import process_uploaded_file

from modules.page_controller import render_page

from modules.progress import (
    show_progress,
    update_progress,
    finish_progress
)

from modules.error_handler import show_error


st.set_page_config(

    page_title=APP_NAME,

    page_icon="📊",

    layout="wide"

)

menu = create_sidebar()

st.title(APP_NAME)

arquivo = st.file_uploader(

    "Selecione um arquivo",

    type=[

        "csv",

        "xlsx",

        "json"

    ]

)

# -------------------------------
# Banco de Dados
# -------------------------------

if menu == "Banco de Dados":

    render_page(
        menu,
        None
    )

    st.stop()

# -------------------------------
# Upload
# -------------------------------

if arquivo is None:

    st.info(

        "Faça o upload de um arquivo."

    )

    st.stop()

try:

    progress = show_progress()

    df = process_uploaded_file(
        arquivo
    )

    update_progress(
        progress,
        40
    )

    df = apply_filters(
        df
    )

    update_progress(
        progress,
        70
    )

    df = search_dataframe(
        df
    )

    update_progress(
        progress,
        90
    )

    render_page(
        menu,
        df
    )

    finish_progress(
        progress
    )

except Exception as erro:

    show_error(
        erro
    )
