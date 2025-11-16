import logging
import logging.config
from pathlib import Path

from app.core.config import (
    LOG_LEVEL, LOG_FORMAT, LOG_MAX_SIZE,
    LOG_FILE, LOG_BACKUP_COUNT,
)


class LoggingConfig:
    """Класс для настройки логирования"""

    def __init__(self):
        self.log_level = LOG_LEVEL
        self.log_format = LOG_FORMAT
        self.log_file = LOG_FILE
        self.max_file_size = LOG_MAX_SIZE
        self.backup_count = LOG_BACKUP_COUNT

        log_dir = Path(self.log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

    def get_logging_config(self) -> dict:
        """Возвращает конфигурацию логирования"""

        # Форматы логов
        formats = {
            "simple": "%(levelname)s - %(message)s",
            "detailed": "%(name)s - %(levelname)s - %(message)s",
            "json": '{"timestamp": "%(asctime)s", '
                    '"logger": "%(name)s", '
                    '"level": "%(levelname)s", '
                    '"function": "%(funcName)s", '
                    '"line": %(lineno)d, '
                    '"message": "%(message)s"}'
        }

        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": formats["simple"]
                },
                "detailed": {
                    "format": formats["detailed"],
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
                "json": {
                    "format": formats["json"],
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.log_level,
                    "formatter": self.log_format,
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": self.log_level,
                    "formatter": self.log_format,
                    "filename": self.log_file,
                    "maxBytes": self.max_file_size,
                    "backupCount": self.backup_count,
                    "encoding": "utf-8"
                },
                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "ERROR",
                    "formatter": self.log_format,
                    "filename": str(Path(self.log_file).parent / "error.log"),
                    "maxBytes": self.max_file_size,
                    "backupCount": self.backup_count,
                    "encoding": "utf-8"
                }
            },
            "loggers": {
                "": {
                    "level": self.log_level,
                    "handlers": ["console", "file", "error_file"],
                    "propagate": False
                },
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                    "propagate": False
                },
                "uvicorn.error": {
                    "level": "INFO",
                    "handlers": ["console", "file", "error_file"],
                    "propagate": False
                },
                "uvicorn.access": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                    "propagate": False
                },
                "sqlalchemy.engine": {
                    "level": "WARNING",
                    "handlers": ["file"],
                    "propagate": False
                },
                "sqlalchemy.pool": {
                    "level": "WARNING",
                    "handlers": ["file"],
                    "propagate": False
                },
                "watchfiles": {
                    "level": "WARNING",
                    "handlers": ["file"],
                    "propagate": False
                }
            }
        }

        return config

    def setup_logging(self):
        """Настраивает логирование"""
        config = self.get_logging_config()
        logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Получить логгер с указанным именем"""
    return logging.getLogger(name)


def setup_logging():
    """Инициализация логирования"""
    LoggingConfig().setup_logging()


def get_app_logger() -> logging.Logger:
    """Логгер для приложения"""
    return get_logger("APP_LOGGER")
