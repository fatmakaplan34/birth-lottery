import asyncio
import random

from app.services.restcountries import get_all_countries
from app.services.worldbank import (
    get_latest_indicator_values_for_all_countries,
)


BIRTH_RATE_INDICATOR = "SP.DYN.CBRT.IN"
POPULATION_INDICATOR = "SP.POP.TOTL"


async def build_birth_distribution():
    countries, populations, birth_rates = await asyncio.gather(
        get_all_countries(),
        get_latest_indicator_values_for_all_countries(
            POPULATION_INDICATOR,
        ),
        get_latest_indicator_values_for_all_countries(
            BIRTH_RATE_INDICATOR,
        ),
    )

    distribution = []
    excluded_countries = []

    for country in countries:
        iso3 = country["iso3"]
        population_record = populations.get(iso3)
        population = (
            float(population_record["value"])
            if population_record
            else float(country["population"])
        )
        birth_rate_record = birth_rates.get(iso3)

        if not birth_rate_record:
            excluded_countries.append({
                "name": country["name"],
                "iso3": iso3,
                "population": population,
                "reason": "Birth rate data not available",
            })
            continue

        birth_rate = float(birth_rate_record["value"])

        estimated_births = (
            population * birth_rate
        ) / 1000

        if estimated_births <= 0:
            excluded_countries.append({
                "name": country["name"],
                "iso3": iso3,
                "population": population,
                "reason": "Estimated births are zero",
            })
            continue

        distribution.append({
            "country": {
                **country,
                "population": round(population),
            },
            "population_year": (
                population_record["year"]
                if population_record
                else None
            ),
            "birth_rate": birth_rate,
            "birth_rate_year": birth_rate_record["year"],
            "estimated_births": estimated_births,
        })

    total_estimated_births = sum(
        item["estimated_births"]
        for item in distribution
    )

    if not distribution or total_estimated_births <= 0:
        raise ValueError(
            "Birth distribution could not be calculated"
        )

    included_population = sum(
        item["country"]["population"]
        for item in distribution
    )

    excluded_population = sum(
        country["population"]
        for country in excluded_countries
    )

    total_population = (
        included_population + excluded_population
    )

    population_coverage_percentage = (
        included_population / total_population
    ) * 100

    return {
        "distribution": distribution,
        "total_estimated_births": total_estimated_births,
        "excluded_countries": excluded_countries,
        "total_country_count": len(countries),
        "included_population": included_population,
        "excluded_population": excluded_population,
        "total_population": total_population,
        "population_coverage_percentage": (
            population_coverage_percentage
        ),
    }


async def draw_birth_lottery():
    birth_data = await build_birth_distribution()

    distribution = birth_data["distribution"]

    selected = random.choices(
        population=distribution,
        weights=[
            item["estimated_births"]
            for item in distribution
        ],
        k=1,
    )[0]

    country = selected["country"]
    estimated_births = selected["estimated_births"]
    total_births = birth_data["total_estimated_births"]

    probability_percentage = (
        estimated_births / total_births
    ) * 100

    one_in_x = round(
        total_births / estimated_births
    )

    return {
        "result": {
            "country": country["name"],
            "country_tr": country.get("name_tr", country["name"]),
            "official_name": country["official_name"],
            "official_name_tr": country.get(
                "official_name_tr",
                country["official_name"],
            ),
            "iso2": country["iso2"],
            "iso3": country["iso3"],
            "flag_emoji": country["flag_emoji"],
            "flag_svg": country["flag_svg"],
            "region": country["region"],
            "subregion": country["subregion"],
            "capital": country["capital"],
            "languages": country["languages"],
            "population": country["population"],
            "calling_codes": country.get("calling_codes", []),
            "continents": country.get("continents", [country["region"]]),
        },
        "birth_probability": {
            "birth_rate_per_1000": selected["birth_rate"],
            "birth_rate_year": selected["birth_rate_year"],
            "estimated_annual_births": round(
                estimated_births
            ),
            "percentage": probability_percentage,
            "one_in_x": one_in_x,
        },
        "dataset": {
            "basis": (
                "Population multiplied by the latest "
                "available crude birth rate"
            ),
            "total_estimated_births": round(total_births),
            "included_country_count": len(distribution),
            "excluded_country_count": len(
                birth_data["excluded_countries"]
            ),
            "total_country_count": birth_data[
                "total_country_count"
            ],
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
        },
    }
