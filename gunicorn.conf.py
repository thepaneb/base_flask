"""Configuração do gunicorn (produção). Ajuste via variáveis de ambiente."""

import multiprocessing
import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:40000")
workers = int(os.getenv("WEB_CONCURRENCY", (multiprocessing.cpu_count() * 2) + 1))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
