import logging
import sys
from abc import ABC, abstractmethod
from typing import TextIO, Optional, Any

import httpx

from tinylogging.formatter import Formatter
from tinylogging.level import Level
from tinylogging.record import Record

__all__ = [
    "BaseHandler",
    "StreamHandler",
    "FileHandler",
    "LoggingAdapterHandler",
    "TelegramHandler",
]


class BaseHandler(ABC):
    """Abstract base class for all handlers.

    Args:
        formatter (Formatter): Formatter instance to format the log records.
        level (Level): Logging level for the handler.
    """

    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
    ) -> None:
        self.formatter = formatter
        self.level = level

    @abstractmethod
    def emit(self, record: Record) -> None:
        """Emit a log record.

        Args:
            record (Record): The log record to be emitted.
        """
        raise NotImplementedError

    def handle(self, record: Record) -> None:
        """Handle a log record.

        Args:
            record (Record): The log record to be handled.
        """
        if record.level >= self.level:
            self.emit(record)


class StreamHandler(BaseHandler):
    """Handler for streaming log records to a stream.

    Args:
        formatter (Formatter): Formatter instance to format the log records.
        level (Level): Logging level for the handler.
        stream (Optional[TextIO]): Stream to write log records to.
    """

    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
        stream: Optional[TextIO] = None,
    ) -> None:
        super().__init__(formatter=formatter, level=level)
        self.stream = stream or sys.stdout  # type: TextIO

    def emit(self, record: Record) -> None:
        """Emit a log record to the stream.

        Args:
            record (Record): The log record to be emitted.
        """
        message = self.formatter.format(record)
        self.stream.write(message)
        self.stream.flush()


class FileHandler(BaseHandler):
    """Handler for writing log records to a file.

    Args:
        file_name (str): Name of the file to write log records to.
        level (Level): Logging level for the handler.
        formatter (Formatter): Formatter instance to format the log records.
    """

    def __init__(
        self,
        file_name: str,
        level: Level = Level.NOTSET,
        formatter: Formatter = Formatter(colorize=False),
    ) -> None:
        super().__init__(formatter=formatter, level=level)
        self.file_name = file_name

    def emit(self, record: Record) -> None:
        """Emit a log record to the file.

        Args:
            record (Record): The log record to be emitted.
        """
        message = self.formatter.format(record)
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(message)
            f.flush()


class LoggingAdapterHandler(logging.Handler):
    """Adapter handler to integrate with the standard logging module.

    Args:
        handler (BaseHandler): Custom handler to delegate log records to.
    """

    def __init__(
        self,
        handler: BaseHandler,
    ) -> None:
        super().__init__()
        self.custom_handler = handler

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record using the custom handler.

        Args:
            record (logging.LogRecord): The log record to be emitted.
        """
        level = Level[record.levelname]  # cspell: disable-line
        custom_record = Record(
            message=self.format(record),
            level=level,
            name=record.name,
        )

        custom_record.filename = record.filename
        custom_record.function = record.funcName
        custom_record.line = record.lineno

        self.custom_handler.handle(custom_record)


class TelegramHandler(BaseHandler):
    """Handler for sending log records to a Telegram chat.

    Args:
        token (str): Telegram bot token.
        chat_id (int | str): Chat ID to send messages to.
        ignore_errors (bool): Whether to ignore errors when sending messages.
        message_thread_id (Optional[int]): ID of the message thread.
        **kwargs: Additional keyword arguments for the base handler.
    """

    def __init__(
        self,
        token: str,
        chat_id: int | str,
        ignore_errors: bool = False,
        message_thread_id: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.token = token
        self.chat_id = chat_id
        self.message_thread_id = message_thread_id
        self.ignore_errors = ignore_errors
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def emit(self, record: Record) -> None:
        """Emit a log record to the Telegram chat.

        Args:
            record (Record): The log record to be emitted.
        """
        _colorize = self.formatter.colorize
        self.formatter.colorize = False
        text = self.formatter.format(record)
        self.formatter.colorize = _colorize

        data = {
            "chat_id": self.chat_id,
            "text": text,
            "message_thread_id": self.message_thread_id,
            "parse_mode": "HTML",
        }

        with httpx.Client() as client:
            response = client.post(self.api_url, json=data)

            if not self.ignore_errors:
                response.raise_for_status()
