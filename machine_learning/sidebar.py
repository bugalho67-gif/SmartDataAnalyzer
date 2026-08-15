import streamlit as st


def create_sidebar():

    st.sidebar.markdown("### SmartDataAnalyzer")

    menu = st.sidebar.radio(
        "Navegação",
        [
            "Dashboard",
            "Dashboard Inteligente",
            "Estatísticas",
            "Gráficos",
            "Correlação",
            "Outliers",
            "Qualidade",
            "Insights",
            "Assistente IA",
            "Machine Learning",
            "Comparação",
            "Exportar",
            "Banco de Dados",
        ],
    )

    st.sidebar.divider()

    st.sidebar.info(
        """
Versão 1.0

Desenvolvido por Gabriel Bugalho
"""
    )

    return menu