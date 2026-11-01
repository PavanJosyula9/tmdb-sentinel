from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from tmdb_sentinel.domain.snapshot import Snapshot
from tmdb_sentinel.persistence.snapshot_repository import SnapshotRepository
from tmdb_sentinel.persistence.sqlite_snapshot_repository import (
    SQLiteSnapshotRepository,
)


def test_sqlite_repository_returns_none_when_no_snapshot_exists(
    tmp_path: Path,
) -> None:
    repository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        assert repository.get_latest(18) is None
    finally:
        repository.close()


def test_sqlite_repository_saves_and_retrieves_snapshot(tmp_path: Path) -> None:
    repository: SnapshotRepository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        snapshot = Snapshot(
            person_id=18,
            biography="Test biography",
            observed_at=datetime(2026, 10, 22, tzinfo=UTC),
        )

        repository.save(snapshot)

        assert repository.get_latest(18) == snapshot
    finally:
        repository.close()


def test_sqlite_repository_returns_latest_snapshot(tmp_path: Path) -> None:
    repository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        older = Snapshot(
            person_id=18,
            biography="Old biography",
            observed_at=datetime(2026, 10, 21, tzinfo=UTC),
        )

        newer = Snapshot(
            person_id=18,
            biography="New biography",
            observed_at=datetime(2026, 10, 22, tzinfo=UTC),
        )

        repository.save(newer)
        repository.save(older)

        assert repository.get_latest(18) == newer
    finally:
        repository.close()


def test_sqlite_repository_keeps_people_separate(tmp_path: Path) -> None:
    repository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        person_18 = Snapshot(
            person_id=18,
            biography="Person 18",
            observed_at=datetime(2026, 10, 22, tzinfo=UTC),
        )

        person_42 = Snapshot(
            person_id=42,
            biography="Person 42",
            observed_at=datetime(2026, 10, 22, tzinfo=UTC),
        )

        repository.save(person_18)
        repository.save(person_42)

        assert repository.get_latest(18) == person_18
        assert repository.get_latest(42) == person_42
    finally:
        repository.close()


def test_sqlite_repository_preserves_data_after_reopening(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "test.db"

    first_repository = SQLiteSnapshotRepository(database_path)

    snapshot = Snapshot(
        person_id=18,
        biography="Persistent biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    first_repository.save(snapshot)
    first_repository.close()

    second_repository = SQLiteSnapshotRepository(database_path)

    try:
        assert second_repository.get_latest(18) == snapshot
    finally:
        second_repository.close()


def test_sqlite_repository_normalizes_timestamp_to_utc(tmp_path: Path) -> None:
    repository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        original_timestamp = datetime(
            2026,
            10,
            22,
            23,
            0,
            tzinfo=timezone(timedelta(hours=5, minutes=30)),
        )

        snapshot = Snapshot(
            person_id=18,
            biography="Test biography",
            observed_at=original_timestamp,
        )

        repository.save(snapshot)

        retrieved = repository.get_latest(18)

        assert retrieved is not None
        assert retrieved.observed_at.tzinfo == UTC
        assert retrieved.observed_at == original_timestamp
    finally:
        repository.close()


def test_sqlite_repository_rejects_naive_datetime(tmp_path: Path) -> None:
    repository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        snapshot = Snapshot(
            person_id=18,
            biography="Test biography",
            # Deliberately naive: tests that the repository rejects naive timestamps.
            observed_at=datetime.fromisoformat("2026-10-22"),
        )

        with pytest.raises(ValueError, match="timezone-aware"):
            repository.save(snapshot)

        assert repository.get_latest(18) is None
    finally:
        repository.close()


def test_sqlite_repository_uses_id_to_break_timestamp_ties(tmp_path: Path) -> None:
    repository = SQLiteSnapshotRepository(tmp_path / "test.db")

    try:
        observed_at = datetime(2026, 10, 26, tzinfo=UTC)

        first = Snapshot(
            person_id=18,
            biography="First biography",
            observed_at=observed_at,
        )

        second = Snapshot(
            person_id=18, biography="Second biography", observed_at=observed_at
        )

        repository.save(first)
        repository.save(second)

        assert repository.get_latest(18) == second

    finally:
        repository.close()
