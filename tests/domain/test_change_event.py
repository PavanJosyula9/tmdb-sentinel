from datetime import UTC, datetime

import pytest

from tmdb_sentinel.domain.change_event import ChangeEvent


def test_change_event_contains_change_information() -> None:
    detected_at = datetime(2026, 10, 4, tzinfo=UTC)

    change_event = ChangeEvent(
        person_id=18,
        field="biography",
        previous_value="Old biography",
        current_value="New biography",
        detected_at=detected_at,
    )

    assert change_event.person_id == 18
    assert change_event.field == "biography"
    assert change_event.previous_value == "Old biography"
    assert change_event.current_value == "New biography"
    assert change_event.detected_at == detected_at


def test_change_event_is_immutable() -> None:
    change_event = ChangeEvent(
        person_id=18,
        field="biography",
        previous_value="Old biography",
        current_value="New biography",
        detected_at=datetime(2026, 10, 4, tzinfo=UTC),
    )

    with pytest.raises(AttributeError):
        change_event.current_value = "Changed biography"
