import csv
import json
from typing import List, Dict, Any
from io import StringIO
from app.models import Device


CSV_HEADER = ["device_id", "name", "location", "model", "metadata_json"]


def devices_to_csv(devices: List[Device]) -> str:
    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(CSV_HEADER)
    for d in devices:
        writer.writerow(
            [
                d.device_id,
                d.name or "",
                d.location or "",
                d.model or "",
                json.dumps(getattr(d, "metadata_", {}) or {}),
            ]
        )
    return out.getvalue()


def csv_to_devices(content: str) -> List[Dict[str, Any]]:
    reader = csv.DictReader(StringIO(content))
    results = []
    for row in reader:
        metadata = {}
        try:
            metadata = json.loads(row.get("metadata_json") or "{}")
        except Exception:
            metadata = {}
        results.append({
            "device_id": row.get("device_id"),
            "name": row.get("name"),
            "location": row.get("location"),
            "model": row.get("model"),
            "metadata": metadata,
        })
    return results
