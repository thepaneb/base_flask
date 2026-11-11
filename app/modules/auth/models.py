"""Modelo do módulo auth."""

from datetime import UTC, datetime

from app.extensions import db


class User(db.Model):
    """Usuário para autenticação JWT."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
