import os
from fastapi.testclient import TestClient
from app.main import app

def test_search_flow_mock_mode():
    # Ensure mock mode for deterministic test
    os.environ["WEATHER_API_MODE"] = "mock"

    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert "Weather Dashboard" in r.text

    r2 = client.post("/weather/search", data={"city": "Pune"})
    assert r2.status_code == 200
    assert "5-day forecast" in r2.text