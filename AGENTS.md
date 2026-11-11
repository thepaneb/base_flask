# AGENTS.md — instruções para agentes neste repositório

## Stack
- Python `3.15.2` (pin em `.python-version`, `requires-python = ">=3.15"` em `pyproject.toml`).
- Flask `3.1.3` com blueprints. Timezone padrão `America/Sao_Paulo` via `zoneinfo` + pacote `tzdata`.
- Gerenciador de dependências: **uv**. Nunca use `pip install` direto; use `uv sync` / `uv add` / `uv run`.
- Dev Container: `mcr.microsoft.com/devcontainers/python:3.15-trixie` + feature `uv`, `postCreateCommand` = `bash dev/dependencies.sh` (`uv sync --frozen`).

## Estrutura
- `app/__init__.py`: cria `app = Flask(__name__)` e registra blueprints. Não coloque lógica de rota aqui.
- `app/modules/<nome>/__init__.py`: cada módulo expõe `bp = Blueprint("<nome>", __name__)` e registra rotas com `@bp.get(...)`.
- `app/modules/status/`: health-check em `GET /status` (checa dependência externa via `requests`).
- `app/modules/hello_world/`: exemplo em `GET /`, `/hello-world`, `/hello_world`.
- `pyproject.toml` + `uv.lock`: única fonte de dependências. Não recrie `requirements.txt`.
- `dev/dependencies.sh`: apenas `uv sync --frozen`.

## Comandos
- Instalar: `uv sync` (com dev: `uv sync --group dev`).
- Rodar: `uv run flask --app app run --host 127.0.0.1 --port 40000` ou `uv run python -m flask --app app run`.
- Teste rápido de rotas: `uv run python -c "import app; c=app.app.test_client(); print(c.get('/status').get_json())"`.
- Auditoria: `uv run --group dev pip-audit --desc`.
- Atualizar deps: `uv lock --upgrade` e depois `uv sync`. Commite `pyproject.toml` + `uv.lock` juntos.

## Convenções
- Respostas JSON via `flask.jsonify`; timestamps ISO 8601 com `ZoneInfo("America/Sao_Paulo")`.
- Chamadas HTTP externas: só `https://`, sempre com `timeout=(5, 5)` e `try/except requests.RequestException` retornando 502/503, nunca estourar 500 sem tratamento.
- Novo módulo: criar `app/modules/<nome>/__init__.py` com `bp`, importar e registrar em `app/__init__.py`, sem dependência circular (módulos não importam `app`; compartilhe helpers por import local ou novo módulo).
- Não commite `.venv/`, `__pycache__/`, `*.pyc` (já no `.gitignore`).
- Debug (`FLASK_DEBUG=1`, launch.json) só local; nunca force `debug=True` no código.
