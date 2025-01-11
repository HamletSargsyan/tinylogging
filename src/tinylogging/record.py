import inspect
import os
from dataclasses import dataclass, field
from datetime import datetime

from tinylogging.level import Level


@dataclass
class Record:
    message: str
    level: Level
    name: str
    time: datetime = field(init=False)
    filename: str = field(init=False)
    line: int = field(init=False)
    function: str = field(init=False)

    @property
    def basename(self) -> str:
        return os.path.basename(self.filename)

    @property
    def relpath(self) -> str:
        return os.path.relpath(self.filename)

    def __post_init__(self):
        self.time = datetime.now()

        depth = self._get_stack_index()
        frame = inspect.stack()[depth]

        depth = self._get_stack_index()
        frame = inspect.currentframe()
        for _ in range(depth):
            frame = frame.f_back

        self.filename = frame.f_code.co_filename
        self.line = frame.f_lineno
        self.function = frame.f_code.co_name

    def _get_stack_index(self) -> int:
        current_frame = inspect.currentframe()
        index = 0
        while current_frame:
            if current_frame.f_code.co_name == "log":
                return index + 1
            current_frame = current_frame.f_back
            index += 1
        return 1
