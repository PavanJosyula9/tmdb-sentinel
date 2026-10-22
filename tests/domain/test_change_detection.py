from datetime import UTC, datetime

import pytest

from tmdb_sentinel.domain.change_detection import detect_change
from tmdb_sentinel.domain.change_event import ChangeEvent
from tmdb_sentinel.domain.snapshot import Snapshot


def test_detect_change_returns_event_when_biography_changes() -> None:
    previous = Snapshot(
        person_id=18,
        biography="Old biography",
        observed_at=datetime(2026, 10, 21, tzinfo=UTC),
    )

    current = Snapshot(
        person_id=18,
        biography="New biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    change = detect_change(previous, current)

    assert change == ChangeEvent(
        person_id=18,
        field="biography",
        previous_value="Old biography",
        current_value="New biography",
        detected_at=current.observed_at,
    )


def test_detect_change_returns_None_when_biography_is_unchanged() -> None:
    previous = Snapshot(
        person_id=18,
        biography="Same biography",
        observed_at=datetime(2026, 10, 21, tzinfo=UTC),
    )

    current = Snapshot(
        person_id=18,
        biography="Same biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    change = detect_change(previous, current)

    assert change is None


def test_detect_change_detects_biography_becoming_empty() -> None:
    previous = Snapshot(
        person_id=18,
        biography="Existing biography",
        observed_at=datetime(2026, 10, 21, tzinfo=UTC),
    )

    current = Snapshot(
        person_id=18, biography="", observed_at=datetime(2026, 10, 22, tzinfo=UTC)
    )

    change = detect_change(previous, current)

    assert change is not None
    assert change.previous_value == "Existing biography"
    assert change.current_value == ""


def test_detect_change_detects_biography_becoming_non_empty() -> None:
    previous = Snapshot(
        person_id=18, biography="", observed_at=datetime(2026, 10, 21, tzinfo=UTC)
    )

    current = Snapshot(
        person_id=18,
        biography="New biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    change = detect_change(previous, current)

    assert change is not None
    assert change.previous_value == ""
    assert change.current_value == "New biography"


def test_detect_change_rejects_different_people() -> None:
    previous = Snapshot(
        person_id=18,
        biography="Biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    current = Snapshot(
        person_id=19,
        biography="Biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    with pytest.raises(ValueError, match="same person"):
        detect_change(previous, current)


def test_detect_change_ignores_observation_time_when_biography_is_same() -> None:
    previous = Snapshot(
        person_id=18,
        biography="Same biography",
        observed_at=datetime(2026, 10, 21, tzinfo=UTC),
    )

    current = Snapshot(
        person_id=18,
        biography="Same biography",
        observed_at=datetime(2026, 10, 22, tzinfo=UTC),
    )

    assert detect_change(previous, current) is None
