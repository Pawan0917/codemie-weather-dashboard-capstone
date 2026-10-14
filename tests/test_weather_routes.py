from fastapi.testclient import TestClient
from app.main import app

def test_home_page_loads():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Weather Dashboard" in r.text