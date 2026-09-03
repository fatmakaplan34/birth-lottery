import unicodedata


TURKISH_LANGUAGE_ALIASES = {
    "almanca": "German",
    "arnavutca": "Albanian",
    "arapca": "Arabic",
    "bengalce": "Bengali",
    "berberice": "Tamazight / Amazigh",
    "bosnakca": "Bosnian",
    "bulgarca": "Bulgarian",
    "cekce": "Czech",
    "cince": "Chinese",
    "danca": "Danish",
    "dhivehi": "Dhivehi",
    "divehi": "Dhivehi",
    "divehice": "Dhivehi",
    "endonezce": "Indonesian",
    "ermenice": "Armenian",
    "farsca": "Persian",
    "fince": "Finnish",
    "fransizca": "French",
    "gurcuce": "Georgian",
    "hirvatca": "Croatian",
    "hintce": "Hindi",
    "hausa": "Hausa",
    "hollandaca": "Dutch",
    "ibranice": "Hebrew",
    "ingilizce": "English",
    "ispanyolca": "Spanish",
    "isvecce": "Swedish",
    "italyanca": "Italian",
    "izlandaca": "Icelandic",
    "japonca": "Japanese",
    "korece": "Korean",
    "kurtce": "Kurdish",
    "lehce": "Polish",
    "macarca": "Hungarian",
    "malayca": "Malay",
    "maldivce": "Dhivehi",
    "maldivian": "Dhivehi",
    "norvecce": "Norwegian",
    "portekizce": "Portuguese",
    "romence": "Romanian",
    "rusca": "Russian",
    "sirpca": "Serbian",
    "slovakca": "Slovak",
    "svahili": "Swahili",
    "tayca": "Thai",
    "turkce": "Turkish",
    "ukraynaca": "Ukrainian",
    "urduca": "Urdu",
    "vietnamca": "Vietnamese",
    "yunanca": "Greek",
}


# REST Countries does not consistently expose every constitutionally official
# language. Algeria and Morocco both officially recognize Tamazight/Amazigh,
# so keep this small, verified correction separate from the upstream payload.
TAMAZIGHT_OFFICIAL_COUNTRY_CODES = {"DZA", "MAR"}
TAMAZIGHT_CANONICAL_NAME = "Tamazight / Amazigh"


LANGUAGE_NAME_ALIASES = {
    "austro-bavarian german": "German",
    "maldivian": "Dhivehi",
    "swiss german": "German",
}


# Safety net for upstream language lists that confuse official, national,
# working and commonly spoken languages.
OFFICIAL_LANGUAGE_MEMBERSHIP = {
    "dhivehi": {
        "include": {"MDV"},
        "exclude": set(),
    },
    "english": {
        "include": set(),
        "exclude": {"NER"},
    },
    "french": {
        "include": set(),
        "exclude": {"NER"},
    },
    "german": {
        "include": {"AUT", "BEL", "CHE", "DEU", "LIE", "LUX"},
        "exclude": {"NAM"},
    },
    "hausa": {
        "include": {"NER"},
        "exclude": set(),
    },
}


def normalize_language_name(value: str) -> str:
    normalized = value.strip().casefold().replace("ı", "i")
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", normalized)
        if not unicodedata.combining(character)
    )


def canonical_language_name(value: str) -> str:
    normalized = normalize_language_name(value)
    return LANGUAGE_NAME_ALIASES.get(normalized, value.strip())


def is_tamazight_name(value: str) -> bool:
    normalized = normalize_language_name(value)
    return any(
        token in normalized
        for token in ("tamazight", "tamazigh", "amazigh", "berber")
    )


def resolve_language_countries(countries: list[dict], language_name: str):
    search_value = normalize_language_name(language_name)

    if is_tamazight_name(language_name):
        matches = [
            country
            for country in countries
            if country.get("iso3") in TAMAZIGHT_OFFICIAL_COUNTRY_CODES
            or any(
                is_tamazight_name(language)
                for language in country.get("languages", [])
            )
        ]
        if not matches:
            raise ValueError(f"Language not found: {language_name}")
        return TAMAZIGHT_CANONICAL_NAME, matches

    canonical_target = canonical_language_name(
        TURKISH_LANGUAGE_ALIASES.get(search_value, language_name)
    )
    target = normalize_language_name(canonical_target)
    matches = [
        country
        for country in countries
        if any(
            normalize_language_name(canonical_language_name(language)) == target
            for language in country.get("languages", [])
        )
    ]

    membership = OFFICIAL_LANGUAGE_MEMBERSHIP.get(target)
    if membership:
        matches = [
            country
            for country in matches
            if country.get("iso3") not in membership["exclude"]
        ]
        matched_ids = {country.get("iso3") for country in matches}
        matches.extend(
            country
            for country in countries
            if country.get("iso3") in membership["include"]
            and country.get("iso3") not in matched_ids
        )

    if not matches:
        raise ValueError(f"Language not found: {language_name}")

    return canonical_target, matches
