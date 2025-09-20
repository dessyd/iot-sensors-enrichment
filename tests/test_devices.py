from fastapi.testclient import TestClient

from app import app as fastapi_app


client = TestClient(fastapi_app)


def test_list_devices_unauthenticated() -> None:
    r = client.get("/devices")
    assert r.status_code in (401, 422)
