import json
from pathlib import Path

import httpx

from app.config import Settings
from app.models.country import normalize_country
from app.services import cache


API_URL = "https://api.restcountries.com/countries/v5"
SNAPSHOT_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "countries_snapshot.json"
)


def load_country_snapshot() -> list[dict]:
    with SNAPSHOT_PATH.open(encoding="utf-8") as snapshot_file:
        countries = json.load(snapshot_file)

    if not isinstance(countries, list) or not countries:
        raise RuntimeError("Bundled country snapshot is invalid")

    return countries


async def fetch_live_countries() -> list[dict]:
    if not Settings.RC_API_KEY:
        raise RuntimeError("REST Countries API key is not configured")

    offset = 0
    all_objects = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            response = await client.get(
                API_URL,
                headers={"Authorization": f"Bearer {Settings.RC_API_KEY}"},
                params={"limit": 100, "offset": offset},
            )
            response.raise_for_status()
            data = response.json()
            page = data.get("data") or {}
            objects = page.get("objects")

            if not isinstance(objects, list):
                raise ValueError(
                    "REST Countries returned an invalid response"
                )

            all_objects.extend(objects)
            if not (page.get("meta") or {}).get("more"):
                break
            offset += 100

    countries = [
        normalize_country(country)
        for country in all_objects
        if country.get("population", 0) > 0
    ]
    countries.sort(
        key=lambda country: country["population"],
        reverse=True,
    )

    if not countries:
        raise ValueError("REST Countries returned no countries")

    return countries


async def get_all_countries() -> list[dict]:
    """Return country data without making startup depend on an API.

    Snapshot mode is the safe default and makes the globe available
    immediately. Users who explicitly choose the live feed still receive the
    bundled snapshot if that external service is unavailable.
    """

    cached_data = cache.get("all_countries")
    if cached_data is not None:
        return cached_data

    countries = load_country_snapshot()

    if (
        Settings.COUNTRY_DATA_MODE == "live"
        and Settings.RC_API_KEY
    ):
        try:
            countries = await fetch_live_countries()
        except (httpx.HTTPError, ValueError, RuntimeError):
            pass

    cache.set("all_countries", countries)
    return countries
