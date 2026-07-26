import streamlit as st


def initialize():

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []


def add(role, text):

    st.session_state.chat_history.append({

        "role": role,

        "content": text

    })


def show():

    for message in st.session_state.chat_history:

        with st.chat_message(

            message["role"]

        ):

            st.markdown(

                message["content"]

            )
