"""Configuração da aplicação (via variáveis de ambiente).

APP_ENV seleciona o perfil: development (padrão), testing ou production.
APP_TIMEZONE define o fuso padrão (default America/Sao_Paulo).
DATABASE_URL define o banco (default SQLite local).
"""

import os

from sqlalchemy.pool import StaticPool


class Config:
    """Base comum."""

    TIMEZONE = os.getenv("APP_TIMEZONE", "America/Sao_Paulo")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///base_flask.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Documentação OpenAPI (flask-smorest)
    API_TITLE = "base-flask"
    API_VERSION = "0.1.0"
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_JSON_PATH = "openapi.json"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js"


class DevelopmentConfig(Config):
    """Local / devcontainer."""

    DEBUG = True


class TestingConfig(Config):
    """Pytest: banco em memória, isolado por app."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }


class ProductionConfig(Config):
    """Produção (Docker/gunicorn)."""

    DEBUG = False


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name=None):
    """Resolve a classe de config pelo nome (default: $APP_ENV)."""
    return configs.get((name or os.getenv("APP_ENV", "development")).lower(), Config)
