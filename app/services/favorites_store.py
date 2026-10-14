import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any

MAX_FAVORITES = 5

class FavoritesStore:
    def __init__(self, path: str):
        self.path = path

    def _ensure_file(self) -> None:
        folder = os.path.dirname(self.path) or "."
        os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"favorites": []}, f)

    def list(self) -> List[Dict[str, Any]]:
        self._ensure_file()
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("favorites", [])

    def add(self, city: str, country: str | None = None) -> None:
        self._ensure_file()
        favs = self.list()

        key = (city.strip().lower(), (country or "").strip().lower())
        exists = any((x["city"].strip().lower(), (x.get("country") or "").strip().lower()) == key for x in favs)
        if exists:
            return

        if len(favs) >= MAX_FAVORITES:
            raise ValueError("FAVORITES_LIMIT")

        favs.append({
            "city": city.strip(),
            "country": country,
            "added_at": datetime.now(timezone.utc).isoformat()
        })
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"favorites": favs}, f, indent=2)

    def remove(self, city: str, country: str | None = None) -> None:
        self._ensure_file()
        favs = self.list()
        key = (city.strip().lower(), (country or "").strip().lower())
        favs2 = [x for x in favs if (x["city"].strip().lower(), (x.get("country") or "").strip().lower()) != key]
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"favorites": favs2}, f, indent=2)