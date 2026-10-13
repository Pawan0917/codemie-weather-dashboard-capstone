import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    weather_api_mode: str = os.getenv("WEATHER_API_MODE", "live")  # live|mock
    openweather_api_key: str | None = os.getenv("OPENWEATHER_API_KEY")
    weather_api_timeout_seconds: float = float(os.getenv("WEATHER_API_TIMEOUT_SECONDS", "3"))
    favorites_file_path: str = os.getenv("FAVORITES_FILE_PATH", "data/favorites.json")

settings = Settings()