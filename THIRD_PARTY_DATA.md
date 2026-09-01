# Third-party data

`app/data/countries_snapshot.json` is an offline resilience layer. Live mode
continues to prefer the configured REST Countries API; calculations continue
to use World Bank indicator endpoints.

The fallback combines ISO country reference fields derived from the
`mledoze/countries` dataset (`world-countries`, Open Database License) with
World Bank population observations. A small number of territories and special
entities absent from that series retain the last successful country-service
snapshot used by this project.

- https://github.com/mledoze/countries
- https://data.worldbank.org/indicator/SP.POP.TOTL
- https://restcountries.com/
