def test_admin_can_get_token(client):
    r = client.post(
        "/auth/token",
        data={"username": "admin", "password": "testadmin"}
    )
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body


def test_bad_credentials(client):
    r = client.post(
        "/auth/token",
        data={"username": "admin", "password": "wrong"}
    )
    assert r.status_code == 401
