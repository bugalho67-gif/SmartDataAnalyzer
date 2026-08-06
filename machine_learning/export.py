import os
from pathlib import Path

import streamlit as st
import pandas as pd

from machine_learning.report import generate_pdf
from core.exceptions import ExportError, show_error


def show_export(df: pd.DataFrame):
    st.header("📥 Exportar")

    # Garante que a pasta exports existe
    Path("exports").mkdir(exist_ok=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 Gerar PDF"):
            try:
                generate_pdf(df)
                st.success("PDF gerado com sucesso!")
            except Exception as exc:
                show_error(ExportError(f"Falha ao gerar PDF: {exc}"))

    with col2:
        try:
            excel_path = "exports/dados.xlsx"
            df.to_excel(excel_path, index=False)
            with open(excel_path, "rb") as arquivo:
                st.download_button(
                    "📊 Baixar Excel",
                    arquivo,
                    file_name="dados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as exc:
            show_error(ExportError(f"Falha ao gerar Excel: {exc}"))

    with col3:
        try:
            csv = df.to_csv(index=False)
            st.download_button(
                "📋 Baixar CSV",
                csv,
                file_name="dados.csv",
                mime="text/csv"
            )
        except Exception as exc:
            show_error(ExportError(f"Falha ao gerar CSV: {exc}"))

    with col4:
        try:
            html = df.to_html()
            st.download_button(
                "🌐 Baixar HTML",
                html,
                file_name="dados.html",
                mime="text/html"
            )
        except Exception as exc:
            show_error(ExportError(f"Falha ao gerar HTML: {exc}"))
            
