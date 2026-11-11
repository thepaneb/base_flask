"""Módulo auth: exemplo `routes > service > repository` com JWT."""

from . import models  # noqa: F401 (registra o model no db)
from .routes import bp

__all__ = ["bp"]
