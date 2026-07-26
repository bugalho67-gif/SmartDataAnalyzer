import streamlit as st
import pandas as pd
from modules.report import generate_pdf


def show_export(df: pd.DataFrame):

    st.header("📥 Exportar")

    if st.button("Gerar PDF"):

        generate_pdf(df)

        st.success("PDF gerado com sucesso!")

    excel = df.to_excel(
        "exports/dados.xlsx",
        index=False
    )

    with open(
        "exports/dados.xlsx",
        "rb"
    ) as arquivo:

        st.download_button(
            "Baixar Excel",
            arquivo,
            file_name="dados.xlsx"
        )

    csv = df.to_csv(index=False)

    st.download_button(
        "Baixar CSV",
        csv,
        file_name="dados.csv"
    )

    html = df.to_html()

    st.download_button(
        "Baixar HTML",
        html,
        file_name="dados.html"
    )
