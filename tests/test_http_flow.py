from fastapi.testclient import TestClient
import app.routes.settings as settings_module
from app.main import app

def test_search_flow_mock_mode():
    # Force mock mode BEFORE calling routes (settings is already imported)
    object.__setattr__(settings_module.settings, "weather_api_mode", "mock")

    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert "Weather Dashboard" in r.text

    r2 = client.post("/weather/search", data={"city": "Pune"})
    assert r2.status_code == 200
    assert "5-day forecast" in r2.text