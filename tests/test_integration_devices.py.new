import uuid


def test_devices_crud(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # create with unique id
    did = f"d{uuid.uuid4().hex[:8]}"
    payload = {"device_id": did, "name": "Device100"}
    r = client.post("/devices", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["device_id"] == did

    # read
    r = client.get(f"/devices/{did}", headers=headers)
    assert r.status_code == 200

    # update
    payload = {"device_id": did, "name": "Device100-updated"}
    r = client.put(f"/devices/{did}", json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Device100-updated"

    # delete
    r = client.delete(f"/devices/{did}", headers=headers)
    assert r.status_code == 204


def test_list_devices_requires_auth(client):
    r = client.get("/devices")
    assert r.status_code in (401, 422)
