from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.weather import router as weather_router
from app.routes.favorites import router as favorites_router

app = FastAPI(title="Weather Dashboard")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(weather_router)
app.include_router(favorites_router)