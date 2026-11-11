# base_flask

**A ready-to-use Flask workspace on VS Code Dev Containers.** Python 3.15, blueprints, dependencies managed with `uv`, debugging preconfigured, and nothing to install on your machine besides Docker.

<p>
  <a href="https://github.com/new?template_name=base_flask&template_owner=thepaneb"><img alt="Use this template" src="https://img.shields.io/badge/Use%20this%20template-2ea44f?logo=github&logoColor=white"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white">
  <img alt="uv" src="https://img.shields.io/badge/uv-managed-5C5CFF">
  <img alt="Dev Containers" src="https://img.shields.io/badge/VS%20Code-Dev%20Containers-007ACC?logo=visualstudiocode&logoColor=white">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue">
</p>

## Why use this template

- **Zero local setup** — Python and the dependencies live inside the container.
- **Python 3.15** on Debian 13 (`trixie`) with the extensions I use daily already installed (Pylance, Ruff, Black, pylint, pytest, debugpy).
- **Blueprint structure** — routes live in `app/modules/<name>/`, ready to grow without refactoring.
- **uv everywhere** — `pyproject.toml` + `uv.lock`, reproducible installs via `uv sync --frozen`.
- **Debug ready** — press `F5` and the app starts on port `40000` with breakpoints enabled.
- **Time zone set** to `America/Sao_Paulo` for reproducible dates in logs and reports.

## Quick start

1. Click **Use this template** → **Create a new repository**.
2. Clone your new repository and open the folder in VS Code.
3. Accept **Reopen in Container** when prompted (or run `Dev Containers: Reopen in Container` from the Command Palette).
4. Press **F5** and open http://127.0.0.1:40000.

Requirements: Docker running, VS Code, and the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.

To use it without creating a repository:

```sh
git clone https://github.com/thepaneb/base_flask.git
code base_flask
```

## What's inside

```text
.
├── .devcontainer/devcontainer.json   # Python 3.15-trixie image, uv feature, port 40000
├── .vscode/
│   ├── extensions.json               # recommends the Dev Containers extension
│   └── launch.json                   # "Flask Debugger" (debugpy)
├── app/
│   ├── __init__.py                   # creates the Flask app, registers blueprints
│   └── modules/
│       ├── hello_world/__init__.py   # GET /, /hello-world, /hello_world
│       └── status/__init__.py        # GET /status (health-check)
├── dev/dependencies.sh               # uv sync --frozen (container postCreate)
├── pyproject.toml / uv.lock          # dependencies (Flask, requests, tzdata)
├── .python-version                   # 3.15.2
└── AGENTS.md                         # guide for coding agents
```

## Endpoints

| Route              | Response                                                                          |
| ------------------ | --------------------------------------------------------------------------------- |
| `GET /`            | `{"message": "hello world", "timestamp": ...}`                                    |
| `GET /hello-world` | same (hyphen and underscore aliases)                                              |
| `GET /status`      | `{"status": "ok"/"degraded", "timestamp", "python", "dependencia": {...}}` (200 / 502 / 503) |

## Run and debug

The container runs `bash dev/dependencies.sh` on creation, so the app is ready as soon as it opens.

| Action | How |
| --- | --- |
| Start with the debugger | `F5` → **Flask Debugger** |
| URL | http://127.0.0.1:40000 |
| Reinstall dependencies | `uv sync --group dev` (or `bash dev/dependencies.sh`) |
| Run without VS Code | `uv run flask --app app run --host 127.0.0.1 --port 40000` |

The launch profile uses `--no-debugger --no-reload` on purpose: Flask's own debugger and reloader conflict with debugpy breakpoints.

Quick check without starting a server:

```bash
uv run python -c "import app; c=app.app.test_client(); print(c.get('/').get_json()); print(c.get('/status').status_code)"
```

## Add a new module

1. Create `app/modules/<name>/__init__.py` exposing `bp = Blueprint("<name>", __name__)` with its routes.
2. Register it in `app/__init__.py`: `from app.modules.<name> import bp as <name>_bp` + `app.register_blueprint(<name>_bp)`.
3. Don't import `app` inside modules (avoids cycles). Answer with `jsonify`, timestamps with `ZoneInfo("America/Sao_Paulo")`, external HTTP only over `https://` with `timeout=(5, 5)` and `try/except requests.RequestException`.

## Customize

- **Dependencies:** edit `pyproject.toml`, run `uv lock && uv sync --group dev`, and commit both files.
- **Port:** update `forwardPorts`/`portsAttributes` in `.devcontainer/devcontainer.json` and `--port` in `.vscode/launch.json`.
- **Security audit:** `uv run --group dev pip-audit --desc`.

Notes: `tzdata` is required on Windows for `zoneinfo`; `FLASK_DEBUG=1` (launch.json) is for local use only.

## License

MIT — see [LICENSE](LICENSE).
