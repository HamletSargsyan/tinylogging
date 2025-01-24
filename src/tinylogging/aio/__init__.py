from tinylogging.aio.handlers import (
    AsyncFileHandler,
    AsyncStreamHandler,
    AsyncTelegramHandler,
    BaseAsyncHandler,
)
from tinylogging.formatter import Formatter
from tinylogging.level import Level
from tinylogging.record import Record

__all__ = [
    "AsyncLogger",
    "BaseAsyncHandler",
    "AsyncFileHandler",
    "AsyncTelegramHandler",
]


class AsyncLogger:
    def __init__(
        self,
        name: str,
        level: Level = Level.NOTSET,
        formatter: Formatter = Formatter(),
        handlers: set[BaseAsyncHandler] = set(),
    ) -> None:
        """
        Initializes an asynchronous logger.

        Args:
            name (str): The name of the logger.
            level (Level, optional): The logging level. Defaults to Level.NOTSET.
            formatter (Formatter, optional): The formatter for log messages. Defaults to Formatter().
            handlers (set[BaseAsyncHandler], optional): A set of handlers for the logger. Defaults to an empty set.
        """
        self.name = name
        self.level = level
        self.formatter = formatter
        self.is_disabled = False
        self.handlers = handlers or {AsyncStreamHandler(self.formatter, self.level)}

    async def log(self, message: str, level: Level) -> None:
        """
        Logs a message at the specified level.

        Args:
            message (str): The message to log.
            level (Level): The level at which to log the message.
        """
        if self.is_disabled or self.level > level:
            return

        record = Record(message, level, self.name)

        for handler in self.handlers:
            await handler.handle(record)

    async def trace(self, message: str) -> None:
        """
        Logs a message with TRACE level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.TRACE)

    async def debug(self, message: str) -> None:
        """
        Logs a message with DEBUG level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.DEBUG)

    async def info(self, message: str) -> None:
        """
        Logs a message with INFO level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.INFO)

    async def notice(self, message: str) -> None:
        """
        Logs a message with NOTICE level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.NOTICE)

    async def warning(self, message: str) -> None:
        """
        Logs a message with WARNING level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.WARNING)

    async def error(self, message: str) -> None:
        """
        Logs a message with ERROR level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.ERROR)

    async def critical(self, message: str) -> None:
        """
        Logs a message with CRITICAL level.

        Args:
            message (str): The message to log.
        """
        await self.log(message, level=Level.CRITICAL)

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
