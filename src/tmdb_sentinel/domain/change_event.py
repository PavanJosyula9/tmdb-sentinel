from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ChangeEvent:
    person_id: int
    field: str
    previous_value: str
    current_value: str
    detected_at: datetime
