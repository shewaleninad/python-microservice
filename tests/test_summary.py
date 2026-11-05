from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_summary_success():

    response = client.post(
        "/summary",
        headers={"X-API-Key": settings.API_KEY},
        json={
            "text": "Python is popular. It is used for AI."
        }
    )

    assert response.status_code == 200
    assert "summary" in response.json()


def test_summary_missing_api_key():

    response = client.post(
        "/summary",
        json={"text": "Python is popular."}
    )

    assert response.status_code == 401


def test_summary_empty_text():

    response = client.post(
        "/summary",
        headers={"X-API-Key": settings.API_KEY},
        json={"text": ""}
    )

    assert response.status_code == 400

def test_summary_invalid_api_key():

    response = client.post(
        "/summary",
        headers={
            "X-API-Key": "wrong-api-key"
        },
        json={
            "text": "Python is a programming language."
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"