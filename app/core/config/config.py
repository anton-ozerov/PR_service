import os

from dotenv import load_dotenv


load_dotenv()


# Database configuration
DB_NAME = str(os.getenv("db_name"))
DB_USER_NAME = str(os.getenv("db_user_name"))
DB_PASSWORD = str(os.getenv("db_password"))
DB_HOST = str(os.getenv("db_host"))
DB_PORT = str(os.getenv("db_port", "5432"))
ASYNC_DATABASE_URL = (f"postgresql+asyncpg://"
                      f"{DB_USER_NAME}:{DB_PASSWORD}"
                      f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Logging configuration
LOG_LEVEL = str(os.getenv("LOG_LEVEL", "INFO")).upper()
LOG_FORMAT = str(os.getenv("LOG_FORMAT", "detailed"))
LOG_FILE = str(os.getenv("LOG_FILE", "logs/app.log"))
LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# Security configuration
ADMIN_AUTO_CREATED_PASSWORD = str(os.getenv("ADMIN_AUTO_CREATED_PASSWORD"))
# Password hashing and encryption
PASSWORD_HASH_ROUNDS = str(os.getenv("PASSWORD_HASH_ROUNDS"))
PASSWORD_SALT_SIZE = str(os.getenv("PASSWORD_SALT_SIZE"))
# JWT configuration
SECRET_KEY = str(os.getenv("jwt_auth_key"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv(
    "ACCESS_TOKEN_EXPIRE_MINUTES", "11520")  # 8 days
)
ALGORITHM = str(os.getenv("ALGORITHM", "HS256"))

# Documentation access credentials
DOCS_USERNAME = str(os.getenv("DOCS_USERNAME"))
DOCS_PASSWORD = str(os.getenv("DOCS_PASSWORD"))


COUNT_REVIEWERS_FOR_PR = int(os.getenv("COUNT_REWIEWEERS_FOR_PR", "2"))
