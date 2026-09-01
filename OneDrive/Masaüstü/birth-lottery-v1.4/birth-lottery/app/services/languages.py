from app.services.restcountries import get_all_countries
from app.services.probability import calculate_share
from app.services.language_catalog import resolve_language_countries


async def get_language_data(language_name: str):
    countries = await get_all_countries()
    canonical_language_name, countries_with_language = (
        resolve_language_countries(countries, language_name)
    )

    covered_population = sum(
        country.get("population", 0)
        for country in countries_with_language
    )

    world_population = sum(
        country["population"]
        for country in countries
    )

    share = calculate_share(
        covered_population,
        world_population,
    )

    return {
        "language": canonical_language_name,
        "metric": (
            "Population living in countries where "
            "the language is officially recognized"
        ),
        "important_note": (
            "This does not represent the number or "
            "percentage of people who speak the language."
        ),
        "population_in_countries_where_official": (
            covered_population
        ),
        "world_population": world_population,
        "percentage_of_world_population_living_in_those_countries": (
            share["percentage"]
        ),
        "country_count": len(
            countries_with_language
        ),
        "countries": [
            {
                "name": country["name"],
                "iso3": country["iso3"],
                "flag_emoji": country["flag_emoji"],
                "population": country["population"],
            }
            for country in countries_with_language
        ],
    }
