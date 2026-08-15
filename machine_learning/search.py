import streamlit as st


def search_dataframe(df):

    texto = st.sidebar.text_input("Pesquisar")

    if texto:
        mascara = df.astype(str).apply(
            lambda coluna: coluna.str.contains(texto, case=False, na=False)
        )

        df = df[mascara.any(axis=1)]

    return df
