"""Aplicação Flask base: factory + OpenAPI + registro de blueprints e erros."""

from flask import Flask
from flask_smorest import Api

from app.modules.hello_world import bp as hello_world_bp
from app.modules.status import bp as status_bp
from app.modules.visits import bp as visits_bp

from .config import get_config
from .errors import register_error_handlers
from .extensions import db


def create_app(config_object=None):
    """Cria e configura o app (permite config por ambiente e testes isolados)."""
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())
    db.init_app(app)
    api = Api(app)
    api.register_blueprint(hello_world_bp)
    api.register_blueprint(status_bp)
    api.register_blueprint(visits_bp)
    register_error_handlers(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()


if __name__ == "__main__":
    app.run()
