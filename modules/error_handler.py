import streamlit as st

from modules.logger import logger


def show_error(error):

    logger.exception(str(error))

    st.error(

        f"""

Erro durante o processamento.

{error}

"""

    )
