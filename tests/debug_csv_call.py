from pathlib import Path
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

with open('tests/test_integration_csv.py') as f:
    print('test file exists')

print('ready')
