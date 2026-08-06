"""Security utility tests."""

import pytest

from src.core.security import (
    sanitize_column_name,
    validate_file_extension,
    validate_file_size,
    RateLimiter,
)


def test_sanitize_column_name():
    assert sanitize_column_name("Normal Column") == "normal_column"
    assert sanitize_column_name("Special!@#Chars") == "special_chars"
    assert sanitize_column_name("123Start") == "col_123start"


def test_validate_file_extension():
    assert validate_file_extension("data.csv") == "csv"
    assert validate_file_extension("data.xlsx") == "xlsx"
    
    with pytest.raises(Exception):
        validate_file_extension("data.exe")


def test_rate_limiter():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    assert limiter.is_allowed("test_key") is True
    assert limiter.is_allowed("test_key") is True
    assert limiter.is_allowed("test_key") is False
