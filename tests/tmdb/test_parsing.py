import pytest

from tmdb_sentinel.tmdb.exceptions import TMDBError
from tmdb_sentinel.tmdb.parsing import parse_person


def test_parse_person() -> None:
    data = {
        "id": 18,
        "name": "Test Person",
        "biography": "A test biography",
    }

    person = parse_person(data)

    assert person.id == 18
    assert person.name == "Test Person"
    assert person.biography == "A test biography"


def test_parse_person_requires_biography() -> None:
    data = {
        "id": 18,
        "name": "Test Person",
    }

    with pytest.raises(KeyError):
        parse_person(data)


def test_parse_person_rejects_non_integer_id() -> None:
    data = {
        "id": "18",
        "name": "Test Person",
        "biography": "A test biography",
    }

    with pytest.raises(TMDBError):
        parse_person(data=data)


def test_parse_person_rejects_non_string_name() -> None:
    data = {
        "id": 18,
        "name": 123,
        "biography": "A test biography",
    }

    with pytest.raises(TMDBError):
        parse_person(data=data)


def test_parse_person_rejects_non_string_biography() -> None:
    data = {
        "id": 18,
        "name": "Test Person",
        "biography": None,
    }

    with pytest.raises(TMDBError):
        parse_person(data=data)


def test_parse_person_accepts_empty_biography() -> None:
    data = {
        "id": 18,
        "name": "Test Person",
        "biography": "",
    }

    person = parse_person(data=data)

    assert person.biography == ""
