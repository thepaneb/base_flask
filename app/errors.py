"""Handlers de erro em JSON (em vez do HTML padrão do Flask)."""

from .extensions import jwt


def register_error_handlers(app):
    """Registra handlers JSON de erro no app."""

    @app.errorhandler(404)
    def not_found(_exc):
        return {"error": "not found"}, 404

    @app.errorhandler(401)
    def unauthorized(_exc):
        return {"error": "unauthorized"}, 401

    @app.errorhandler(405)
    def method_not_allowed(_exc):
        return {"error": "method not allowed"}, 405

    @app.errorhandler(429)
    def rate_limited(_exc):
        return {"error": "rate limit exceeded"}, 429

    @app.errorhandler(500)
    def internal_error(_exc):
        return {"error": "internal server error"}, 500

    @jwt.unauthorized_loader
    def _jwt_missing(msg):
        return {"error": msg}, 401

    @jwt.invalid_token_loader
    def _jwt_invalid(msg):
        return {"error": msg}, 401

    @jwt.expired_token_loader
    def _jwt_expired(_header, _payload):
        return {"error": "token expirado"}, 401
