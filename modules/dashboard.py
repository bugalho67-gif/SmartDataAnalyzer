import streamlit as st
from modules.overview import overview


def show_dashboard(df):

    dados = overview(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📄 Registros",
        f"{dados['rows']:,}"
    )

    c2.metric(
        "📊 Colunas",
        dados["columns"]
    )

    c3.metric(
        "❗ Nulos",
        dados["missing"]
    )

    c4.metric(
        "📦 Duplicados",
        dados["duplicates"]
    )

    st.divider()

    st.subheader("Pré-visualização")

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )
