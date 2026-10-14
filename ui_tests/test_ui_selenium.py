import os
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions


def start_app():
    env = os.environ.copy()
    env["WEATHER_API_MODE"] = "mock"
    p = subprocess.Popen(
        ["python", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(2)
    return p


def stop_app(p):
    if p:
        p.terminate()


def test_search_city_shows_forecast():
    p = None
    driver = None
    try:
        p = start_app()

        options = EdgeOptions()
        # options.add_argument("--headless=new")  # enable later if needed
        options.add_argument("--window-size=1280,800")

        driver = webdriver.Edge(options=options)

        driver.get("http://127.0.0.1:8000/")
        driver.find_element(By.NAME, "city").send_keys("Pune")
        driver.find_element(By.XPATH, "//button[contains(.,'Search')]").click()
        time.sleep(1)

        assert "5-day forecast" in driver.page_source
    finally:
        if driver:
            driver.quit()
        stop_app(p)