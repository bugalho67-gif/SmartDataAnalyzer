from machine_learning.dashboard import show_dashboard
from machine_learning.statistics import show_statistics
from machine_learning.graphics import show_graphics
from machine_learning.correlation import show_correlation
from machine_learning.outliers import show_outliers
from machine_learning.quality import show_quality
from machine_learning.insights import generate_insights
from machine_learning.export import show_export
from machine_learning.chat import show_chat
from machine_learning.smart_dashboard import suggest_chart
from database.database_manager import connect_database


PAGES = {
    "Dashboard": show_dashboard,
    "Dashboard Inteligente": suggest_chart,
    "Estatísticas": show_statistics,
    "Gráficos": show_graphics,
    "Correlação": show_correlation,
    "Outliers": show_outliers,
    "Qualidade": show_quality,
    "Insights": generate_insights,
    "Assistente IA": show_chat,
    "Exportar": show_export,
    "Banco de Dados": connect_database,
}
