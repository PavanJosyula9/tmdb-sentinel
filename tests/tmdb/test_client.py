import httpx
import pytest

from tmdb_sentinel.config import Settings
from tmdb_sentinel.tmdb.client import TMDBClient
from tmdb_sentinel.tmdb.exceptions import TMDBError


def test_client_accepts_settings() -> None:
    settings = Settings(
        tmdb_api_read_access_token="test-token",
    )

    client = TMDBClient(settings)

    assert client._settings is settings


def test_client_configures_settings() -> None:
    settings = Settings(
        tmdb_api_read_access_token="test-token",
        tmdb_base_url="https://example.com",
        tmdb_timeout=5.0,
    )

    client = TMDBClient(settings)

    assert client._client.base_url == "https://example.com"
    assert client._client.timeout.read == 5.0


def test_client_configures_authentication_header() -> None:
    settings = Settings(tmdb_api_read_access_token="test-token")

    client = TMDBClient(settings)

    assert client._client.headers["Authorization"] == "Bearer test-token"


def test_get_person_returns_person() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/3/person/18"
        assert request.url.params["language"] == "en-US"

        return httpx.Response(
            200,
            json={
                "id": 18,
                "name": "Test Person",
                "biography": "A test biography",
            },
        )

    transport = httpx.MockTransport(handler)

    settings = Settings(
        tmdb_api_read_access_token="test-token",
    )

    client = TMDBClient(settings, transport=transport)

    person = client.get_person(18)

    assert person.id == 18
    assert person.name == "Test Person"
    assert person.biography == "A test biography"


def test_get_person_sends_authentication_header() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-token"

        return httpx.Response(
            200,
            json={
                "id": 18,
                "name": "Test Person",
                "biography": "A test biography",
            },
        )

    transport = httpx.MockTransport(handler)

    settings = Settings(tmdb_api_read_access_token="test-token")

    client = TMDBClient(settings, transport=transport)

    client.get_person(18)


def test_get_person_raises_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={
                "status": 34,
                "status_message": "The resource you requested could not be found.",
            },
        )

    transport = httpx.MockTransport(handler)

    settings = Settings(tmdb_api_read_access_token="test-token")

    client = TMDBClient(settings, transport=transport)

    with pytest.raises(TMDBError):
        client.get_person(18)


def test_get_person_rejects_missing_biography() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": 18,
                "name": "Test Person",
            },
        )

    transport = httpx.MockTransport(handler)

    settings = Settings(tmdb_api_read_access_token="test-token")

    client = TMDBClient(settings, transport=transport)

    with pytest.raises(KeyError):
        client.get_person(18)
