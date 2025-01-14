from tinylogging.aio import AsyncLogger
from tinylogging.aio.handlers import (
    AsyncFileHandler,
    AsyncStreamHandler,
    BaseAsyncHandler,
    AsyncTelegramHandler,
)
from tinylogging.formatter import Formatter
from tinylogging.level import Level
from tinylogging.record import Record
from tinylogging.sync import Logger
from tinylogging.sync.handlers import (
    BaseHandler,
    FileHandler,
    LoggingAdapterHandler,
    StreamHandler,
    TelegramHandler,
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
    "AsyncTelegramHandler",
    "TelegramHandler",
]

COLOR_MAP = Formatter().color_map
"""Deprecated"""
