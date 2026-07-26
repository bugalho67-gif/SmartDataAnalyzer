from modules.dashboard import show_dashboard
from modules.statistics import show_statistics
from modules.graphics import show_graphics
from modules.correlation import show_correlation
from modules.outliers import show_outliers
from modules.quality import show_quality
from modules.insights import generate_insights
from modules.export import show_export


PAGES = {
    "Dashboard": show_dashboard,
    "Estatísticas": show_statistics,
    "Gráficos": show_graphics,
    "Correlação": show_correlation,
    "Outliers": show_outliers,
    "Qualidade": show_quality,
    "Insights": generate_insights,
    "Exportar": show_export,
}
