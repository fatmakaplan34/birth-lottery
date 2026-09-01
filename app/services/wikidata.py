import json
from pathlib import Path
import unicodedata

import httpx

from app.services import cache


WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"
WIKIDATA_ACTION_API_URL = "https://www.wikidata.org/w/api.php"
USER_AGENT = (
    "BirthLottery/1.2 "
    "(educational country profile application; Wikidata read-only client)"
)
LOCAL_DATES_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "country_dates.json"
)


def _load_local_dates() -> dict:
    try:
        return json.loads(LOCAL_DATES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


LOCAL_COUNTRY_DATES = _load_local_dates()


def _country_date_key(iso3: str, country_name: str | None) -> str:
    if iso3:
        return iso3
    normalized_name = "".join(
        character
        for character in unicodedata.normalize(
            "NFKD",
            (country_name or "").strip().casefold(),
        )
        if not unicodedata.combining(character)
    )
    return f"NAME:{normalized_name.upper()}"


def _result(
    date: str | None,
    source: str,
    definition: str,
    event: dict | None = None,
    source_url: str | None = None,
    precision: int | None = None,
) -> dict:
    return {
        "date": date,
        "precision": precision,
        "event": event,
        "source": source,
        "source_url": source_url,
        "definition": definition,
    }


def _wikidata_result(date: str | None) -> dict:
    return _result(
        date=date,
        event=(
            {
                "tr": "Modern devlet başlangıcı",
                "en": "Modern-state inception",
            }
            if date
            else None
        ),
        source="Wikidata P571",
        source_url="https://www.wikidata.org/wiki/Property:P571",
        precision=11 if date else None,
        definition=(
            "Latest available inception date for the modern country entity"
        ),
    )


def _extract_sparql_date(payload: dict) -> str | None:
    try:
        bindings = payload["results"]["bindings"]
        return bindings[0]["inception"]["value"][:10] if bindings else None
    except (KeyError, IndexError, TypeError):
        return None


def _claim_values(entity: dict, property_id: str) -> list:
    values = []
    for claim in entity.get("claims", {}).get(property_id, []):
        try:
            values.append(claim["mainsnak"]["datavalue"]["value"])
        except (KeyError, TypeError):
            continue
    return values


def _extract_action_api_date(payload: dict, iso3: str) -> str | None:
    dates = []
    for entity in payload.get("entities", {}).values():
        iso_values = _claim_values(entity, "P298")
        if iso3 not in iso_values:
            continue
        for value in _claim_values(entity, "P571"):
            if isinstance(value, dict) and value.get("time"):
                dates.append(value["time"].lstrip("+")[:10])
    return max(dates) if dates else None


async def _get_date_from_sparql(
    client: httpx.AsyncClient,
    iso3: str,
) -> str | None:
    query = f'''SELECT ?inception WHERE {{
      ?country wdt:P298 "{iso3}".
      ?country wdt:P571 ?inception.
    }} ORDER BY DESC(?inception) LIMIT 1'''
    response = await client.post(
        WIKIDATA_SPARQL_URL,
        data={"query": query, "format": "json"},
    )
    response.raise_for_status()
    return _extract_sparql_date(response.json())


async def _get_date_from_action_api(
    client: httpx.AsyncClient,
    iso3: str,
    country_name: str,
) -> str | None:
    search_response = await client.get(
        WIKIDATA_ACTION_API_URL,
        params={
            "action": "wbsearchentities",
            "search": country_name,
            "language": "en",
            "type": "item",
            "limit": 10,
            "format": "json",
        },
    )
    search_response.raise_for_status()
    entity_ids = [
        item["id"]
        for item in search_response.json().get("search", [])
        if item.get("id")
    ]
    if not entity_ids:
        return None

    entity_response = await client.get(
        WIKIDATA_ACTION_API_URL,
        params={
            "action": "wbgetentities",
            "ids": "|".join(entity_ids),
            "props": "claims",
            "format": "json",
        },
    )
    entity_response.raise_for_status()
    return _extract_action_api_date(entity_response.json(), iso3)


async def get_country_inception(
    iso3: str,
    country_name: str | None = None,
) -> dict:
    normalized_iso3 = iso3.strip().upper()
    local_record = LOCAL_COUNTRY_DATES.get(
        _country_date_key(normalized_iso3, country_name)
    )
    if local_record:
        return local_record

    cache_key = f"wikidata_inception_v2_{normalized_iso3}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    date = None
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": USER_AGENT,
    }
    async with httpx.AsyncClient(headers=headers, timeout=15.0) as client:
        try:
            date = await _get_date_from_sparql(client, normalized_iso3)
        except (httpx.HTTPError, TypeError, ValueError):
            date = None

        if not date and country_name:
            try:
                date = await _get_date_from_action_api(
                    client,
                    normalized_iso3,
                    country_name,
                )
            except (httpx.HTTPError, TypeError, ValueError):
                date = None

    result = _wikidata_result(date)
    # A transient upstream failure must not turn into a cached missing date.
    if date:
        cache.set(cache_key, result)
    return result
