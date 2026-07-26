import streamlit as st

from modules.router import PAGES

from modules.ai import ai_summary


def render_page(
    menu,
    df
):

    if menu == "Relatório IA":

        st.header("🤖 Relatório Inteligente")

        st.write(
            ai_summary(df)
        )

        return

    pagina = PAGES.get(menu)

    if pagina is None:

        st.warning(
            "Página não encontrada."
        )

        return

    if menu == "Banco de Dados":

        pagina()

        return

    pagina(df)
