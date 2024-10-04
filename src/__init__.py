from colorama import Fore, Style, init
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum, auto
import sys
from typing import Optional


init()


class Level(IntEnum):
    NOTSET = auto()
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    NOTICE = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class Record:
    message: str
    level: Level
    time: datetime = field(init=False)

    def __post_init__(self):
        self.time = datetime.now()


class Formatter:
    def __init__(
        self,
        time_format: str = "[%H:%M:%S]",
        template: str = "{time} | {level} | {message}",
    ) -> None:
        self.template = template
        self.time_format = time_format

    def format(self, record: Record) -> str:
        return self.template.format(
            level=record.level.name,
            message=record.message,
            time=record.time.strftime(self.time_format),
        )


COLOR_MAP: dict[Level, str] = {
    Level.TRACE: Fore.WHITE + Style.DIM,
    Level.DEBUG: Fore.CYAN,
    Level.INFO: Fore.BLUE,
    Level.NOTICE: Fore.MAGENTA,
    Level.WARNING: Fore.LIGHTYELLOW_EX,  # cspell: disable-line
    Level.ERROR: Fore.LIGHTRED_EX,  # cspell: disable-line
    Level.CRITICAL: Fore.RED + Style.BRIGHT,
}


class Logger:
    def __init__(
        self,
        level: Optional[Level] = None,
        formatter: Optional[Formatter] = None,
        colorize: bool = True,
    ) -> None:
        self.level = level or Level.NOTSET
        self.formatter = formatter or Formatter()
        self.is_disabled = False
        self.colorize = colorize

    def log(self, message: str, level: Level):
        if self.level > level or self.is_disabled:
            return

        record = Record(message, level)
        msg = self.formatter.format(record)

        if self.colorize:
            color = COLOR_MAP.get(level, "")
            msg = f"{color}{msg}{Style.RESET_ALL}"

        sys.stdout.write(msg + "\n")
        sys.stdout.flush()

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
