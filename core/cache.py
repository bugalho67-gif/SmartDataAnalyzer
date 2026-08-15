import streamlit as st


@st.cache_data(show_spinner=False)
def load_dataframe(loader, arquivo):
    """
    Mantém o DataFrame em cache para evitar
    recarregamentos desnecessários.
    """
    return loader.load(arquivo)
