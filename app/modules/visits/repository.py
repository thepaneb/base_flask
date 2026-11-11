"""Acesso aos dados do módulo visits (único lugar que toca o banco)."""

from app.extensions import db

from .models import Visit


class VisitRepository:
    """Persistência de visitas."""

    def add(self, name):
        """Cria e retorna uma visita."""
        visit = Visit(name=name)
        db.session.add(visit)
        db.session.commit()
        return visit

    def get(self, visit_id):
        """Retorna uma visita pelo id (None se não existir)."""
        return db.session.get(Visit, visit_id)

    def delete(self, visit):
        """Remove uma visita."""
        db.session.delete(visit)
        db.session.commit()

    def list(self, limit, offset):
        """Retorna uma página de visitas, mais recentes primeiro."""
        return Visit.query.order_by(Visit.id.desc()).limit(limit).offset(offset).all()

    def count(self):
        """Total de visitas."""
        return Visit.query.count()
