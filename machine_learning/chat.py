import streamlit as st

from ai.ai_factory import get_provider
from ai.context_builder import build_context
from ai.chat_history import (
    initialize_chat,
    add_message,
    show_history,
)
from core.exceptions import AIError, show_error


def show_chat(df):
    st.header("🤖 Assistente IA")

    initialize_chat()
    show_history()

    pergunta = st.chat_input("Faça uma pergunta sobre seus dados...")

    if not pergunta:
        return

    add_message("user", pergunta)

    try:
        contexto = build_context(df)
        client = get_provider()
        resposta = client.ask(pergunta, contexto)
        add_message("assistant", resposta)
    except AIError as erro:
        show_error(erro)
        add_message(
            "assistant",
            "⚠️ Não foi possível obter uma resposta. "
            "Verifique a configuração do provedor de IA.",
        )
    except Exception as erro:
        show_error(erro)
        add_message(
            "assistant", "⚠️ Ocorreu um erro inesperado ao processar sua pergunta."
        )

    st.rerun()
