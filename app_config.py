from pathlib import Path
import os

from dotenv import load_dotenv


# Carrega variáveis do .env

load_dotenv()


# =========================
# ROOT
# =========================

BASE_DIR = Path(__file__).resolve().parent



# =========================
# APPLICATION
# =========================

APP_NAME = os.getenv(
    "APP_NAME",
    "SmartDataAnalyzer"
)


APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)


ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)


DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"



# =========================
# DATABASE
# =========================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///smartdata.db"
)



# =========================
# AI CONFIGURATION
# =========================

AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "local"
)


AI_MODEL = os.getenv(
    "AI_MODEL",
    ""
)


AI_TEMPERATURE = float(
    os.getenv(
        "AI_TEMPERATURE",
        "0.2"
    )
)



# =========================
# SECURITY
# =========================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-key"
)


SESSION_TIMEOUT = int(
    os.getenv(
        "SESSION_TIMEOUT",
        "3600"
    )
)



# =========================
# UPLOAD
# =========================

MAX_UPLOAD_SIZE_MB = int(
    os.getenv(
        "MAX_UPLOAD_SIZE_MB",
        "100"
    )
)


UPLOAD_FOLDER = BASE_DIR / os.getenv(
    "UPLOAD_FOLDER",
    "uploads"
)


UPLOAD_FOLDER.mkdir(
    exist_ok=True
)



# =========================
# CACHE
# =========================

CACHE_TIMEOUT = int(
    os.getenv(
        "CACHE_TIMEOUT",
        "3600"
    )
)



# =========================
# LOGGING
# =========================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)


LOG_FOLDER = BASE_DIR / os.getenv(
    "LOG_FOLDER",
    "logs"
)


LOG_FOLDER.mkdir(
    exist_ok=True
)



# =========================
# FILE SUPPORT
# =========================

SUPPORTED_FILES = [

    "csv",

    "xlsx",

    "json"

]


# =========================
# SYSTEM LIMITS
# =========================

MAX_PREVIEW_ROWS = 1000


MAX_AI_CONTEXT_ROWS = 50


DEFAULT_ENCODING = "utf-8"
