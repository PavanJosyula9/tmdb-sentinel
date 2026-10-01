import pytest

from tmdb_sentinel.tmdb.models import Person


def test_person_contains_expected_fields() -> None:
    person = Person(
        id=31,
        name="Test Person",
        biography="A test biography.",
    )

    assert person.id == 31
    assert person.name == "Test Person"
    assert person.biography == "A test biography."


def test_person_is_immutable() -> None:
    person = Person(
        id=31,
        name="Test Person",
        biography="A test biography.",
    )

    with pytest.raises(AttributeError):
        person.name = "Changed Name"
