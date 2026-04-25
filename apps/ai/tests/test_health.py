"""Smoke test for the AI Gateway health endpoint."""

from fastapi.testclient import TestClient

from sdgi_ai.main import app

client = TestClient(app)


def test_health() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["service"] == "ai"
