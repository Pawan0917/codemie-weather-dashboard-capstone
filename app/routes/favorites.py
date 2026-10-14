from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

from app.routes.settings import settings
from app.services.favorites_store import FavoritesStore

router = APIRouter()

@router.post("/favorites/add")
def add_favorite(city: str = Form(...), country: str | None = Form(None)):
    store = FavoritesStore(settings.favorites_file_path)
    try:
        store.add(city, country)
    except ValueError:
        pass
    return RedirectResponse(url="/", status_code=303)

@router.post("/favorites/remove")
def remove_favorite(city: str = Form(...), country: str | None = Form(None)):
    FavoritesStore(settings.favorites_file_path).remove(city, country)
    return RedirectResponse(url="/", status_code=303)