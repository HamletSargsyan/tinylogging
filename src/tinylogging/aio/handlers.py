from abc import ABC, abstractmethod
import sys
from typing import Optional

from anyio import AsyncFile, open_file

from tinylogging.record import Record
from tinylogging.level import Level
from tinylogging.formatter import Formatter


__all__ = [
    "BaseAsyncHandler",
    "AsyncStreamHandler",
    "AsyncFileHandler",
]


class BaseAsyncHandler(ABC):
    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
    ) -> None:
        self.formatter = formatter
        self.level = level

    @abstractmethod
    async def emit(self, record: Record) -> None:
        raise NotImplementedError

    async def handle(self, record: Record):
        if record.level >= self.level:
            await self.emit(record)


class AsyncStreamHandler(BaseAsyncHandler):
    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
        stream: Optional[AsyncFile[str]] = None,
    ) -> None:
        super().__init__(formatter=formatter, level=level)
        self.stream = stream or AsyncFile(sys.stdout)

    async def emit(self, record: Record):
        message = self.formatter.format(record)
        await self.stream.write(message)
        await self.stream.flush()


class AsyncFileHandler(BaseAsyncHandler):
    def __init__(
        self,
        file_name: str,
        level: Level = Level.NOTSET,
        formatter: Formatter = Formatter(colorize=False),
    ) -> None:
        super().__init__(formatter=formatter, level=level)
        self.file_name = file_name

    async def emit(self, record: Record):
        message = self.formatter.format(record)
        async with await open_file(self.file_name, "a") as f:
            await f.write(message)
            await f.flush()
