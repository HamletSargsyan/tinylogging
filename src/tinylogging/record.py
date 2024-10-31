from dataclasses import dataclass, field
from datetime import datetime
import os
from tinylogging.level import Level
import inspect


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
        self.filename = frame.filename
        self.line = frame.lineno
        self.function = frame.function

    def _get_stack_index(self) -> int:
        current_frame = inspect.currentframe()
        index = 0
        while current_frame:
            index += 1
            current_frame = current_frame.f_back
            if current_frame and current_frame.f_code.co_name == "log":
                break
        return index + 1
