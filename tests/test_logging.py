"""Testes do logging estruturado (sem app, sem I/O)."""

import json
import logging

from app.logging_conf import JsonFormatter


def _record(msg):
    return logging.LogRecord("test", logging.INFO, __file__, 10, msg, None, None)


def test_formatter_emits_json_with_expected_keys():
    out = json.loads(JsonFormatter().format(_record("hello")))
    assert out["level"] == "INFO"
    assert out["message"] == "hello"
    assert "ts" in out and "logger" in out


def test_formatter_merges_dict_messages():
    out = json.loads(JsonFormatter().format(_record({"method": "GET", "status": 200})))
    assert out["method"] == "GET"
    assert out["status"] == 200
    assert "message" not in out
