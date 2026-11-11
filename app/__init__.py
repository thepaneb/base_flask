"""Aplicação Flask base: factory + OpenAPI + registro de blueprints e erros."""

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from app.modules.admin import bp as admin_bp
from app.modules.auth import bp as auth_bp
from app.modules.hello_world import bp as hello_world_bp
from app.modules.status import bp as status_bp
from app.modules.visits import bp as visits_bp

from .cli import seed_command
from .config import get_config
from .errors import register_error_handlers
from .extensions import cache, db, jwt, limiter, migrate
from .logging_conf import configure_logging
from .observability import bp as metrics_bp
from .observability import init_observability


def create_app(config_object=None):
    """Cria e configura o app (permite config por ambiente e testes isolados)."""
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())
    configure_logging(app)
    origins = app.config["CORS_ORIGINS"]
    CORS(app, origins=origins.split(",") if origins != "*" else "*")
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    app.cli.add_command(seed_command)
    prefix = app.config["API_PREFIX"]
    api = Api(app)
    api.register_blueprint(hello_world_bp, url_prefix=prefix)
    api.register_blueprint(status_bp, url_prefix=prefix)
    api.register_blueprint(visits_bp, url_prefix=f"{prefix}/visits")
    api.register_blueprint(auth_bp, url_prefix=f"{prefix}/auth")
    api.register_blueprint(admin_bp, url_prefix=f"{prefix}/admin")
    init_observability(app)
    app.register_blueprint(metrics_bp)  # texto puro: fora do smorest de propósito
    register_error_handlers(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run()
