# Etapa build: resolve e instala as deps travadas no uv.lock
FROM ghcr.io/astral-sh/uv:python3.15-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /srv/app

COPY pyproject.toml uv.lock .python-version ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Etapa runtime: imagem final enxuta, non-root
FROM python:3.15-slim-trixie AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production \
    DATABASE_URL=sqlite:////data/base_flask.db \
    PATH="/srv/app/.venv/bin:$PATH"

WORKDIR /srv/app

COPY --from=builder /srv/app/.venv /srv/app/.venv
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY entrypoint.sh ./entrypoint.sh
COPY gunicorn.conf.py ./gunicorn.conf.py

RUN useradd --create-home --uid 10000 appuser \
    && mkdir -p /data && chown -R appuser:appuser /srv/app /data
USER appuser

EXPOSE 40000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:40000/v1/live').status == 200 else 1)"

# O entrypoint aplica `flask db upgrade` e chama o CMD (gunicorn).
ENTRYPOINT ["/srv/app/entrypoint.sh"]
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:create_app()"]
