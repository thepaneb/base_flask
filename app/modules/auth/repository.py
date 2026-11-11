"""Acesso aos dados do módulo auth."""

from app.extensions import cache, db

from .models import User

BLOCKLIST_PREFIX = "jwt:blocked:"


class TokenBlocklist:
    """JTIs revogados (logout + rotação de refresh). TTL = vida restante do token."""

    @staticmethod
    def _key(jti):
        return f"{BLOCKLIST_PREFIX}{jti}"

    @classmethod
    def add(cls, jti, ttl_seconds):
        """Revoga um token até expirar."""
        cache.set(cls._key(jti), True, timeout=int(ttl_seconds))

    @classmethod
    def contains(cls, jti):
        """Verifica se um token foi revogado."""
        return bool(cache.get(cls._key(jti)))


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
