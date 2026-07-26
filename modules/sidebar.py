import streamlit as st

def create_sidebar():

    st.sidebar.title("📊 Smart Data Analyzer")

    menu = st.sidebar.radio(
        "Navegação",
       [
           "Dashboard",
           "Estatísticas",
           "Gráficos",
           "Correlação",
           "Outliers",
           "Qualidade",
           "Insights",
           "Relatório IA",
           "Exportar"
           "Machine Learning",
           "Gráfico Inteligente",
           "Comparar Arquivos"
      ]
    )

    st.sidebar.divider()

    st.sidebar.info(
        """
Versão 1.0

Desenvolvido por Gabriel Bugalho
"""
    )

    return menu
