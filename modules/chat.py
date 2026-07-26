import streamlit as st


def show_chat():

    st.header("🤖 Assistente IA")

    pergunta = st.chat_input(
        "Pergunte qualquer coisa..."
    )

    if pergunta:

        st.chat_message("user").write(
            pergunta
        )

        resposta = "Resposta da IA"

        st.chat_message("assistant").write(
            resposta
        )
