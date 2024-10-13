from enum import IntEnum, auto


class Level(IntEnum):
    NOTSET = auto()
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    NOTICE = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
