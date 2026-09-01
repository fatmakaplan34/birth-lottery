from datetime import date

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.services.odds import (
    get_birth_odds,
    get_language_birth_odds,
    get_living_standards_comparison,
)


router = APIRouter(prefix="/odds", tags=["odds"])


def external_data_error(error: Exception):
    if isinstance(error, ValueError):
        return HTTPException(status_code=422, detail=str(error))
    return HTTPException(
        status_code=503,
        detail="External data service is unavailable",
    )


@router.get("/birth")
async def birth_odds(
    country: str,
    birth_date: date,
    city: str | None = None,
):
    try:
        return await get_birth_odds(country, birth_date, city)
    except (ValueError, httpx.HTTPError) as error:
        raise external_data_error(error) from error


@router.get("/language")
async def language_birth_odds(
    language: str,
    year: int = Query(default=date.today().year, ge=1960, le=date.today().year),
):
    try:
        return await get_language_birth_odds(language, year)
    except (ValueError, httpx.HTTPError) as error:
        raise external_data_error(error) from error


@router.get("/living-standards")
async def living_standards(
    country1: str,
    country2: str,
    year: int = Query(default=date.today().year, ge=1960, le=date.today().year),
):
    try:
        return await get_living_standards_comparison(country1, country2, year)
    except (ValueError, httpx.HTTPError) as error:
        raise external_data_error(error) from error
