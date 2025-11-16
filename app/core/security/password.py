import base64
import secrets

import bcrypt

from app.core.config import lprint, PASSWORD_HASH_ROUNDS, PASSWORD_SALT_SIZE


class PasswordUtils:
    """Утилита для хеширования и проверки паролей"""

    @classmethod
    def generate_salt(cls, size: int = None) -> bytes:
        """Генерирует криптографически стойкую соль

        Args:
            size: Размер соли в байтах (по умолчанию SALT_SIZE)

        Returns:
            bytes: Сгенерированная соль
        """
        size = size or int(PASSWORD_SALT_SIZE)
        return secrets.token_bytes(size)

    @classmethod
    def hash_password(cls,
                      password: str, rounds: int = None
                      ) -> tuple[str, str]:
        """Хеширует пароль с использованием bcrypt и возвращает хеш и соль

        Args:
            password: Пароль для хеширования
            rounds: Количество раундов хеширования (сложность)

        Returns:
            Tuple[str, str]: Кортеж (хеш пароля в виде строки,
            соль в виде строки в base64)
        """
        try:
            rounds = rounds or int(PASSWORD_HASH_ROUNDS)

            salt = cls.generate_salt()
            salt_str = base64.b64encode(salt).decode('utf-8')

            password_bytes = password.encode('utf-8')
            bcrypt_salt = bcrypt.gensalt(rounds=rounds, prefix=b'2b')
            password_hash = bcrypt.hashpw(password_bytes, bcrypt_salt)

            hash_str = password_hash.decode('utf-8')

            return hash_str, salt_str

        except Exception as e:
            lprint.error(f"Error hashing password: {e}")
            raise

    @classmethod
    def verify_password(cls, password: str, stored_hash: str) -> bool:
        """Проверяет соответствие пароля хешу

        Args:
            password: Пароль для проверки
            stored_hash: Сохраненный хеш пароля

        Returns:
            bool: True если пароль соответствует хешу, иначе False
        """
        try:
            password_bytes = password.encode('utf-8')
            stored_hash_bytes = stored_hash.encode('utf-8') if isinstance(
                stored_hash, str
            ) else stored_hash

            return bcrypt.checkpw(password_bytes, stored_hash_bytes)

        except Exception as e:
            lprint.error(f"Error verifying password: {e}")
            return False
