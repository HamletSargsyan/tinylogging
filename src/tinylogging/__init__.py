import sys

from datetime import datetime
from enum import IntEnum, auto
from abc import ABC, abstractmethod
from typing import Optional, TextIO
from dataclasses import dataclass, field

from colorama import Fore, Style


class Level(IntEnum):
    NOTSET = auto()
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    NOTICE = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


COLOR_MAP: dict[Level, str] = {
    Level.TRACE: Fore.WHITE + Style.DIM,
    Level.DEBUG: Fore.CYAN,
    Level.INFO: Fore.BLUE,
    Level.NOTICE: Fore.MAGENTA,
    Level.WARNING: Fore.LIGHTYELLOW_EX,  # cspell: disable-line
    Level.ERROR: Fore.LIGHTRED_EX,  # cspell: disable-line
    Level.CRITICAL: Fore.RED + Style.BRIGHT,
}


@dataclass
class Record:
    message: str
    level: Level
    name: str
    time: datetime = field(init=False)

    def __post_init__(self):
        self.time = datetime.now()


class Formatter:
    def __init__(
        self,
        time_format: str = "[%H:%M:%S]",
        template: str = "{time} | {level} | {message}",
        colorize: bool = True,
    ) -> None:
        self.template = template
        self.time_format = time_format
        self.colorize = colorize

    def format(self, record: Record) -> str:
        formatted_text = self.template.format(
            level=record.level.name,
            message=record.message,
            time=record.time.strftime(self.time_format),
            name=record.name,
        )

        if self.colorize:
            color = COLOR_MAP.get(record.level, "")
            return f"{color}{formatted_text}{Style.RESET_ALL}\n"
        return formatted_text + "\n"


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
        pass


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
            handler.emit(record)

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
