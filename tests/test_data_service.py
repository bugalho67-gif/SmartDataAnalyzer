"""Data service tests."""

from src.application.services.data_service import DataService


def test_generate_quality_report(sample_dataset):
    service = DataService()
    report = service._generate_quality_report(sample_dataset.data)

    assert report.total_rows == 100
    assert report.total_columns == 5
    assert len(report.column_profiles) == 5


def test_get_dataset_summary(sample_dataset):
    service = DataService()
    summary = service.get_dataset_summary(sample_dataset)

    assert summary["name"] == "test.csv"
    assert summary["shape"] == [100, 5]
    assert len(summary["columns"]) == 5
