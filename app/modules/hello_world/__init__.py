# -*- coding: utf-8 -*-
"""Exemplo mínimo de módulo."""

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Blueprint, jsonify

bp = Blueprint("hello_world", __name__)


@bp.get("/")
@bp.get("/hello-world")
@bp.get("/hello_world")
def hello():
    """Retorna mensagem de exemplo."""
    return jsonify(
        {
            "message": "hello world",
            "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
        }
    )
