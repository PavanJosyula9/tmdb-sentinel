from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Snapshot:
    person_id: int
    biography: str
    observed_at: datetime
