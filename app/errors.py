"""Handlers de erro em JSON (em vez do HTML padrão do Flask)."""


def register_error_handlers(app):
    """Registra handlers JSON de erro no app."""

    @app.errorhandler(404)
    def not_found(_exc):
        return {"error": "not found"}, 404

    @app.errorhandler(405)
    def method_not_allowed(_exc):
        return {"error": "method not allowed"}, 405

    @app.errorhandler(500)
    def internal_error(_exc):
        return {"error": "internal server error"}, 500
