# Фильтры - условия по которым подаются обработчику
from .admin import AdminFilter
from .users.private_chat import IsPrivate

__all__ = [
    'AdminFilter',
    'IsPrivate',
]
