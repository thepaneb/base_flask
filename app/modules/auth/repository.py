"""Acesso aos dados do módulo auth."""

from datetime import UTC, datetime, timedelta

from app.extensions import db

from .models import RevokedToken, User


class TokenBlocklist:
    """JTIs revogados (logout + rotação). Tabela própria: não é cache."""

    @staticmethod
    def add(jti, ttl_seconds):
        """Revoga um token até expirar (idempotente por PK)."""
        expires_at = datetime.now(UTC) + timedelta(seconds=int(ttl_seconds))
        if db.session.get(RevokedToken, jti) is None:
            db.session.add(RevokedToken(jti=jti, expires_at=expires_at))
            db.session.commit()

    @staticmethod
    def contains(jti):
        """Verifica se um token foi revogado (limpa expirados de passagem)."""
        now = datetime.now(UTC)
        expired = RevokedToken.query.filter(RevokedToken.expires_at <= now).all()
        for token in expired:
            db.session.delete(token)
        db.session.commit()
        token = db.session.get(RevokedToken, jti)
        if token is None:
            return False
        stored = (
            token.expires_at if token.expires_at.tzinfo else token.expires_at.replace(tzinfo=UTC)
        )
        return stored > now


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
