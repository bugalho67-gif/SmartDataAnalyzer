"""Exceções da camada de aplicação."""


class ApplicationError(Exception):
    """Erro conhecido que pode ser exibido de forma amigável."""

    def __init__(self, message: str, details: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class FileUploadError(ApplicationError):
    """Erro de validação ou leitura no upload."""


class MLTrainingError(ApplicationError):
    """Erro durante treinamento ou explicação de modelos."""
