import streamlit as st

from core.logger import logger


class DataLoadError(Exception):
    """Erro ao carregar ou interpretar um arquivo de dados (CSV, Excel, JSON)."""


class AIError(Exception):
    """Erro ao consultar um provedor de IA (local ou externo)."""


class ExportError(Exception):
    """Erro ao gerar ou exportar um relatório (PDF, Excel, CSV, HTML)."""


class DatabaseError(Exception):
    """Erro ao conectar ou consultar um banco de dados externo."""


class ValidationError(Exception):
    """Erro de validação de dados de entrada."""


def show_error(error):

    logger.exception(str(error))

    st.error(
        f"""

Erro durante o processamento.

{error}

"""
    )
