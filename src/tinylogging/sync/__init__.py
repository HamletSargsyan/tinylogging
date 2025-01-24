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
        """
        Initializes a new Logger instance.

        Args:
            name (str): The name of the logger.
            level (Level, optional): The logging level. Defaults to Level.NOTSET.
            formatter (Formatter, optional): The formatter for log messages. Defaults to Formatter().
            handlers (set[BaseHandler], optional): A set of handlers for the logger. Defaults to an empty set.
        """
        self.name = name
        self.level = level
        self.formatter = formatter
        self.is_disabled = False
        self.handlers = handlers or {StreamHandler(self.formatter, self.level)}

    def log(self, message: str, level: Level) -> None:
        """
        Logs a message with the specified logging level.

        Args:
            message (str): The message to log.
            level (Level): The logging level for the message.
        """
        if self.is_disabled or self.level > level:
            return

        record = Record(message, level, self.name)

        for handler in self.handlers:
            handler.handle(record)

    def trace(self, message: str) -> None:
        """
        Logs a message with TRACE level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.TRACE)

    def debug(self, message: str) -> None:
        """
        Logs a message with DEBUG level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.DEBUG)

    def info(self, message: str) -> None:
        """
        Logs a message with INFO level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.INFO)

    def notice(self, message: str) -> None:
        """
        Logs a message with NOTICE level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.NOTICE)

    def warning(self, message: str) -> None:
        """
        Logs a message with WARNING level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.WARNING)

    def error(self, message: str) -> None:
        """
        Logs a message with ERROR level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.ERROR)

    def critical(self, message: str) -> None:
        """
        Logs a message with CRITICAL level.

        Args:
            message (str): The message to log.
        """
        self.log(message, level=Level.CRITICAL)

    def enable(self) -> None:
        """
        Enables the logger.
        """
        self.is_disabled = False

    def disable(self) -> None:
        """
        Disables the logger.
        """
        self.is_disabled = True
