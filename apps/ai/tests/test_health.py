"""Smoke tests for the AI Gateway."""

from fastapi.testclient import TestClient

from sdgi_ai.main import app

client = TestClient(app)


def test_health() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["service"] == "ai"


def test_ready() -> None:
    res = client.get("/ready")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["checks"]["self"] == "ok"


def test_request_id_round_trip() -> None:
    res = client.get("/health", headers={"x-request-id": "trace-abc-1234-5678"})
    assert res.headers.get("x-request-id") == "trace-abc-1234-5678"


def test_request_id_generated_when_missing() -> None:
    res = client.get("/health")
    rid = res.headers.get("x-request-id")
    assert rid is not None
    assert len(rid) >= 8
