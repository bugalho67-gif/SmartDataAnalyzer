import streamlit as st


def show_progress():

    progress = st.progress(0)

    progress.progress(15)

    return progress


def update_progress(progress, value):

    progress.progress(value)


def finish_progress(progress):

    progress.progress(100)

    progress.empty()
