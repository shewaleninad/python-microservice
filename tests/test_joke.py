from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

client = TestClient(app)


def test_joke_success():

    mock_joke = {
        "joke": "Why did Python cross the road? To get to the other side.",
        "category": "programming"
    }

    with patch(
        "app.routers.joke.fetch_joke",
        new_callable=AsyncMock
    ) as mock_fetch:

        mock_fetch.return_value = mock_joke

        response = client.get("/joke")

    assert response.status_code == 200
    assert "joke" in response.json()
    assert response.json()["category"] == "programming"


def test_joke_provider_error():

    from app.services.joke_service import JokeUpstreamError

    with patch(
        "app.routers.joke.fetch_joke",
        new_callable=AsyncMock
    ) as mock_fetch:

        mock_fetch.side_effect = JokeUpstreamError()

        response = client.get("/joke")

    assert response.status_code == 502
    assert response.json()["detail"] == "Joke provider is unavailable"