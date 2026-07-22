import streamlit as st
from modules.overview import overview

def show_dashboard(df):

    dados = overview(df)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Linhas",
        f"{dados['rows']:,}"
    )

    c2.metric(
        "Colunas",
        dados["columns"]
    )

    c3.metric(
        "Memória (KB)",
        round(dados["memory"],2)
    )

    c4.metric(
        "Valores Nulos",
        dados["missing"]
    )

    c5.metric(
        "Duplicados",
        dados["duplicates"]
    )

    st.divider()

    st.subheader("Pré-visualização")

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )
