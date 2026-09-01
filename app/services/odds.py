import asyncio
from datetime import date

from app.services.lottery import build_birth_distribution
from app.services.language_catalog import resolve_language_countries
from app.services.probability import calculate_share, resolve_country
from app.services.restcountries import get_all_countries
from app.services.worldbank import (
    get_indicator_value_at_or_before,
    get_indicator_values_for_all_countries_by_year,
)


BIRTH_RATE_INDICATOR = "SP.DYN.CBRT.IN"
POPULATION_INDICATOR = "SP.POP.TOTL"


async def build_historical_birth_distribution(year: int):
    countries, populations, birth_rates = await asyncio.gather(
        get_all_countries(),
        get_indicator_values_for_all_countries_by_year(
            POPULATION_INDICATOR,
            year,
        ),
        get_indicator_values_for_all_countries_by_year(
            BIRTH_RATE_INDICATOR,
            year,
        ),
    )

    distribution = []
    excluded_countries = []
    population_with_data = 0

    for country in countries:
        iso3 = country["iso3"]
        population_record = populations.get(iso3)
        birth_rate_record = birth_rates.get(iso3)

        if population_record:
            population_with_data += float(population_record["value"])

        if not population_record or not birth_rate_record:
            missing = []
            if not population_record:
                missing.append("population")
            if not birth_rate_record:
                missing.append("birth rate")

            excluded_countries.append({
                "name": country["name"],
                "iso3": iso3,
                "reason": f"No {' or '.join(missing)} data for {year}",
            })
            continue

        population = float(population_record["value"])
        birth_rate = float(birth_rate_record["value"])
        estimated_births = population * birth_rate / 1000

        if estimated_births <= 0:
            continue

        distribution.append({
            "country": country,
            "population": population,
            "population_year": year,
            "birth_rate": birth_rate,
            "birth_rate_year": year,
            "estimated_births": estimated_births,
        })

    total_births = sum(item["estimated_births"] for item in distribution)
    included_population = sum(item["population"] for item in distribution)

    if not distribution or total_births <= 0:
        raise ValueError(f"Birth probability could not be calculated for {year}")

    coverage = (
        included_population / population_with_data * 100
        if population_with_data > 0
        else 0
    )

    return {
        "distribution": distribution,
        "total_estimated_births": total_births,
        "excluded_countries": excluded_countries,
        "total_country_count": len(countries),
        "population_coverage_percentage": coverage,
        "data_year": year,
        "calculation_mode": "historical_observation",
        "basis": (
            "Same-year World Bank population multiplied by the same-year "
            "crude birth rate"
        ),
    }


async def get_distribution_for_year(requested_year: int):
    current_year = date.today().year

    if requested_year >= current_year - 1:
        latest = await build_birth_distribution()
        return {
            **latest,
            "data_year": None,
            "calculation_mode": "latest_available_estimate",
            "basis": (
                "Latest country population multiplied by each country's "
                "latest available crude birth rate"
            ),
        }

    return await build_historical_birth_distribution(requested_year)


async def get_birth_odds(
    country_identifier: str,
    birth_date: date,
    city: str | None = None,
):
    countries = await get_all_countries()
    country = resolve_country(countries, country_identifier)
    birth_data = await get_distribution_for_year(birth_date.year)

    selected = next(
        (
            item
            for item in birth_data["distribution"]
            if item["country"]["iso3"] == country["iso3"]
        ),
        None,
    )

    if not selected:
        raise ValueError(
            f"Birth data is not available for {country['name']} in {birth_date.year}"
        )

    sorted_distribution = sorted(
        birth_data["distribution"],
        key=lambda item: item["estimated_births"],
        reverse=True,
    )
    rank = next(
        index
        for index, item in enumerate(sorted_distribution, start=1)
        if item["country"]["iso3"] == country["iso3"]
    )

    total_births = birth_data["total_estimated_births"]
    share = calculate_share(selected["estimated_births"], total_births)

    return {
        "query": {
            "birth_date": birth_date.isoformat(),
            "year_used_for_probability": birth_date.year,
            "city": city.strip() if city else None,
            "country_input": country_identifier,
        },
        "country": {
            "name": country["name"],
            "name_tr": country.get("name_tr", country["name"]),
            "official_name": country["official_name"],
            "official_name_tr": country.get(
                "official_name_tr",
                country["official_name"],
            ),
            "iso2": country["iso2"],
            "iso3": country["iso3"],
            "flag_emoji": country["flag_emoji"],
            "capital": country["capital"],
            "region": country["region"],
        },
        "probability": {
            "percentage": share["percentage"],
            "one_in_x": share["one_in_x"],
            "rank": rank,
            "ranked_country_count": len(sorted_distribution),
            "estimated_births": round(selected["estimated_births"]),
            "total_estimated_births": round(total_births),
        },
        "source_values": {
            "population": round(
                selected.get("population", selected["country"]["population"])
            ),
            "population_year": selected.get("population_year"),
            "birth_rate_per_1000": selected["birth_rate"],
            "birth_rate_year": selected["birth_rate_year"],
        },
        "methodology": {
            "calculation_mode": birth_data["calculation_mode"],
            "basis": birth_data["basis"],
            "population_coverage_percentage": birth_data[
                "population_coverage_percentage"
            ],
            "date_note": (
                "The full date personalizes the result, but annual source data "
                "means the year determines the probability."
            ),
            "city_note": (
                "City is shown as context only; this dataset calculates at "
                "country level."
                if city
                else None
            ),
        },
    }


async def get_language_birth_odds(language_name: str, year: int):
    countries = await get_all_countries()
    canonical_name, language_countries = resolve_language_countries(
        countries,
        language_name,
    )
    official_country_ids = {
        country["iso3"] for country in language_countries
    }

    birth_data = await get_distribution_for_year(year)
    matching = [
        item
        for item in birth_data["distribution"]
        if item["country"]["iso3"] in official_country_ids
    ]
    language_births = sum(item["estimated_births"] for item in matching)

    rankings = []
    for rank, item in enumerate(
        sorted(matching, key=lambda value: value["estimated_births"], reverse=True),
        start=1,
    ):
        share = calculate_share(item["estimated_births"], language_births)
        global_share = calculate_share(
            item["estimated_births"],
            birth_data["total_estimated_births"],
        )
        country = item["country"]
        rankings.append({
            "rank": rank,
            "country": country["name"],
            "country_tr": country.get("name_tr", country["name"]),
            "iso3": country["iso3"],
            "flag_emoji": country["flag_emoji"],
            "estimated_births": round(item["estimated_births"]),
            "conditional_percentage": share["percentage"],
            "conditional_one_in_x": share["one_in_x"],
            "global_percentage": global_share["percentage"],
            "data_available": True,
        })

    included_ids = {item["iso3"] for item in rankings}
    missing_data_countries = [
        country
        for country in language_countries
        if country["iso3"] not in included_ids
    ]

    for country in sorted(
        missing_data_countries,
        key=lambda item: item["name"],
    ):
        rankings.append({
            "rank": None,
            "country": country["name"],
            "country_tr": country.get("name_tr", country["name"]),
            "iso3": country["iso3"],
            "flag_emoji": country["flag_emoji"],
            "estimated_births": None,
            "conditional_percentage": None,
            "conditional_one_in_x": None,
            "global_percentage": None,
            "data_available": False,
        })

    return {
        "language": canonical_name,
        "requested_year": year,
        "metric": (
            "Birth distribution among countries where the language is "
            "officially recognized"
        ),
        "important_note": (
            "This is not the probability for an individual speaker and does "
            "not estimate how many people speak the language."
        ),
        "calculation_mode": birth_data["calculation_mode"],
        "country_count": len(language_countries),
        "included_country_count": len(matching),
        "excluded_country_count": len(missing_data_countries),
        "estimated_births_in_language_countries": round(language_births),
        "countries": rankings,
    }


LIVING_STANDARD_INDICATORS = {
    "gdp_per_capita": ("NY.GDP.PCAP.CD", "Current US$", True),
    "life_expectancy": ("SP.DYN.LE00.IN", "Years", True),
    "internet_usage": ("IT.NET.USER.ZS", "% of population", True),
    "urban_population": ("SP.URB.TOTL.IN.ZS", "% of population", None),
    "infant_mortality": ("SP.DYN.IMRT.IN", "Per 1,000 live births", False),
    "birth_rate": ("SP.DYN.CBRT.IN", "Per 1,000 people", None),
}


async def get_living_standards_comparison(
    country1_identifier: str,
    country2_identifier: str,
    year: int,
):
    countries = await get_all_countries()
    country1 = resolve_country(countries, country1_identifier)
    country2 = resolve_country(countries, country2_identifier)

    requests = [
        get_indicator_value_at_or_before(country["iso3"], code, year)
        for country in (country1, country2)
        for code, _, _ in LIVING_STANDARD_INDICATORS.values()
    ]
    values = await asyncio.gather(*requests)
    metric_names = list(LIVING_STANDARD_INDICATORS)

    def build_country_result(country: dict, offset: int):
        return {
            "country": country["name"],
            "country_tr": country.get("name_tr", country["name"]),
            "iso3": country["iso3"],
            "flag_emoji": country["flag_emoji"],
            "metrics": {
                name: values[offset + index]
                for index, name in enumerate(metric_names)
            },
        }

    return {
        "requested_year": year,
        "data_note": (
            "Each metric uses the closest available observation at or before "
            "the requested year; the returned year is shown per value."
        ),
        "metric_definitions": {
            name: {
                "unit": unit,
                "higher_is_generally_better": higher_is_better,
            }
            for name, (_, unit, higher_is_better) in LIVING_STANDARD_INDICATORS.items()
        },
        "country1": build_country_result(country1, 0),
        "country2": build_country_result(country2, len(metric_names)),
    }
