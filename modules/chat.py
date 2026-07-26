import streamlit as st

from ai.context_builder import build_context
from ai.local_client import LocalAIClient


def show_chat(df):

    st.header("🤖 Assistente IA")

    pergunta = st.chat_input(
        "Faça uma pergunta sobre seus dados..."
    )

    if not pergunta:
        return

    contexto = build_context(df)

    client = LocalAIClient()

    resposta = client.ask(
        pergunta,
        contexto
    )

    with st.chat_message("user"):

        st.write(pergunta)

    with st.chat_message("assistant"):

        st.write(resposta)
