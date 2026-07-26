import streamlit as st

from ai.context_builder import build_context

from ai.local_client import LocalAIClient

from ai.chat_history import (

    initialize_chat,

    add_message,

    show_history

)


def show_chat(df):

    st.header("🤖 Assistente IA")

    initialize_chat()

    show_history()

    pergunta = st.chat_input(
        "Faça uma pergunta sobre seus dados..."
    )

    if not pergunta:

        return

    add_message(
        "user",
        pergunta
    )

    contexto = build_context(df)

    client = LocalAIClient()

    resposta = client.ask(

        pergunta,

        contexto

    )

    add_message(
        "assistant",
        resposta
    )

    st.rerun()
