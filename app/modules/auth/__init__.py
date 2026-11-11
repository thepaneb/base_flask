"""Módulo auth: exemplo `routes > service > repository` com JWT e rate limit no login."""

from . import models  # noqa: F401 (registra o model no db)
from .routes import bp

__all__ = ["bp"]
