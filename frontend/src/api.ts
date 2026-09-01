const configuredApiUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = configuredApiUrl
  || (import.meta.env.DEV ? "http://127.0.0.1:8081" : window.location.origin);

export type Country = {
  name: string;
  name_tr: string;
  official_name: string;
  official_name_tr: string;
  iso2: string;
  iso3: string;
  population: number;
  region: string;
  subregion: string;
  capital: string;
  languages: string[];
  flag_emoji: string;
  flag_svg: string;
  calling_codes: string[];
  continents: string[];
};

export type CountryProfile = Country & {
  founding: {
    date: string | null;
    precision?: number | null;
    event?: { tr: string; en: string } | null;
    source: string;
    source_url?: string | null;
    definition: string;
  };
};

export type CountriesResponse = {
  count: number;
  world_population: number;
  countries: Country[];
};

export type BirthOddsResponse = {
  query: { birth_date: string; year_used_for_probability: number; city: string | null };
  country: Country;
  probability: {
    percentage: number; one_in_x: number; rank: number;
    ranked_country_count: number; estimated_births: number; total_estimated_births: number;
  };
  source_values: {
    population: number; population_year: number | null;
    birth_rate_per_1000: number; birth_rate_year: number;
  };
  methodology: {
    calculation_mode: "historical_observation" | "latest_available_estimate";
    basis: string; population_coverage_percentage: number;
    date_note: string; city_note: string | null;
  };
};

export type LanguageOddsResponse = {
  language: string; requested_year: number; metric: string; important_note: string;
  calculation_mode: string; country_count: number; included_country_count: number;
  excluded_country_count: number; estimated_births_in_language_countries: number;
  countries: Array<{
    rank: number | null; country: string; country_tr: string; iso3: string; flag_emoji: string;
    estimated_births: number | null; conditional_percentage: number | null;
    conditional_one_in_x: number | null; global_percentage: number | null;
    data_available: boolean;
  }>;
};

type IndicatorValue = { year: number; value: number } | null;
export type ComparisonCountry = {
  country: string; country_tr: string; iso3: string; flag_emoji: string;
  metrics: Record<string, IndicatorValue>;
};
export type LivingStandardsResponse = {
  requested_year: number; data_note: string;
  metric_definitions: Record<string, { unit: string; higher_is_generally_better: boolean | null }>;
  country1: ComparisonCountry; country2: ComparisonCountry;
};

export type LotteryResponse = {
  result: {
    country: string; country_tr: string; official_name: string; official_name_tr: string; iso2: string; iso3: string;
    flag_emoji: string; region: string; subregion: string;
    capital: string; languages: string[];
  };
  birth_probability: {
    birth_rate_per_1000: number; birth_rate_year: number;
    estimated_annual_births: number; percentage: number; one_in_x: number;
  };
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    let message = `İstek başarısız oldu (${response.status})`;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body.detail) message = body.detail;
    } catch {
      // Status-based fallback stays visible when the response is not JSON.
    }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export const getCountries = () => request<CountriesResponse>("/countries/");
export const getCountryProfile = (country: string) =>
  request<CountryProfile>(`/countries/${encodeURIComponent(country)}/profile`);

export function getBirthOdds(params: { country: string; birthDate: string; city?: string }) {
  const query = new URLSearchParams({ country: params.country, birth_date: params.birthDate });
  if (params.city?.trim()) query.set("city", params.city.trim());
  return request<BirthOddsResponse>(`/odds/birth?${query}`);
}

export function getLanguageOdds(language: string, year: number) {
  const query = new URLSearchParams({ language, year: String(year) });
  return request<LanguageOddsResponse>(`/odds/language?${query}`);
}

export function getLivingStandards(country1: string, country2: string, year: number) {
  const query = new URLSearchParams({ country1, country2, year: String(year) });
  return request<LivingStandardsResponse>(`/odds/living-standards?${query}`);
}

export const drawLottery = () =>
  request<LotteryResponse>("/lottery/draw", { method: "POST" });
