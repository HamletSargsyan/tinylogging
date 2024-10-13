from dataclasses import dataclass, field
from datetime import datetime
from tinylogging.level import Level


@dataclass
class Record:
    message: str
    level: Level
    name: str
    time: datetime = field(init=False)

    def __post_init__(self):
        self.time = datetime.now()
