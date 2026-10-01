from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    id: int
    name: str
    biography: str
