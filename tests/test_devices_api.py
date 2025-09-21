from app.auth import create_access_token
import uuid


def test_devices_list_is_list_of_ids(client):
    # Ensure list returns an array of strings (device ids)
    token = create_access_token(data={"sub": "admin"})
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/devices", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # if non-empty, each element should be a string
    if data:
        assert all(isinstance(x, str) for x in data)


def test_get_device_returns_full_object(client):
    # create a device via POST with a unique id to avoid conflicts
    payload = {
        "device_id": f"test-api-{uuid.uuid4().hex[:8]}",
        "name": "API Device",
        "location": "Test",
        "model": "X",
        "metadata": {"a": 1},
    }
    token = create_access_token(data={"sub": "admin"})
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/devices", json=payload, headers=headers)
    assert r.status_code in (200, 201)
    created = r.json()
    assert "device_id" in created
    assert created["device_id"] == payload["device_id"]

    # list endpoint should NOT return full dicts; ensure it's a list of ids
    r = client.get("/devices", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)

    # get endpoint should return full object
    r = client.get(f"/devices/{payload['device_id']}", headers=headers)
    assert r.status_code == 200
    obj = r.json()
    assert obj.get("device_id") == payload["device_id"]
    assert obj.get("metadata") == {"a": 1}
