import sys
from pathlib import Path
from fastapi.testclient import TestClient

# ensure project root in path for imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import app


client = TestClient(app)


def test_list_devices_unauthenticated() -> None:
    r = client.get("/devices")
    assert r.status_code in (401, 422)
