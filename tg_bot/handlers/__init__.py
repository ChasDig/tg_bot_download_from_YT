from .admin.admins_handler import register_admin_base
from .users.user_base_handlers import register_user_base

__all__ = [
    "register_user_base",
    "register_admin_base",
]
