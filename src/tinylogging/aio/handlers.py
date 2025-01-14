import sys
from abc import ABC, abstractmethod
from typing import Optional

import httpx
from anyio import AsyncFile, open_file

from tinylogging.formatter import Formatter
from tinylogging.level import Level
from tinylogging.record import Record

__all__ = [
    "BaseAsyncHandler",
    "AsyncStreamHandler",
    "AsyncFileHandler",
    "AsyncTelegramHandler",
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


class AsyncTelegramHandler(BaseAsyncHandler):
    def __init__(
        self, token: str, chat_id: int | str, ignore_errors: bool = False, **kwargs
    ):
        super().__init__(**kwargs)
        self.token = token
        self.chat_id = chat_id
        self.ignore_errors = ignore_errors
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    async def emit(self, record: Record):
        _colorize = self.formatter.colorize
        self.formatter.colorize = False
        text = self.formatter.format(record)
        self.formatter.colorize = _colorize

        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, json=data)

            if not self.ignore_errors:
                response.raise_for_status()
