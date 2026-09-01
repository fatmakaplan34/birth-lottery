from fastapi import APIRouter, HTTPException
from app.services.probability import calculate_population_share, calculate_birth_share
from app.services.worldbank import get_latest_indicator_value
import asyncio

router = APIRouter(tags=["compare"])

@router.get("/compare")
async def compare_countries(country1: str, country2: str):
    try:
        results = await asyncio.gather(
            calculate_population_share(country1),
            calculate_birth_share(country1),
            calculate_population_share(country2),
            calculate_birth_share(country2),
        )

        return {
            "country1": {
                "population_share": results[0],
                "birth_share": results[1],
            },
            "country2": {
                "population_share": results[2],
                "birth_share": results[3],
            },
        }

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error