from datetime import UTC, datetime

from tmdb_sentinel.domain.snapshot import Snapshot
from tmdb_sentinel.persistence.snapshot_repository import SnapshotRepository


class InMemorySnapshotRepository:
    def __init__(self) -> None:
        self._snapshots: list[Snapshot] = []

    def save(self, snapshot: Snapshot) -> None:
        self._snapshots.append(snapshot)

    def get_latest(self, person_id: int) -> Snapshot | None:
        matching = [
            snapshot for snapshot in self._snapshots if snapshot.person_id == person_id
        ]

        if not matching:
            return None

        return max(matching, key=lambda snapshot: snapshot.observed_at)


def test_repository_returns_none_when_person_has_no_snapshot() -> None:
    repository: SnapshotRepository = InMemorySnapshotRepository()

    assert repository.get_latest(18) is None


def test_repository_returns_latest_snapshot() -> None:
    repository: SnapshotRepository = InMemorySnapshotRepository()

    older = Snapshot(
        person_id=18,
        biography="Old biography",
        observed_at=datetime(2026, 10, 31, tzinfo=UTC),
    )

    newer = Snapshot(
        person_id=18,
        biography="New biography",
        observed_at=datetime(2026, 11, 1, tzinfo=UTC),
    )

    repository.save(older)
    repository.save(newer)

    assert repository.get_latest(18) == newer


def test_repository_keeps_people_separate() -> None:
    repository: SnapshotRepository = InMemorySnapshotRepository()

    person_18 = Snapshot(
        person_id=18,
        biography="Biograhy of person 18",
        observed_at=datetime(2026, 11, 1, tzinfo=UTC),
    )

    person_19 = Snapshot(
        person_id=19,
        biography="Biography of person 19",
        observed_at=datetime(2026, 11, 1, tzinfo=UTC),
    )

    repository.save(person_18)
    repository.save(person_19)

    assert repository.get_latest(18) == person_18
    assert repository.get_latest(19) == person_19
