import streamlit as st


def executive_dashboard(df):

    st.header("📊 Dashboard Executivo")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Registros", len(df))

    c2.metric("Colunas", len(df.columns))

    c3.metric("Nulos", df.isnull().sum().sum())

    c4.metric("Duplicados", df.duplicated().sum())

    st.success("Base pronta para análise.")
