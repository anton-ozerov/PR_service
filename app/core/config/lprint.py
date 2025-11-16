import datetime
import inspect

from app.core.config import get_app_logger


class lprint:
    """логгер для приложения"""

    logger = get_app_logger()

    @classmethod
    def _log(cls, level, text, *args):
        """Универсальный метод логирования"""
        moscow_time = (datetime.datetime.now(datetime.timezone.utc)
                       + datetime.timedelta(hours=3))
        time_str = moscow_time.strftime("%Y-%m-%d %H:%M:%S")
        frame = inspect.currentframe().f_back.f_back
        caller = (f"{frame.f_code.co_filename.split('\\')[-1]}"
                  f":{frame.f_code.co_name}")
        message = f"[{time_str}] {caller} - {text}"
        if args:
            message += " " + " ".join(map(str, args))
        getattr(cls.logger, level)(message)

    @classmethod
    def init(cls):
        """Инициализация логгера"""
        cls.logger.info("Script started %s", datetime.datetime.now())

    @classmethod
    def debug(cls, text, *args):
        """Debug уровень"""
        cls._log("debug", text, *args)

    @classmethod
    def info(cls, text, *args):
        """Info уровень"""
        cls._log("info", text, *args)

    @classmethod
    def warning(cls, text, *args):
        """Warning уровень"""
        cls._log("warning", text, *args)

    @classmethod
    def error(cls, text, *args):
        """Error уровень"""
        cls._log("error", text, *args)

    @classmethod
    def critical(cls, text, *args):
        """Critical уровень"""
        cls._log("critical", text, *args)
