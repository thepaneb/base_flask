"""Modelo do módulo visits (exemplo de persistência com SQLAlchemy)."""

from datetime import UTC, datetime

from app.extensions import db


class Visit(db.Model):
    """Uma visita registrada via POST /visits."""

    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
