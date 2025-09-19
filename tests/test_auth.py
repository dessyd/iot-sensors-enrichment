import sys
from pathlib import Path
from fastapi.testclient import TestClient

# ensure project root in path for imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import app


client = TestClient(app)


def test_token_missing_credentials() -> None:
    r = client.post("/auth/token", data={})
    assert r.status_code == 422
