from tinylogging.level import Level
from tinylogging.record import Record
from tinylogging.formatter import Formatter

from tinylogging.sync import Logger
from tinylogging.sync.handlers import (
    BaseHandler,
    StreamHandler,
    FileHandler,
    LoggingAdapterHandler,
)

from tinylogging.aio import AsyncLogger
from tinylogging.aio.handlers import (
    BaseAsyncHandler,
    AsyncStreamHandler,
    AsyncFileHandler,
)

__all__ = [
    "COLOR_MAP",
    "Record",
    "Formatter",
    "BaseHandler",
    "StreamHandler",
    "FileHandler",
    "LoggingAdapterHandler",
    "Logger",
    "AsyncLogger",
    "BaseAsyncHandler",
    "AsyncStreamHandler",
    "AsyncFileHandler",
    "Level",
]

COLOR_MAP = Formatter().color_map
"""Deprecated"""
