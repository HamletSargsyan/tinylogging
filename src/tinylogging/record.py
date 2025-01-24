import inspect
import os
from dataclasses import dataclass, field
from datetime import datetime

from tinylogging.level import Level


@dataclass
class Record:
    """Represents a log record.

    Attributes:
        message (str): The log message.
        level (Level): The log level.
        name (str): The name of the logger.
        time (datetime): The time the log record was created.
        filename (str): The name of the file where the log record was created.
        line (int): The line number in the file where the log record was created.
        function (str): The function name where the log record was created.
    """

    message: str
    level: Level
    name: str
    time: datetime = field(init=False)
    filename: str = field(init=False)
    line: int = field(init=False)
    function: str = field(init=False)

    @property
    def basename(self) -> str:
        """Gets the base name of the file where the log record was created.

        Returns:
            str: The base name of the file.
        """
        return os.path.basename(self.filename)

    @property
    def relpath(self) -> str:
        """Gets the relative path of the file where the log record was created.

        Returns:
            str: The relative path of the file.
        """
        return os.path.relpath(self.filename)

    def __post_init__(self) -> None:
        """Initializes additional attributes after the dataclass is created."""
        self.time = datetime.now()

        depth = self._get_stack_index()
        frame = inspect.stack()[depth]

        depth = self._get_stack_index()
        frame = inspect.currentframe()
        for _ in range(depth):
            frame = frame.f_back

        if not frame:
            raise RuntimeError("Failed to get stack frame")

        self.filename = frame.f_code.co_filename
        self.line = frame.f_lineno
        self.function = frame.f_code.co_name

    def _get_stack_index(self) -> int:
        """Gets the index of the stack frame for the log record.

        Returns:
            int: The index of the stack frame.
        """
        current_frame = inspect.currentframe()
        index = 0
        while current_frame:
            if current_frame.f_code.co_name == "log":
                return index + 1
            current_frame = current_frame.f_back
            index += 1
        return 1
