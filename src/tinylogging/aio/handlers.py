import sys
from abc import ABC, abstractmethod
from typing import Optional, Any

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
    """
    Base class for all async handlers.
    """

    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
    ) -> None:
        """
        Initializes the BaseAsyncHandler.

        Args:
            formatter (Formatter): The formatter instance to format log records.
            level (Level): The logging level threshold for this handler.
        """
        self.formatter = formatter
        self.level = level

    @abstractmethod
    async def emit(self, record: Record) -> None:
        """
        Emit a log record.

        Args:
            record (Record): The log record to be emitted.

        Raises:
            NotImplementedError: This method should be overridden by subclasses.
        """
        raise NotImplementedError

    async def handle(self, record: Record) -> None:
        """
        Handle a log record if it meets the logging level threshold.

        Args:
            record (Record): The log record to be handled.
        """
        if record.level >= self.level:
            await self.emit(record)


class AsyncStreamHandler(BaseAsyncHandler):
    """
    Asynchronous handler for streaming log records.
    """

    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
        stream: Optional[AsyncFile[str]] = None,
    ) -> None:
        """
        Initializes the AsyncStreamHandler.

        Args:
            formatter (Formatter): The formatter instance to format log records.
            level (Level): The logging level threshold for this handler.
            stream (Optional[AsyncFile[str]]): The stream to write log records to.
        """
        super().__init__(formatter=formatter, level=level)
        self.stream = stream or AsyncFile(sys.stdout)

    async def emit(self, record: Record) -> None:
        """
        Emit a log record to the stream.

        Args:
            record (Record): The log record to be emitted.
        """
        message = self.formatter.format(record)
        await self.stream.write(message)
        await self.stream.flush()


class AsyncFileHandler(BaseAsyncHandler):
    """
    Asynchronous handler for writing log records to a file.
    """

    def __init__(
        self,
        file_name: str,
        level: Level = Level.NOTSET,
        formatter: Formatter = Formatter(colorize=False),
    ) -> None:
        """
        Initializes the AsyncFileHandler.

        Args:
            file_name (str): The name of the file to write log records to.
            level (Level): The logging level threshold for this handler.
            formatter (Formatter): The formatter instance to format log records.
        """
        super().__init__(formatter=formatter, level=level)
        self.file_name = file_name

    async def emit(self, record: Record) -> None:
        """
        Emit a log record to the file.

        Args:
            record (Record): The log record to be emitted.
        """
        message = self.formatter.format(record)
        async with await open_file(self.file_name, "a") as f:
            await f.write(message)
            await f.flush()


class AsyncTelegramHandler(BaseAsyncHandler):
    """
    Asynchronous handler for sending log records to a Telegram chat.
    """

    def __init__(
        self,
        token: str,
        chat_id: int | str,
        message_thread_id: Optional[int] = None,
        ignore_errors: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the AsyncTelegramHandler.

        Args:
            token (str): The Telegram bot token.
            chat_id (int | str): The chat ID to send log records to.
            message_thread_id (Optional[int]): The message thread ID (optional).
            ignore_errors (bool): Whether to ignore errors during sending.
            **kwargs: Additional keyword arguments for the base handler.
        """
        super().__init__(**kwargs)
        self.token = token
        self.chat_id = chat_id
        self.message_thread_id = message_thread_id
        self.ignore_errors = ignore_errors
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    async def emit(self, record: Record) -> None:
        """
        Emit a log record to the Telegram chat.

        Args:
            record (Record): The log record to be emitted.
        """
        _colorize = self.formatter.colorize
        self.formatter.colorize = False
        text = self.formatter.format(record)
        self.formatter.colorize = _colorize

        data = {
            "chat_id": self.chat_id,
            "message_thread_id": self.message_thread_id,
            "text": text,
            "parse_mode": "HTML",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, json=data)

            if not self.ignore_errors:
                response.raise_for_status()
