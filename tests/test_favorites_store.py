import tempfile
from app.services.favorites_store import FavoritesStore, MAX_FAVORITES

def test_add_and_list_and_remove():
    with tempfile.TemporaryDirectory() as d:
        path = f"{d}/favorites.json"
        store = FavoritesStore(path)
        store.add("Pune", "IN")
        favs = store.list()
        assert len(favs) == 1
        store.remove("Pune", "IN")
        assert store.list() == []

def test_limit():
    with tempfile.TemporaryDirectory() as d:
        path = f"{d}/favorites.json"
        store = FavoritesStore(path)
        for i in range(MAX_FAVORITES):
            store.add(f"City{i}")
        try:
            store.add("CityX")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == "FAVORITES_LIMIT"