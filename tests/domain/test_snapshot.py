from datetime import UTC, datetime

import pytest

from tmdb_sentinel.domain.snapshot import Snapshot


def test_snapshot_contains_observed_biography() -> None:
    observed_at = datetime(2026, 10, 4, tzinfo=UTC)

    snapshot = Snapshot(
        person_id=18,
        biography="A test biography",
        observed_at=observed_at,
    )

    assert snapshot.person_id == 18
    assert snapshot.biography == "A test biography"
    assert snapshot.observed_at == observed_at


def test_snapshot_is_immutable() -> None:
    snapshot = Snapshot(
        person_id=18,
        biography="A test biography",
        observed_at=datetime(2026, 10, 4, tzinfo=UTC),
    )

    with pytest.raises(AttributeError):
        snapshot.biography = "Changed"
