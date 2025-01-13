from tinylogging.formatter import Formatter
from tinylogging.level import Level
from tinylogging.record import Record
from tinylogging.sync.handlers import (
    BaseHandler,
    FileHandler,
    LoggingAdapterHandler,
    StreamHandler,
    TelegramHandler,
)

__all__ = [
    "Logger",
    "Formatter",
    "BaseHandler",
    "FileHandler",
    "LoggingAdapterHandler",
    "TelegramHandler",
]


class Logger:
    def __init__(
        self,
        name: str,
        level: Level = Level.NOTSET,
        formatter: Formatter = Formatter(),
        handlers: set[BaseHandler] = set(),
    ) -> None:
        self.name = name
        self.level = level
        self.formatter = formatter
        self.is_disabled = False
        self.handlers = handlers or {StreamHandler(self.formatter, self.level)}

    def log(self, message: str, level: Level):
        if self.level > level or self.is_disabled:
            return

        record = Record(message, level, self.name)

        for handler in self.handlers:
            handler.handle(record)

    def trace(self, message: str):
        self.log(message, level=Level.TRACE)

    def debug(self, message: str):
        self.log(message, level=Level.DEBUG)

    def info(self, message: str):
        self.log(message, level=Level.INFO)

    def notice(self, message: str):
        self.log(message, level=Level.NOTICE)

    def warning(self, message: str):
        self.log(message, level=Level.WARNING)

    def error(self, message: str):
        self.log(message, level=Level.ERROR)

    def critical(self, message: str):
        self.log(message, level=Level.CRITICAL)

    def enable(self):
        self.is_disabled = False

    def disable(self):
        self.is_disabled = True
