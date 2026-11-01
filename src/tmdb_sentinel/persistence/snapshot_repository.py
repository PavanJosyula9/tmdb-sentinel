from typing import Protocol

from tmdb_sentinel.domain.snapshot import Snapshot


class SnapshotRepository(Protocol):
    """Contract for storing and retrieving snapshots"""

    def save(self, snapshot: Snapshot) -> None:
        """Persist a Snapshot"""
        ...

    def get_latest(self, person_id: int) -> Snapshot | None:
        """Return the latest snapshot for a person, if one exists"""
        ...
