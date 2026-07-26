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

    "Dashboard Executivo": executive_dashboard

}
