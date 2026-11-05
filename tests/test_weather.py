from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

client = TestClient(app)


def test_weather_success():

    mock_weather = {
        "city": "Pune",
        "temperature": 28.5,
        "condition": "Clear sky",
        "humidity": 60
    }

    with patch(
        "app.routers.weather.fetch_weather",
        new_callable=AsyncMock
    ) as mock_fetch:

        mock_fetch.return_value = mock_weather

        response = client.get("/weather?city=Pune")

    assert response.status_code == 200
    assert response.json()["city"] == "Pune"
    assert response.json()["temperature"] == 28.5

def test_weather_empty_city():

    response = client.get("/weather?city=")

    assert response.status_code == 422