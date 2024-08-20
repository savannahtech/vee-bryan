from dataclasses import dataclass
from datetime import datetime


@dataclass
class Interaction:
    id: int
    input: str
    output: str
    created_at: datetime
