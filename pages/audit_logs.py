"""Página administrativa de logs de auditoria."""

import streamlit as st

from security.audit import AuditLogger
from security.auth import AuthService
from security.rbac import Role


auth_service = AuthService()
auth_service.require_role(Role.ADMIN)

st.title("Logs de Auditoria")
st.dataframe(AuditLogger().list_events(limit=200), use_container_width=True)
