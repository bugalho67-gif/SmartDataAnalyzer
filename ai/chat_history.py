from __future__ import annotations

import streamlit as st


def initialize_chat():

    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_message(role: str, content: str):

    st.session_state.messages.append({"role": role, "content": content})


def show_history():

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
