from app.services.restcountries import get_all_countries
from app.services.worldbank import get_latest_indicator_value
from app.services.lottery import build_birth_distribution

def resolve_country(countries: list[dict], identifier: str) -> dict:
    search_value = identifier.strip().casefold()

    exact_matches = []

    for country in countries:
        searchable_values = {
            str(country.get("name", "")).strip().casefold(),
            str(country.get("official_name", "")).strip().casefold(),
            str(country.get("iso2", "")).strip().casefold(),
            str(country.get("iso3", "")).strip().casefold(),
        }

        if search_value in searchable_values:
            exact_matches.append(country)

    if len(exact_matches) == 1:
        return exact_matches[0]

    partial_matches = []

    for country in countries:
        country_name = str(country.get("name", "")).casefold()
        official_name = str(country.get("official_name", "")).casefold()

        if search_value in country_name or search_value in official_name:
            partial_matches.append(country)

    if len(partial_matches) == 1:
        return partial_matches[0]

    if len(partial_matches) > 1:
        options = ", ".join(
            f'{country["name"]} ({country["iso3"]})'
            for country in partial_matches
        )

        raise ValueError(
            f"Country name is ambiguous. Possible countries: {options}"
        )

    raise ValueError(f"Country not found: {identifier}")


def calculate_share(group_population: float, world_population: float):
    percentage = (group_population / world_population) * 100
    one_in_x = round(world_population / group_population)

    return {
        "percentage": percentage,
        "one_in_x": one_in_x,
    }


async def calculate_population_share(country_identifier: str):
    countries = await get_all_countries()
    target_country = resolve_country(countries, country_identifier)

    world_population = sum(
        country["population"] for country in countries
    )

    share = calculate_share(
        target_country["population"],
        world_population,
    )

    return {
        "country": target_country["name"],
        "iso3": target_country["iso3"],
        "population": target_country["population"],
        "world_population": world_population,
        "percentage": share["percentage"],
        "one_in_x": share["one_in_x"],
    }


async def calculate_birth_share(country_identifier: str):
    countries = await get_all_countries()

    target_country = resolve_country(
        countries,
        country_identifier,
    )

    birth_data = await build_birth_distribution()

    target_birth_data = next(
        (
            item
            for item in birth_data["distribution"]
            if item["country"]["iso3"]
            == target_country["iso3"]
        ),
        None,
    )

    if not target_birth_data:
        raise ValueError(
            "Birth rate data is not available for "
            f'{target_country["name"]}'
        )

    country_births = target_birth_data[
        "estimated_births"
    ]

    total_births = birth_data[
        "total_estimated_births"
    ]

    share = calculate_share(
        country_births,
        total_births,
    )

    return {
        "country": target_country["name"],
        "iso3": target_country["iso3"],
        "birth_rate_per_1000": target_birth_data[
            "birth_rate"
        ],
        "birth_rate_year": target_birth_data[
            "birth_rate_year"
        ],
        "estimated_births": round(country_births),
        "total_estimated_births": round(total_births),
        "percentage": share["percentage"],
        "one_in_x": share["one_in_x"],
        "population_coverage_percentage": birth_data[
            "population_coverage_percentage"
        ],
    }