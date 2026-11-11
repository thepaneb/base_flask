# -*- coding: utf-8 -*-
"""Health-check do serviço."""

import hashlib
import platform
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from flask import Blueprint, jsonify

bp = Blueprint("status", __name__)

TIMEOUT = (5, 5)
CHECK_URL = "https://www.google.com.br"


def agora(tz: str = "America/Sao_Paulo") -> datetime:
    """Retorna a data/hora atual com tz oficial BR."""
    return datetime.now(ZoneInfo(tz))


@bp.get("/status")
def status():
    """Retorna saúde da aplicação e de dependência externa."""
    try:
        r = requests.get(url=CHECK_URL, timeout=TIMEOUT)
        dependencia = {
            "url": CHECK_URL,
            "status_code": r.status_code,
            "content_length": len(r.text),
            "content_hash_sha512": hashlib.sha512(r.text.encode()).hexdigest(),
            "ok": r.status_code == 200,
        }
        http_status = 200 if dependencia["ok"] else 502
    except requests.RequestException as exc:
        dependencia = {"url": CHECK_URL, "ok": False, "erro": str(exc)}
        http_status = 503

    return (
        jsonify(
            {
                "status": "ok" if http_status == 200 else "degraded",
                "timestamp": agora().isoformat(),
                "python": platform.python_version(),
                "dependencia": dependencia,
            }
        ),
        http_status,
    )
