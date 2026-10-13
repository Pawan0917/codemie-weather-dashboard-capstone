from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.routes.settings import settings
from app.services.weather_client import WeatherClient, CityNotFound, ServiceUnavailable, ConfigError
from app.services.favorites_store import FavoritesStore

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def _get_unit(request: Request) -> str:
    unit = request.cookies.get("unit", "C")
    return unit if unit in ("C", "F") else "C"

@router.get("/")
def home(request: Request):
    unit = _get_unit(request)
    favs = FavoritesStore(settings.favorites_file_path).list()
    return templates.TemplateResponse("index.html", {"request": request, "unit": unit, "favorites": favs})

@router.post("/unit")
def set_unit(unit: str = Form(...)):
    unit = unit if unit in ("C", "F") else "C"
    resp = RedirectResponse(url="/", status_code=303)
    resp.set_cookie("unit", unit, httponly=False)
    return resp

@router.post("/weather/search")
def search(request: Request, city: str = Form(...)):
    city = (city or "").strip()
    unit = _get_unit(request)
    favs = FavoritesStore(settings.favorites_file_path).list()

    if not city:
        return templates.TemplateResponse("index.html", {
            "request": request, "unit": unit, "favorites": favs, "error": "Please enter a city."
        })

    client = WeatherClient(
        api_key=settings.openweather_api_key,
        timeout_seconds=settings.weather_api_timeout_seconds,
        mode=settings.weather_api_mode,
    )

    try:
        bundle = client.get_weather(city, unit)
        return templates.TemplateResponse("results.html", {
            "request": request, "unit": unit, "bundle": bundle
        })
    except CityNotFound:
        return templates.TemplateResponse("index.html", {
            "request": request, "unit": unit, "favorites": favs,
            "error": "City not found. Check spelling."
        })
    except ConfigError:
        return templates.TemplateResponse("index.html", {
            "request": request, "unit": unit, "favorites": favs,
            "error": "Service configuration error."
        })
    except ServiceUnavailable:
        return templates.TemplateResponse("index.html", {
            "request": request, "unit": unit, "favorites": favs,
            "error": "Weather service unavailable, try again."
        })