from typing import Any

from tmdb_sentinel.tmdb.exceptions import TMDBError
from tmdb_sentinel.tmdb.models import Person


def parse_person(data: dict[str, Any]) -> Person:
    person_id = data["id"]
    name = data["name"]
    biography = data["biography"]

    if type(person_id) is not int:
        raise TMDBError("TMDB person id is not integer")

    if not isinstance(name, str):
        raise TMDBError("TMDB person name is not string")

    if not isinstance(biography, str):
        raise TMDBError("TMDB person biography is not string")

    return Person(id=person_id, name=name, biography=biography)
