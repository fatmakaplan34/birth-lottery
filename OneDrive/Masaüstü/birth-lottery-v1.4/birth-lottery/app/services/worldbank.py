import httpx

from app.services import cache 

WB_BASE_URL = "https://api.worldbank.org/v2"


async def get_indicator(country_iso3: str, indicator_code: str):
    url = f"{WB_BASE_URL}/country/{country_iso3}/indicator/{indicator_code}"

    cache_key = f"wb_{country_iso3}_{indicator_code}"

    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"format": "json", "per_page": 1000},
                                    timeout=20.0)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or len(data) < 2:
            raise ValueError(
                f"World Bank returned an invalid response for {indicator_code}"
            )

        records = data[1] or []
        timeseries = [
            {"year": int(r["date"]), "value": r["value"]}
            for r in records
        ]

        cache.set(cache_key, timeseries)
        return timeseries

async def get_latest_indicator_value(country_iso3: str, indicator_code: str):
    timeseries = await get_indicator(country_iso3, indicator_code)

    for record in timeseries:
        if record["value"] is not None:
            return record

    return None


async def get_indicator_value_at_or_before(
    country_iso3: str,
    indicator_code: str,
    year: int | None = None,
):
    timeseries = await get_indicator(country_iso3, indicator_code)

    for record in timeseries:
        if record["value"] is None:
            continue

        if year is None or record["year"] <= year:
            return record

    return None


async def get_indicator_values_for_all_countries_by_year(
    indicator_code: str,
    year: int,
):
    cache_key = f"wb_all_{indicator_code}_{year}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return cached_data

    url = f"{WB_BASE_URL}/country/all/indicator/{indicator_code}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "format": "json",
                "date": str(year),
                "per_page": 1000,
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()

    if not isinstance(data, list) or len(data) < 2:
        raise ValueError(
            f"World Bank returned an invalid response for {indicator_code}"
        )

    values = {}

    for record in data[1] or []:
        iso3 = record.get("countryiso3code")
        value = record.get("value")

        if iso3 and value is not None:
            values[iso3] = {
                "year": year,
                "value": value,
            }

    cache.set(cache_key, values)
    return values

async def get_latest_indicator_values_for_all_countries(
    indicator_code: str,
):
    cache_key = f"wb_all_latest_{indicator_code}"

    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return cached_data

    url = (
        f"{WB_BASE_URL}/country/all/"
        f"indicator/{indicator_code}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={
                "format": "json",
                "mrnev": 1,
                "per_page": 1000,
            },
            timeout=20.0,
        )

        response.raise_for_status()
        data = response.json()

    if not isinstance(data, list) or len(data) < 2:
        raise ValueError(
            f"World Bank returned an invalid response for {indicator_code}"
        )

    records = data[1] or []

    latest_values = {}

    for record in records:
        iso3 = record.get("countryiso3code")
        value = record.get("value")
        year = record.get("date")

        if iso3 and value is not None and year:
            latest_values[iso3] = {
                "year": int(year),
                "value": value,
            }

    cache.set(cache_key, latest_values)

    return latest_values
