from pathlib import Path


def test_csv_import_export(client, admin_token, tmp_path):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # prepare CSV
    csv_content = (
        "device_id,name,location,model,metadata_json\n"
        '{"device_id":"ci1","name":"CI-1"}\n'
    )
    # more explicit valid CSV row
    csv_content = 'device_id,name,location,model,metadata_json\nci1,CI-1,Lab,ModelZ,{"firmware":"v1"}\n'
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

    # export to path
    out_path = tmp_path / "out.csv"
    r = client.get(f"/devices/csv?path={out_path}", headers=headers)
    assert r.status_code == 200
    assert out_path.exists()
