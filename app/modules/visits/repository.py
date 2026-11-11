"""Acesso aos dados do módulo visits (único lugar que toca o banco)."""

from app.extensions import db

from .models import Visit


class VisitRepository:
    """Persistência de visitas."""

    def add(self, name):
        """Cria e retorna uma visita (commit imediato, exemplo mínimo)."""
        visit = Visit(name=name)
        db.session.add(visit)
        db.session.commit()
        return visit

    def list_all(self):
        """Retorna todas as visitas, mais recentes primeiro."""
        return Visit.query.order_by(Visit.id.desc()).all()
