import streamlit as st

def create_sidebar():

    st.sidebar.title("📊 Smart Data Analyzer")

    menu = st.sidebar.radio(
        "Navegação",
       [
           "Dashboard",
           "Estatísticas",
           "Gráficos",
           "Gráfico Inteligente",
           "Correlação",
           "Outliers",
           "Qualidade",
           "Insights",
           "Machine Learning",
           "Comparar Arquivos",
           "Relatório IA",
           "Exportar"
           "Dashboard Executivo"
           "Banco de Dados"
           "Dashboard Inteligente"
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
