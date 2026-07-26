import streamlit as st

from config import APP_NAME
from modules.loader import DataLoader
from modules.sidebar import create_sidebar
from modules.dashboard import show_dashboard
from modules.statistics import show_statistics
from modules.graphics import show_graphics
from modules.filters import apply_filters
from modules.correlation import show_correlation
from modules.outliers import show_outliers
from modules.quality import show_quality
from modules.insights import generate_insights

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

menu = create_sidebar()

st.title(APP_NAME)

arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["csv", "xlsx", "json"]
)

if arquivo:

    try:
        # Carrega o arquivo
        df = DataLoader.load(arquivo)

        # Aplica filtros
        df = apply_filters(df)

        # Navegação entre os módulos
        if menu == "Dashboard":
            show_dashboard(df)

        elif menu == "Estatísticas":
            show_statistics(df)

        elif menu == "Gráficos":
            show_graphics(df)

        elif menu == "Correlação":
            show_correlation(df)

        elif menu == "Outliers":
            show_outliers(df)

        elif menu == "Qualidade":
            show_quality(df)

        elif menu == "Insights":
            generate_insights(df)

        else:
            st.info(f"O módulo '{menu}' será implementado nas próximas etapas.")

    except Exception as erro:
        st.error(f"Erro ao carregar o arquivo: {erro}")

else:
    st.info("📁 Faça o upload de um arquivo CSV, Excel ou JSON para começar.")
