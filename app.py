from __future__ import annotations

import streamlit as st

from app_config import APP_NAME, SUPPORTED_FILES
from core.exceptions import show_error
from machine_learning.file_handler import process_uploaded_file
from machine_learning.filters import apply_filters
from machine_learning.page_controller import render_page
from machine_learning.progress import finish_progress, show_progress, update_progress
from machine_learning.search import search_dataframe
from machine_learning.sidebar import create_sidebar
from security.anonymizer import anonymize_dataframe, detect_sensitive_columns
from security.audit import AuditLogger
from security.auth import AuthService, render_user_header
from security.rbac import Role, has_permission
from security.upload import upload_rate_limiter, validate_upload_file


st.set_page_config(page_title=APP_NAME, page_icon="📊", layout="wide")


def render_consent(auth_service: AuthService, user_id: int) -> None:
    """Exibe termo de consentimento LGPD no primeiro acesso."""
    st.warning(
        "Para continuar, aceite o termo de consentimento para processamento "
        "dos dados enviados conforme a LGPD."
    )
    if st.button("Aceito o termo de consentimento"):
        auth_service.accept_terms(user_id)
        st.success("Consentimento registrado.")
        st.rerun()
    st.stop()


def main() -> None:
    """Executa a aplicação Streamlit com autenticação e upload seguro."""
    auth_service = AuthService()
    audit_logger = AuditLogger()
    user = auth_service.current_user()

    if user is None:
        auth_service.require_role(Role.VIEWER)
        return

    render_user_header(auth_service, user)
    if not user.accepted_terms:
        render_consent(auth_service, user.id)

    menu = create_sidebar()
    st.title(APP_NAME)

    if menu == "Banco de Dados":
        if not has_permission(user.role, Role.ADMIN):
            st.error("Apenas administradores podem acessar conexões de banco.")
            st.stop()
        render_page(menu, None)
        st.stop()

    if not has_permission(user.role, Role.ANALYST):
        st.info("Seu perfil permite visualizar dashboards e relatórios compartilhados.")
        st.stop()

    anonymize_sensitive_data = st.checkbox(
        "Anonimizar dados sensíveis automaticamente",
        value=True,
        help="Detecta CPF, CNPJ, e-mail, telefone e RG antes da análise.",
    )
    uploaded_file = st.file_uploader("Selecione um arquivo", type=SUPPORTED_FILES)

    if uploaded_file is None:
        st.info("Faça o upload de um arquivo.")
        st.stop()

    try:
        if not upload_rate_limiter.is_allowed(str(user.id)):
            st.error("Limite de 5 uploads por hora atingido. Tente novamente mais tarde.")
            st.stop()

        validate_upload_file(uploaded_file)
        audit_logger.log_event(
            "upload_validado",
            user_id=user.id,
            metadata={"file_name": uploaded_file.name, "size": uploaded_file.size},
        )

        progress = show_progress()
        df = process_uploaded_file(uploaded_file)

        if anonymize_sensitive_data:
            sensitive_columns = detect_sensitive_columns(df)
            if sensitive_columns:
                df = anonymize_dataframe(df, sensitive_columns)
                st.toast("Colunas sensíveis anonimizadas com segurança.")

        update_progress(progress, 40)
        df = apply_filters(df)
        update_progress(progress, 70)
        df = search_dataframe(df)
        update_progress(progress, 90)
        render_page(menu, df)
        finish_progress(progress)
    except Exception as erro:
        show_error(erro)


main()
