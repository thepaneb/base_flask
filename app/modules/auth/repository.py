"""Acesso aos dados do módulo auth."""

from app.extensions import db

from .models import User


class UserRepository:
    """Persistência de usuários."""

    def add(self, username, password_hash):
        """Cria e retorna um usuário."""
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

    def get_by_username(self, username):
        """Retorna um usuário pelo username (None se não existir)."""
        return User.query.filter_by(username=username).first()

    def get_by_id(self, user_id):
        """Retorna um usuário pelo id (None se não existir)."""
        return db.session.get(User, user_id)

    def count(self):
        """Total de usuários."""
        return User.query.count()
