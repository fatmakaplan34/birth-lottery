import asyncio

from fastapi import APIRouter, HTTPException

from app.services.restcountries import get_all_countries
from app.services.worldbank import get_latest_indicator_value
from app.services.wikidata import get_country_inception
from app.services.probability import (
    calculate_population_share,
    calculate_birth_share,
    resolve_country,
)


router = APIRouter(
    prefix="/countries",
    tags=["countries"],
)


async def get_resolved_country(country_identifier: str) -> dict:
    countries = await get_all_countries()

    try:
        return resolve_country(countries, country_identifier)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@router.get("/")
async def list_countries():
    countries = await get_all_countries()

    return {
        "count": len(countries),
        "world_population": sum(
            country["population"] for country in countries
        ),
        "countries": countries,
    }


@router.get("/{country}/profile")
async def get_country_profile(country: str):
    target_country = await get_resolved_country(country)
    founding, population_result = await asyncio.gather(
        get_country_inception(
            target_country["iso3"],
            target_country["name"],
        ),
        get_latest_indicator_value(
            target_country["iso3"],
            "SP.POP.TOTL",
        ),
        return_exceptions=True,
    )

    if isinstance(founding, Exception):
        founding = None
    if isinstance(population_result, Exception):
        population_result = None

    return {
        **target_country,
        "population": (
            round(float(population_result["value"]))
            if population_result
            else target_country["population"]
        ),
        "population_year": (
            population_result["year"]
            if population_result
            else None
        ),
        "founding": founding,
    }


@router.get("/{country}/indicators")
async def get_country_indicators(country: str):
    target_country = await get_resolved_country(country)
    country_iso3 = target_country["iso3"]

    results = await asyncio.gather(
        get_latest_indicator_value(
            country_iso3,
            "NY.GDP.PCAP.CD",
        ),
        get_latest_indicator_value(
            country_iso3,
            "SP.DYN.LE00.IN",
        ),
        get_latest_indicator_value(
            country_iso3,
            "IT.NET.USER.ZS",
        ),
        get_latest_indicator_value(
            country_iso3,
            "SP.URB.TOTL.IN.ZS",
        ),
        get_latest_indicator_value(
            country_iso3,
            "SP.DYN.CBRT.IN",
        ),
    )

    return {
        "country": target_country["name"],
        "iso3": country_iso3,
        "gdp_per_capita": results[0],
        "life_expectancy": results[1],
        "internet_usage": results[2],
        "urban_population": results[3],
        "birth_rate": results[4],
    }


@router.get("/{country}/population_share")
async def get_population_share(country: str):
    try:
        return await calculate_population_share(country)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@router.get("/{country}/birth_share")
async def get_birth_share(country: str):
    try:
        return await calculate_birth_share(country)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error
