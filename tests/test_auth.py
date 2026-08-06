"""Authentication service tests."""

import pytest

from src.application.services.auth_service import AuthService
from src.domain.entities.user import UserRole


@pytest.fixture
def auth_service():
    return AuthService()


def test_authenticate_success(auth_service):
    session = auth_service.authenticate("admin@smartdataanalyzer.dev", "admin123")
    assert session is not None
    assert session.user_id == "usr_admin_001"


def test_authenticate_failure(auth_service):
    session = auth_service.authenticate("admin@smartdataanalyzer.dev", "wrong")
    assert session is None


def test_authenticate_unknown_user(auth_service):
    session = auth_service.authenticate("unknown@test.com", "password")
    assert session is None


def test_validate_session(auth_service):
    session = auth_service.authenticate("analyst@smartdataanalyzer.dev", "analyst123")
    user = auth_service.validate_session(session.token)
    assert user is not None
    assert user.role == UserRole.ANALYST


def test_invalid_session(auth_service):
    user = auth_service.validate_session("invalid_token")
    assert user is None


def test_check_permission(auth_service):
    session = auth_service.authenticate("viewer@smartdataanalyzer.dev", "viewer123")
    assert auth_service.check_permission(session.token, UserRole.VIEWER) is True
    assert auth_service.check_permission(session.token, UserRole.ADMIN) is False


def test_invalidate_session(auth_service):
    session = auth_service.authenticate("admin@smartdataanalyzer.dev", "admin123")
    auth_service.invalidate_session(session.token)
    user = auth_service.validate_session(session.token)
    assert user is None
