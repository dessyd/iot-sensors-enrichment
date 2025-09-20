from fastapi.testclient import TestClient

from app import app as fastapi_app


client = TestClient(fastapi_app)


def test_token_missing_credentials() -> None:
    r = client.post("/auth/token", data={})
    assert r.status_code == 422
