import os
from dataclasses import dataclass


@dataclass
class Settings:
    tmdb_api_read_access_token: str
    tmdb_base_url: str = "https://www.api.themoviedb.org/3"
    tmdb_timeout: float = 10.0

    @classmethod
    def from_environment(cls) -> "Settings":
        token: str | None = os.environ.get("TMDB_API_READ_ACCESS_TOKEN")

        if not token:
            raise ValueError("TMDB_API_READ_ACCESS_TOKEN is not set")

        return cls(tmdb_api_read_access_token=token)
