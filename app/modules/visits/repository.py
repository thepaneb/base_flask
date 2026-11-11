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

    def list(self, limit, offset, name=None, order="desc"):
        """Retorna uma página de visitas (filtro opcional por nome)."""
        return self._query(name, order).limit(limit).offset(offset).all()

    def all(self, name=None, order="desc"):
        """Retorna todas as visitas (para exportação)."""
        return self._query(name, order).all()

    def count(self, name=None):
        """Total de visitas (respeitando o filtro, se houver)."""
        return self._filtered(name).count()

    @staticmethod
    def _filtered(name):
        query = Visit.query
        if name and name.strip():
            query = query.filter(Visit.name.ilike(f"%{name.strip()}%"))
        return query

    @classmethod
    def _query(cls, name, order):
        return cls._filtered(name).order_by(Visit.id.asc() if order == "asc" else Visit.id.desc())
