from enum import IntEnum, auto


class Level(IntEnum):
    """Enumeration for logging levels.

    Attributes:
        NOTSET: No level set.
        TRACE: Trace level for detailed debugging.
        DEBUG: Debug level for general debugging.
        INFO: Informational messages.
        NOTICE: Notice level for normal but significant conditions.
        WARNING: Warning level for potentially harmful situations.
        ERROR: Error level for error events.
        CRITICAL: Critical level for severe error events.
    """

    NOTSET = auto()
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    NOTICE = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
