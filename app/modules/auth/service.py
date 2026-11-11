"""Regra de negócio do módulo auth (pura: sem `flask`, sem banco direto)."""

from werkzeug.security import check_password_hash, generate_password_hash

from .repository import UserRepository

_repository = UserRepository()


def register(username, password, repository=None):
    """Cria um usuário. Levanta ValueError se o username já existe ou é vazio."""
    repo = repository or _repository
    clean = (username or "").strip()
    if not clean or not password:
        raise ValueError("username e password são obrigatórios")
    if repo.get_by_username(clean) is not None:
        raise ValueError("username já está em uso")
    return repo.add(clean, generate_password_hash(password))


def authenticate(username, password, repository=None):
    """Retorna o usuário se as credenciais conferem, senão None."""
    repo = repository or _repository
    user = repo.get_by_username((username or "").strip())
    if user is None or not check_password_hash(user.password_hash, password or ""):
        return None
    return user
