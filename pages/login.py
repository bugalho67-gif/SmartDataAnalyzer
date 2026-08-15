"""Página dedicada de login."""

from security.auth import AuthService, render_login_form

render_login_form(AuthService())
