# Test Plan - Weather Dashboard Capstone

## Gherkin Scenarios
Location: docs/gherkin/weather_dashboard.feature

## Automated UI Tests
Tool: Selenium (Python)
Test location: ui_tests/test_ui_selenium.py

## How to execute (Windows)
```powershell
$env:WEATHER_API_MODE="mock"
python -m pytest -q tests\test_http_flow.py | Tee-Object -FilePath ui-test-output.txt   

Note on Browser UI Execution (Restricted Environment)
Selenium UI automation script is provided at ui_tests/test_ui_selenium.py.
However, browser driver resolution (Chrome/Edge WebDriver) was blocked/unsupported in the current restricted Windows environment.Therefore, automated execution evidence is produced using HTTP-level automation via FastAPI TestClient (tests/test_http_flow.py),and manual UI screenshots are captured for the demo.