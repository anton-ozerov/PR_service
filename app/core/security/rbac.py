from fastapi import HTTPException, status
from functools import wraps

from app.core.config import lprint
from app.enums import UserRoleEnum


class PermissionChecker:
    """Декоратор для проверки ролей пользователя"""

    def __init__(self, roles: list[UserRoleEnum]):
        self.roles = roles  # Список разрешённых ролей

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Получаем текущего пользователя
            user_db = kwargs.get("current_user")
            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Требуется аутентификация"
                )

            user_role = getattr(user_db, "role", None)
            lprint.debug(f"PermissionChecker: user_role = {user_role}")

            user_role_value = user_role.value if isinstance(
                user_role,
                UserRoleEnum
            ) else user_role

            allowed_roles_values = [role.value if isinstance(
                role,
                UserRoleEnum
            ) else role for role in self.roles]

            if user_role_value not in allowed_roles_values:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Недостаточно прав для доступа"
                )
            return await func(*args, **kwargs)

        return wrapper
