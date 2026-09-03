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


# The upstream ``languages`` field mixes official languages with regional or
# commonly spoken languages for some countries. Keep the legally relevant
# country-level values used by the language-odds feature explicit here.
OFFICIAL_LANGUAGE_OVERRIDES = {
    "AUT": ["German"],
    "CHE": ["German", "French", "Italian", "Romansh"],
    "LUX": ["Luxembourgish", "French", "German"],
    "MDV": ["Dhivehi"],
    "NAM": ["English"],
    "NER": ["Hausa"],
}


def apply_country_corrections(country: dict) -> dict:
    corrected = dict(country)
    official_languages = OFFICIAL_LANGUAGE_OVERRIDES.get(
        corrected.get("iso3")
    )
    if official_languages is not None:
        corrected["languages"] = official_languages.copy()
    return corrected


def merge_country_data(
    snapshot_countries: list[dict],
    live_countries: list[dict],
) -> list[dict]:
    """Enrich the complete snapshot without letting a partial feed delete rows."""

    live_by_iso3 = {
        country.get("iso3"): country
        for country in live_countries
        if country.get("iso3")
    }
    snapshot_ids = {
        country.get("iso3")
        for country in snapshot_countries
        if country.get("iso3")
    }
    merged = []

    for snapshot_country in snapshot_countries:
        combined = dict(snapshot_country)
        live_country = live_by_iso3.get(snapshot_country.get("iso3"))
        if live_country:
            combined.update({
                key: value
                for key, value in live_country.items()
                if value not in (None, "", [], {})
            })
        merged.append(apply_country_corrections(combined))

    for live_country in live_countries:
        if live_country.get("iso3") not in snapshot_ids:
            merged.append(apply_country_corrections(live_country))

    merged.sort(
        key=lambda country: country.get("population", 0),
        reverse=True,
    )
    return merged


def load_country_snapshot() -> list[dict]:
    with SNAPSHOT_PATH.open(encoding="utf-8") as snapshot_file:
        countries = json.load(snapshot_file)

    if not isinstance(countries, list) or not countries:
        raise RuntimeError("Bundled country snapshot is invalid")

    return [apply_country_corrections(country) for country in countries]


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
        apply_country_corrections(normalize_country(country))
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
            live_countries = await fetch_live_countries()
            countries = merge_country_data(countries, live_countries)
        except (httpx.HTTPError, ValueError, RuntimeError):
            pass

    cache.set("all_countries", countries)
    return countries
