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
# Inclui o X-Request-Id da resposta (definido pelo app em after_request).
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" req_id=%({X-Request-Id}o)s'
)
