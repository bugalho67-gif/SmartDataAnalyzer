import streamlit as st

from machine_learning.router import PAGES

from machine_learning.ai import ai_summary


def render_page(menu, df):

    if menu == "Relatório IA":
        st.header("🤖 Relatório Inteligente")

        st.write(ai_summary(df))

        return

    pagina = PAGES.get(menu)

    if pagina is None:
        st.warning("Página não encontrada.")

        return

    if menu == "Banco de Dados":
        pagina()

        return

    pagina(df)
