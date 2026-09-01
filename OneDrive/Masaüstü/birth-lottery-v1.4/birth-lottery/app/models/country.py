def normalize_country(raw):
    capitals = raw.get("capitals", [])
    names = raw.get("names", {})
    translations = names.get("translations", {})
    turkish_names = translations.get("tur", {})
    calling_codes = [
        f"+{str(code).lstrip('+')}"
        for code in raw.get("calling_codes", [])
        if code
    ]

    return {
        "name": names.get("common", ""),
        "name_tr": turkish_names.get("common") or names.get("common", ""),
        "official_name": names.get("official", ""),
        "official_name_tr": (
            turkish_names.get("official") or names.get("official", "")
        ),
        "iso2": raw.get("codes", {}).get("alpha_2", ""),
        "iso3": raw.get("codes", {}).get("alpha_3", ""),
        "population": raw.get("population", 0),
        "area_km2": raw.get("area", {}).get("kilometers", ""),
        "region": raw.get("region", ""),
        "subregion": raw.get("subregion", ""),
        "continents": raw.get("continents", []) or [raw.get("region", "")],
        "capital": capitals[0].get("name", "") if capitals else "",
        "languages": [item.get("name", "") for item in raw.get("languages", [])],
        "calling_codes": calling_codes,
        "currencies": [
            {
                "code": item.get("code", ""),
                "name": item.get("name", ""),
                "symbol": item.get("symbol", "")
            }
            for item in raw.get("currencies", [])
        ],
        "flag_svg": raw.get("flag", {}).get("url_svg", ""),
        "flag_emoji": raw.get("flag", {}).get("emoji", ""),
        "borders": raw.get("borders", []),
    }
