"""Logging estruturado em JSON (stdlib, sem deps novas)."""

import json
import logging
from datetime import UTC, datetime

from flask import g, has_request_context

DEFAULT_LEVEL = "INFO"


class JsonFormatter(logging.Formatter):
    """Formata o log como uma linha JSON (com request_id quando houver request)."""

    def format(self, record):
        payload = {
            "ts": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
        }
        if has_request_context():
            payload["request_id"] = g.get("request_id", "-")
        if isinstance(record.msg, dict):
            payload.update(record.msg)
        else:
            payload["message"] = record.getMessage()
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(app):
    """Aplica nível ($LOG_LEVEL) + formato JSON ao logger do app."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    app.logger.handlers = [handler]
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.logger.propagate = False
