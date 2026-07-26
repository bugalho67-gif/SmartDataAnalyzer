from modules.ml import regression
from modules.autocharts import auto_chart
from modules.comparison import compare

PAGES = {

    "Dashboard": show_dashboard,

    "Estatísticas": show_statistics,

    "Gráficos": show_graphics,

    "Gráfico Inteligente": auto_chart,

    "Correlação": show_correlation,

    "Outliers": show_outliers,

    "Qualidade": show_quality,

    "Insights": generate_insights,

    "Machine Learning": regression,

    "Comparar Arquivos": compare,

    "Exportar": show_export

}
