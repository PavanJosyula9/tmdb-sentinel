import httpx

from tmdb_sentinel.config import Settings
from tmdb_sentinel.tmdb.exceptions import TMDBError
from tmdb_sentinel.tmdb.models import Person
from tmdb_sentinel.tmdb.parsing import parse_person


class TMDBClient:
    def __init__(
        self, settings: Settings, transport: httpx.BaseTransport | None = None
    ) -> None:
        self._settings = settings
        self._client = httpx.Client(
            base_url=settings.tmdb_base_url,
            timeout=settings.tmdb_timeout,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_read_access_token}",
                "accept": "application/json",
            },
            transport=transport,
        )

    def get_person(self, person_id: int) -> Person:
        response = self._client.get(
            f"/person/{person_id}",
            params={
                "language": "en-US",
            },
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise TMDBError(
                f"TMDB request failed with status {response.status_code}"
            ) from exc

        data = response.json()

        return parse_person(data=data)
