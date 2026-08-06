"""Analytics service tests."""

from src.application.services.analytics_service import AnalyticsService
from src.domain.enums.ml_enums import OutlierMethod


def test_descriptive_statistics(sample_dataset):
    service = AnalyticsService()
    stats = service.get_descriptive_statistics(sample_dataset)
    
    assert "value" in stats
    assert "score" in stats
    assert stats["value"]["count"] == 100


def test_correlation_matrix(sample_dataset):
    service = AnalyticsService()
    corr = service.get_correlation_matrix(sample_dataset)
    
    assert corr is not None
    assert corr.shape == (2, 2)  # value and score are numeric


def test_outlier_detection(sample_dataset):
    service = AnalyticsService()
    outliers = service.detect_outliers(
        sample_dataset,
        method=OutlierMethod.IQR,
    )
    
    assert "value" in outliers or "_summary" in outliers
