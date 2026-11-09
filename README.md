# base_flask

**A ready-to-use Flask workspace on VS Code Dev Containers.** Python 3.14, debugging preconfigured, and nothing to install on your machine besides Docker.

<p>
  <a href="https://github.com/new?template_name=base_flask&template_owner=thepaneb"><img alt="Use this template" src="https://img.shields.io/badge/Use%20this%20template-2ea44f?logo=github&logoColor=white"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white">
  <img alt="Dev Containers" src="https://img.shields.io/badge/VS%20Code-Dev%20Containers-007ACC?logo=visualstudiocode&logoColor=white">
</p>

## Why use this template

- **Zero local setup** — Python, pip and the dependencies live inside the container.
- **Python 3.14** with the extensions I use daily already installed (Pylance, Ruff, Black, pylint, pytest, debugpy).
- **Debug ready** — press `F5` and the app starts on port `40000` with breakpoints enabled.
- **Time zone set** to `America/Sao_Paulo` for reproducible dates in logs and reports.
- **Concurrency examples** included to compare four I/O approaches on the same workload.

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
├── .devcontainer/devcontainer.json   # Python 3.14 image, extensions, port 40000
├── .vscode/
│   ├── extensions.json               # recommends the Dev Containers extension
│   └── launch.json                   # "Flask Debugger" (debugpy)
├── app/
│   ├── __init__.py                   # Flask app and the sample route
│   ├── requirements.txt              # Flask + requests
│   ├── sync.py                       # sequential I/O
│   ├── thread.py                     # threaded I/O
│   ├── httpx.py                      # async I/O with httpx
│   └── aiohttp.py                    # async I/O with aiohttp
├── dev/dependencies.sh               # upgrades pip and installs requirements
└── base_flask.code-workspace
```

## Run and debug

The container runs `bash dev/dependencies.sh` on creation, so the app is ready as soon as it opens.

| Action | How |
| --- | --- |
| Start with the debugger | `F5` → **Flask Debugger** |
| URL | http://127.0.0.1:40000 |
| Reinstall/upgrade dependencies | `bash dev/dependencies.sh` |

The launch profile uses `--no-debugger --no-reload` on purpose: Flask's own debugger and reloader conflict with debugpy breakpoints.

## The sample code

- `app/__init__.py` — a minimal Flask app. `GET /` requests `google.com.br` and returns the status code, body length and a SHA-512 hash, which makes it a quick check that outbound networking works from inside the container.
- `sync.py`, `thread.py`, `httpx.py` and `aiohttp.py` — the same download workload with sequential, threaded, `httpx` async and `aiohttp` async implementations, useful to compare execution times.
- `requirements.txt` lists only `Flask` and `requests`. To run the async examples, add `httpx` and `aiohttp` and rerun `dev/dependencies.sh`.

## Customize

- **Dependencies:** edit `app/requirements.txt` and run `bash dev/dependencies.sh`.
- **Port:** update `forwardPorts`/`portsAttributes` in `.devcontainer/devcontainer.json` and `--port` in `.vscode/launch.json`.
- **Packages:** create folders under `app/` or add a blueprint; the template keeps no opinionated structure.

## License

This template does not ship a license file. Add one if you plan to distribute derived work.
