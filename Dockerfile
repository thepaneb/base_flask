# Exemplo de imagem de produção da aplicação Flask.
# Build: docker build -t base-flask .
FROM python:3.15-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production \
    PATH="/srv/app/.venv/bin:$PATH"

WORKDIR /srv/app

# uv (só para instalar as deps travadas no uv.lock)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock .python-version ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

COPY app/ ./app/

EXPOSE 40000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:40000/status').status == 200 else 1)"

# "app:create_app()" chama a factory e devolve o WSGI app
CMD ["gunicorn", "--bind", "0.0.0.0:40000", "--workers", "2", "app:create_app()"]
