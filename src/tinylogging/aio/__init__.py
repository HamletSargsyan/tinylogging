from tinylogging.aio.handlers import (
    AsyncFileHandler,
    AsyncStreamHandler,
    BaseAsyncHandler,
    AsyncTelegramHandler,
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
        self.name = name
        self.level = level
        self.formatter = formatter
        self.is_disabled = False
        self.handlers = handlers or {AsyncStreamHandler(self.formatter, self.level)}

    async def log(self, message: str, level: Level):
        if self.level > level or self.is_disabled:
            return

        record = Record(message, level, self.name)

        for handler in self.handlers:
            await handler.handle(record)

    async def trace(self, message: str):
        await self.log(message, level=Level.TRACE)

    async def debug(self, message: str):
        await self.log(message, level=Level.DEBUG)

    async def info(self, message: str):
        await self.log(message, level=Level.INFO)

    async def notice(self, message: str):
        await self.log(message, level=Level.NOTICE)

    async def warning(self, message: str):
        await self.log(message, level=Level.WARNING)

    async def error(self, message: str):
        await self.log(message, level=Level.ERROR)

    async def critical(self, message: str):
        await self.log(message, level=Level.CRITICAL)

    def enable(self):
        self.is_disabled = False

    def disable(self):
        self.is_disabled = True
