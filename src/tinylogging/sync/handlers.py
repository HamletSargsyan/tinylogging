import logging
import sys
from abc import ABC, abstractmethod
from typing import Optional, TextIO

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
    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
    ) -> None:
        self.formatter = formatter
        self.level = level

    @abstractmethod
    def emit(self, record: Record) -> None:
        raise NotImplementedError

    def handle(self, record: Record):
        if record.level >= self.level:
            self.emit(record)


class StreamHandler(BaseHandler):
    def __init__(
        self,
        formatter: Formatter = Formatter(),
        level: Level = Level.NOTSET,
        stream: Optional[TextIO] = None,
    ) -> None:
        super().__init__(formatter=formatter, level=level)
        self.stream = stream or sys.stdout  # type: TextIO

    def emit(self, record: Record):
        message = self.formatter.format(record)
        self.stream.write(message)
        self.stream.flush()


class FileHandler(BaseHandler):
    def __init__(
        self,
        file_name: str,
        level: Level = Level.NOTSET,
        formatter: Formatter = Formatter(colorize=False),
    ) -> None:
        super().__init__(formatter=formatter, level=level)
        self.file_name = file_name

    def emit(self, record: Record):
        message = self.formatter.format(record)
        with open(self.file_name, "a") as f:
            f.write(message)
            f.flush()


class LoggingAdapterHandler(logging.Handler):
    def __init__(
        self,
        handler: BaseHandler,
    ):
        super().__init__()
        self.custom_handler = handler

    def emit(self, record: logging.LogRecord):
        level = Level[record.levelname]  # cspell: disable-line
        custom_record = Record(
            message=self.format(record), level=level, name=record.name
        )

        custom_record.filename = record.filename
        custom_record.function = record.funcName
        custom_record.line = record.lineno

        self.custom_handler.handle(custom_record)


class TelegramHandler(BaseHandler):
    def __init__(
        self, token: str, chat_id: int | str, ignore_errors: bool = False, **kwargs
    ):
        super().__init__(**kwargs)
        self.token = token
        self.chat_id = chat_id
        self.ignore_errors = ignore_errors
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def emit(self, record: Record):
        _colorize = self.formatter.colorize
        self.formatter.colorize = False
        text = self.formatter.format(record)
        self.formatter.colorize = _colorize

        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
        }

        with httpx.Client() as client:
            response = client.post(self.api_url, json=data)

            if not self.ignore_errors:
                response.raise_for_status()
