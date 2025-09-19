def test_get_devices_csv_inline(client, admin_token, tmp_path):
    """Import one device, then GET /devices/csv without path and assert CSV content is returned."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    csv_content = 'device_id,name,location,model,metadata_json\nciX,CSV-Device,LabX,ModelX,{"fw":"1.0"}\n'
    p = tmp_path / "to_import.csv"
    p.write_text(csv_content, encoding="utf-8")

    with open(p, "rb") as fh:
        r = client.post(
            "/devices/csv",
            files={"file": ("to_import.csv", fh)},
            headers=headers,
        )
    assert r.status_code == 201
    body = r.json()
    assert body.get("created", 0) >= 1

    # GET inline CSV
    r = client.get("/devices/csv", headers=headers)
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("text/csv")
    text = r.content.decode("utf-8")
    assert "device_id,name,location,model,metadata_json" in text
    assert "ciX" in text
