from modules.dashboard import show_dashboard
from modules.statistics import show_statistics
from modules.graphics import show_graphics
from modules.correlation import show_correlation
from modules.outliers import show_outliers
from modules.quality import show_quality
from modules.insights import generate_insights
from modules.export import show_export
from modules.ml import regression
from modules.autocharts import auto_chart
from modules.comparison import compare
from modules.executive_dashboard import executive_dashboard
from database.database_manager import connect_database
from modules.smart_dashboard import suggest_chart
from modules.chat import show_chat

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
    "Exportar": show_export,
    "Dashboard Executivo": executive_dashboard,
    "Banco de Dados": connect_database,
    "Dashboard Inteligente": suggest_chart,
    "Assistente IA": show_chat,

}
