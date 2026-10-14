from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CurrentWeather:
    city: str
    country: Optional[str]
    temperature: float
    humidity: int
    wind_speed: float
    condition: str
    unit: str  # C|F

@dataclass
class ForecastDay:
    date: str
    min_temp: float
    max_temp: float
    condition: str
    unit: str

@dataclass
class WeatherBundle:
    current: CurrentWeather
    forecast: List[ForecastDay]