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
        query = Visit.query
        if name and name.strip():
            query = query.filter(Visit.name.ilike(f"%{name.strip()}%"))
        sorting = Visit.id.asc() if order == "asc" else Visit.id.desc()
        return query.order_by(sorting).limit(limit).offset(offset).all()

    def count(self, name=None):
        """Total de visitas (respeitando o filtro, se houver)."""
        query = Visit.query
        if name and name.strip():
            query = query.filter(Visit.name.ilike(f"%{name.strip()}%"))
        return query.count()
