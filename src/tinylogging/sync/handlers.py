from abc import ABC, abstractmethod
import logging
import sys
from typing import Optional, TextIO

from tinylogging.record import Record
from tinylogging.level import Level
from tinylogging.formatter import Formatter


__all__ = [
    "BaseHandler",
    "StreamHandler",
    "FileHandler",
    "LoggingAdapterHandler",
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
        self.custom_handler.handle(custom_record)
