import streamlit as st


from app_config import (
    APP_NAME,
    SUPPORTED_FILES,
    MAX_UPLOAD_SIZE_MB
)


from machine_learning.sidebar import create_sidebar

from machine_learning.filters import apply_filters

from machine_learning.search import search_dataframe

from machine_learning.file_handler import process_uploaded_file

from machine_learning.page_controller import render_page

from machine_learning.progress import (
    show_progress,
    update_progress,
    finish_progress
)

from core.exceptions import show_error



st.set_page_config(

    page_title=APP_NAME,

    page_icon="📊",

    layout="wide"

)



menu = create_sidebar()


st.title(APP_NAME)



arquivo = st.file_uploader(

    "Selecione um arquivo",

    type=SUPPORTED_FILES

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



# Validação de tamanho

tamanho_mb = arquivo.size / (1024 * 1024)


if tamanho_mb > MAX_UPLOAD_SIZE_MB:

    st.error(
        f"O arquivo excede o limite de {MAX_UPLOAD_SIZE_MB} MB."
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
