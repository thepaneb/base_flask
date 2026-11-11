"""Módulo visits: exemplo completo `routes > service > repository` com banco."""

from . import models  # noqa: F401 (registra o model no db)
from .routes import bp

__all__ = ["bp"]
