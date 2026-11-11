# -*- coding: utf-8 -*-
"""Aplicação Flask base com blueprints modulares."""

from flask import Flask

from app.modules.hello_world import bp as hello_world_bp
from app.modules.status import bp as status_bp

app = Flask(__name__)
app.register_blueprint(hello_world_bp)
app.register_blueprint(status_bp)


if __name__ == "__main__":
    app.run()
