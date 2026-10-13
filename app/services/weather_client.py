import httpx
from typing import List
from app.services.dtos import CurrentWeather, ForecastDay, WeatherBundle

class WeatherClientError(Exception): ...
class CityNotFound(WeatherClientError): ...
class ServiceUnavailable(WeatherClientError): ...
class ConfigError(WeatherClientError): ...

class WeatherClient:
    def __init__(self, api_key: str | None, timeout_seconds: float = 3.0, mode: str = "live"):
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.mode = mode

    def get_weather(self, city: str, unit: str) -> WeatherBundle:
        if self.mode == "mock":
            return self._mock(city, unit)
        if not self.api_key:
            raise ConfigError("Missing OPENWEATHER_API_KEY")

        units_param = "metric" if unit == "C" else "imperial"
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                cur = client.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={"q": city, "appid": self.api_key, "units": units_param},
                )
                if cur.status_code == 404:
                    raise CityNotFound()
                cur.raise_for_status()
                curj = cur.json()

                fc = client.get(
                    "https://api.openweathermap.org/data/2.5/forecast",
                    params={"q": city, "appid": self.api_key, "units": units_param},
                )
                if fc.status_code == 404:
                    raise CityNotFound()
                fc.raise_for_status()
                fcj = fc.json()

            current = CurrentWeather(
                city=curj.get("name", city),
                country=(curj.get("sys") or {}).get("country"),
                temperature=float((curj.get("main") or {}).get("temp")),
                humidity=int((curj.get("main") or {}).get("humidity")),
                wind_speed=float((curj.get("wind") or {}).get("speed")),
                condition=((curj.get("weather") or [{}])[0].get("main") or "Unknown"),
                unit=unit,
            )

            forecast = self._aggregate_5day(fcj, unit)
            return WeatherBundle(current=current, forecast=forecast)

        except (httpx.TimeoutException, httpx.NetworkError):
            raise ServiceUnavailable()
        except httpx.HTTPStatusError:
            raise ServiceUnavailable()

    def _aggregate_5day(self, fcj: dict, unit: str) -> List[ForecastDay]:
        buckets = {}
        for item in fcj.get("list", []):
            dt_txt = item.get("dt_txt", "")
            date = dt_txt.split(" ")[0] if " " in dt_txt else dt_txt[:10]
            main = item.get("main") or {}
            temp_min = main.get("temp_min")
            temp_max = main.get("temp_max")
            cond = ((item.get("weather") or [{}])[0].get("main")) or "Unknown"

            if date not in buckets:
                buckets[date] = {"min": temp_min, "max": temp_max, "cond": cond}
            else:
                buckets[date]["min"] = min(buckets[date]["min"], temp_min)
                buckets[date]["max"] = max(buckets[date]["max"], temp_max)

        days = []
        for date in sorted(buckets.keys())[:5]:
            b = buckets[date]
            days.append(ForecastDay(
                date=date,
                min_temp=float(b["min"]),
                max_temp=float(b["max"]),
                condition=b["cond"],
                unit=unit,
            ))
        return days

    def _mock(self, city: str, unit: str) -> WeatherBundle:
        current = CurrentWeather(
            city=city, country="XX", temperature=25.0, humidity=60, wind_speed=3.5, condition="Clear", unit=unit
        )
        forecast = [
            ForecastDay(date=f"2026-10-{d:02d}", min_temp=20.0, max_temp=28.0, condition="Clouds", unit=unit)
            for d in range(14, 19)
        ]
        return WeatherBundle(current=current, forecast=forecast)