import httpx

from fastapi import APIRouter, HTTPException,Query

from app.services.lottery import (draw_birth_lottery, build_birth_distribution,)


router = APIRouter(
    prefix="/lottery",
    tags=["lottery"],
)


@router.post("/draw")
async def draw_lottery():
    try:
        return await draw_birth_lottery()

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=503,
            detail="External data service is unavailable",
        ) from error



@router.get("/coverage")
async def get_lottery_coverage():
    try:
        birth_data = await build_birth_distribution()

        return {
            "total_country_count": birth_data[
                "total_country_count"
            ],
            "included_country_count": len(
                birth_data["distribution"]
            ),
            "excluded_country_count": len(
                birth_data["excluded_countries"]
            ),
            "included_population": birth_data[
                "included_population"
            ],
            "excluded_population": birth_data[
                "excluded_population"
            ],
            "total_population": birth_data[
                "total_population"
            ],
            "population_coverage_percentage": birth_data[
                "population_coverage_percentage"
            ],
            "excluded_countries": birth_data[
                "excluded_countries"
            ],
        }

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=503,
            detail="External data service is unavailable",
        ) from error

@router.get("/rankings")
async def get_birth_rankings(
    limit: int = Query(
        default=10,
        ge=1,
        le=252,
    ),
):
    try:
        birth_data = await build_birth_distribution()

        total_births = birth_data[
            "total_estimated_births"
        ]

        sorted_distribution = sorted(
            birth_data["distribution"],
            key=lambda item: item["estimated_births"],
            reverse=True,
        )

        rankings = []

        for rank, item in enumerate(
            sorted_distribution[:limit],
            start=1,
        ):
            country = item["country"]
            estimated_births = item[
                "estimated_births"
            ]

            percentage = (
                estimated_births / total_births
            ) * 100

            rankings.append({
                "rank": rank,
                "country": country["name"],
                "iso3": country["iso3"],
                "flag_emoji": country["flag_emoji"],
                "estimated_annual_births": round(
                    estimated_births
                ),
                "birth_rate_per_1000": item[
                    "birth_rate"
                ],
                "birth_rate_year": item[
                    "birth_rate_year"
                ],
                "percentage": percentage,
                "one_in_x": round(
                    total_births / estimated_births
                ),
            })

        return {
            "limit": limit,
            "total_estimated_births": round(
                total_births
            ),
            "population_coverage_percentage": birth_data[
                "population_coverage_percentage"
            ],
            "rankings": rankings,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=503,
            detail="External data service is unavailable",
        ) from error