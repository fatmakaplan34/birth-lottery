import { lazy, Suspense, useEffect, useMemo, useState } from "react";
import {
  drawLottery, getBirthOdds, getCountries, getCountryProfile,
  getLanguageOdds, getLivingStandards,
} from "./api";
import type {
  BirthOddsResponse, ComparisonCountry, Country, CountryProfile,
  LanguageOddsResponse, LivingStandardsResponse,
} from "./api";
import { CountryInfoCard } from "./CountryInfoCard";
import {
  formatLocalizedNumber, languageLabel, localizedCountryName,
  t,
} from "./i18n";
import type { Locale, MessageKey } from "./i18n";
import "./App.css";

const GlobePicker = lazy(() =>
  import("./GlobePicker").then((module) => ({ default: module.GlobePicker })),
);

type View = "birth" | "language" | "compare" | "random";
type Theme = "dark" | "light";
const currentYear = new Date().getFullYear();
const viewKeys: Array<{ id: View; key: MessageKey; number: string }> = [
  { id: "birth", key: "navBirth", number: "01" },
  { id: "language", key: "navLanguage", number: "02" },
  { id: "compare", key: "navCompare", number: "03" },
  { id: "random", key: "navRandom", number: "04" },
];

function visibleError(error: unknown, fallback: string) {
  return error instanceof Error && error.message ? error.message : fallback;
}

function CountrySelect({ countries, value, onChange, label, locale }: {
  countries: Country[]; value: string; onChange: (value: string) => void;
  label: string; locale: Locale;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {countries.map((country) => (
          <option key={country.iso3} value={country.iso3}>
            {country.flag_emoji} {localizedCountryName(country, locale)}
          </option>
        ))}
      </select>
    </label>
  );
}

function BirthResult({ result, locale }: { result: BirthOddsResponse; locale: Locale }) {
  const historical = result.methodology.calculation_mode === "historical_observation";
  const countryName = localizedCountryName(result.country, locale);
  return (
    <section className="result-card" aria-live="polite">
      <div className="result-heading">
        <div>
          <p className="eyebrow">{result.query.year_used_for_probability} {t(locale, "birthAtlas")}</p>
          <h2>{result.country.flag_emoji} {result.query.city ? `${result.query.city}, ` : ""}{countryName}</h2>
        </div>
        <span className="data-badge">{t(locale, historical ? "historical" : "latestEstimate")}</span>
      </div>
      <div className="probability-display">
        <div className="probability-number"><strong>{result.probability.percentage.toFixed(3)}</strong><span>%</span></div>
        <p>{t(locale, "oneIn").replace("{value}", formatLocalizedNumber(result.probability.one_in_x, locale))}</p>
      </div>
      <div className="stat-grid">
        <div><span>{t(locale, "worldRank")}</span><b>#{result.probability.rank}</b></div>
        <div><span>{t(locale, "estimatedBirths")}</span><b>{formatLocalizedNumber(result.probability.estimated_births, locale)}</b></div>
        <div><span>{t(locale, "birthRate")}</span><b>‰ {result.source_values.birth_rate_per_1000.toFixed(1)}</b></div>
        <div><span>{t(locale, "coverage")}</span><b>%{result.methodology.population_coverage_percentage.toFixed(1)}</b></div>
      </div>
      <details className="method-note">
        <summary>{t(locale, "methodology")}</summary>
        <p>{t(locale, historical ? "historicalBasis" : "latestBasis")}</p>
        <p>{t(locale, "annualDateNote")}</p>
        {result.query.city && <p>{t(locale, "cityNote")}</p>}
      </details>
    </section>
  );
}

function canonicalLanguageName(value: string) {
  return /tamazigh|tamazight|amazigh|berber/i.test(value)
    ? "Tamazight / Amazigh"
    : value;
}

function LanguagePanel({ countries, locale }: { countries: Country[]; locale: Locale }) {
  const [language, setLanguage] = useState(locale === "tr" ? "Fransızca" : "French");
  const [year, setYear] = useState(currentYear);
  const [result, setResult] = useState<LanguageOddsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const languages = useMemo(() => {
    const canonical = [...new Set(countries.flatMap((country) =>
      country.languages.map(canonicalLanguageName),
    ))];
    return canonical.sort((a, b) => languageLabel(a, locale).localeCompare(languageLabel(b, locale)));
  }, [countries, locale]);

  async function analyze() {
    setLoading(true); setError(null);
    try { setResult(await getLanguageOdds(language, year)); }
    catch (requestError) {
      setError(visibleError(requestError, t(locale, "calculationError")));
    }
    finally { setLoading(false); }
  }

  return (
    <div className="module-panel language-panel">
      <div className="module-intro">
        <p className="eyebrow">{t(locale, "languageEyebrow")}</p>
        <h2>{t(locale, "languageTitle")}</h2>
        <p>{t(locale, "languageBody")}</p>
      </div>
      <div className="compact-form">
        <label className="field"><span>{t(locale, "language")}</span>
          <input list="language-list" value={language} onChange={(event) => setLanguage(event.target.value)} />
          <datalist id="language-list">{languages.map((item) => <option key={item} value={languageLabel(item, locale)} />)}</datalist>
        </label>
        <label className="field field-small"><span>{t(locale, "year")}</span><input type="number" min="1960" max={currentYear} value={year} onChange={(event) => setYear(Number(event.target.value))} /></label>
        <button className="primary-button" type="button" onClick={analyze} disabled={loading}>{t(locale, loading ? "calculating" : "showDistribution")}</button>
      </div>
      {error && <p className="error-message">{error}</p>}
      {result && (
        <div className="ranking-list" aria-live="polite">
          <div className="ranking-header"><span>{languageLabel(result.language, locale)} · {t(locale, "officialLanguageContext")}</span><b>{result.country_count} {t(locale, "countries")}</b></div>
          {result.countries.map((item) => (
            <div className="ranking-row" key={item.iso3}>
              <span className="rank">{item.rank === null ? "—" : String(item.rank).padStart(2, "0")}</span>
              <span className="country-name">{item.flag_emoji} {locale === "tr" ? item.country_tr || item.country : item.country}</span>
              <div className="bar-track"><i style={{ width: `${item.conditional_percentage === null ? 0 : Math.max(2, item.conditional_percentage)}%` }} /></div>
              <b className={item.data_available ? "" : "no-data"}>{item.conditional_percentage === null ? t(locale, "noBirthData") : `%${item.conditional_percentage.toFixed(2)}`}</b>
            </div>
          ))}
          <p className="fine-print">{t(locale, "languageNote")}</p>
        </div>
      )}
    </div>
  );
}

const metricKeys = [
  "gdp_per_capita", "life_expectancy", "internet_usage",
  "urban_population", "infant_mortality", "birth_rate",
] as const;

function metricValue(country: ComparisonCountry, metric: string) {
  return country.metrics[metric]?.value ?? null;
}

function ComparePanel({ countries, locale }: { countries: Country[]; locale: Locale }) {
  const [country1, setCountry1] = useState("FRA");
  const [country2, setCountry2] = useState("COD");
  const [year, setYear] = useState(currentYear);
  const [result, setResult] = useState<LivingStandardsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  async function compare() {
    setLoading(true); setError(null);
    try { setResult(await getLivingStandards(country1, country2, year)); }
    catch (requestError) {
      setError(visibleError(requestError, t(locale, "comparisonError")));
    }
    finally { setLoading(false); }
  }
  const resultName = (country: ComparisonCountry) => locale === "tr" ? country.country_tr || country.country : country.country;
  return (
    <div className="module-panel compare-panel">
      <div className="module-intro">
        <p className="eyebrow">{t(locale, "compareEyebrow")}</p><h2>{t(locale, "compareTitle")}</h2><p>{t(locale, "compareBody")}</p>
      </div>
      <div className="compare-form">
        <CountrySelect countries={countries} value={country1} onChange={setCountry1} label={t(locale, "firstCountry")} locale={locale} />
        <span className="versus">VS</span>
        <CountrySelect countries={countries} value={country2} onChange={setCountry2} label={t(locale, "secondCountry")} locale={locale} />
        <label className="field field-small"><span>{t(locale, "year")}</span><input type="number" min="1960" max={currentYear} value={year} onChange={(event) => setYear(Number(event.target.value))} /></label>
        <button className="primary-button" type="button" onClick={compare} disabled={loading}>{t(locale, loading ? "comparing" : "compare")}</button>
      </div>
      {error && <p className="error-message">{error}</p>}
      {result && (
        <div className="comparison-table" aria-live="polite">
          <div className="comparison-head"><span>{t(locale, "indicator")}</span><b>{result.country1.flag_emoji} {resultName(result.country1)}</b><b>{result.country2.flag_emoji} {resultName(result.country2)}</b></div>
          {metricKeys.map((metric) => {
            const left = metricValue(result.country1, metric); const right = metricValue(result.country2, metric);
            return (
              <div className="comparison-row" key={metric}>
                <span>{t(locale, metric)}<small>{t(locale, `unit_${metric}` as MessageKey)}</small></span>
                <b>{left === null ? "—" : formatLocalizedNumber(left, locale, 1)}<small>{result.country1.metrics[metric]?.year}</small></b>
                <b>{right === null ? "—" : formatLocalizedNumber(right, locale, 1)}<small>{result.country2.metrics[metric]?.year}</small></b>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function RandomPanel({ locale }: { locale: Locale }) {
  const [profile, setProfile] = useState<CountryProfile | null>(null);
  const [probability, setProbability] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  async function draw() {
    setLoading(true); setError(null); setProfile(null);
    try {
      const lottery = await drawLottery();
      setProbability(lottery.birth_probability.percentage);
      setProfile(await getCountryProfile(lottery.result.iso3));
    } catch (requestError) {
      setError(visibleError(requestError, t(locale, "calculationError")));
    }
    finally { setLoading(false); }
  }
  return (
    <div className="module-panel random-panel">
      <div className="module-intro"><p className="eyebrow">{t(locale, "randomEyebrow")}</p><h2>{t(locale, "randomTitle")}</h2><p>{t(locale, "randomBody")}</p></div>
      <button className="lottery-button" type="button" onClick={draw} disabled={loading}><span>{t(locale, loading ? "orbiting" : "draw")}</span><i>↗</i></button>
      {error && <p className="error-message">{error}</p>}
      {profile && probability !== null && <div className="random-country-card"><CountryInfoCard profile={profile} locale={locale} probability={probability} /></div>}
    </div>
  );
}

function App() {
  const [view, setView] = useState<View>("birth");
  const [locale, setLocale] = useState<Locale>(() => (localStorage.getItem("birth-lottery-locale") as Locale) || "tr");
  const [theme, setTheme] = useState<Theme>(() => (localStorage.getItem("birth-lottery-theme") as Theme) || "dark");
  const [countries, setCountries] = useState<Country[]>([]);
  const [countriesLoading, setCountriesLoading] = useState(true);
  const [countriesError, setCountriesError] = useState<string | null>(null);
  const [selectedIso3, setSelectedIso3] = useState("TUR");
  const [birthDate, setBirthDate] = useState("2004-12-14");
  const [city, setCity] = useState("Ankara");
  const [result, setResult] = useState<BirthOddsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("birth-lottery-theme", theme);
  }, [theme]);
  useEffect(() => {
    document.documentElement.lang = locale;
    document.title = "Birth Lottery";
    localStorage.setItem("birth-lottery-locale", locale);
  }, [locale]);
  async function loadCountries() {
    setCountriesLoading(true);
    setCountriesError(null);
    try {
      const response = await getCountries();
      setCountries(response.countries);
    } catch (requestError) {
      setCountriesError(visibleError(requestError, t(locale, "loadError")));
    } finally {
      setCountriesLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;
    getCountries()
      .then((response) => {
        if (!cancelled) setCountries(response.countries);
      })
      .catch((requestError: unknown) => {
        if (!cancelled) {
          setCountriesError(visibleError(requestError, "Country data could not be loaded."));
        }
      })
      .finally(() => {
        if (!cancelled) setCountriesLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const selected = countries.find((country) => country.iso3 === selectedIso3);
  async function analyzeBirth() {
    if (!selected || !birthDate) return;
    setLoading(true); setError(null);
    try { setResult(await getBirthOdds({ country: selected.iso3, birthDate, city })); }
    catch (requestError) {
      setError(visibleError(requestError, t(locale, "calculationError")));
    }
    finally { setLoading(false); }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" type="button" onClick={() => setView("birth")} aria-label="Birth Lottery">
          <img className="brand-mark" src="/brand/birth-lottery-mark.png" alt="" />
          <span className="brand-copy">
            <span className="brand-name"><strong>Birth</strong> Lottery</span>
            <small className="brand-slogan"><span>Born anywhere.</span> <em>Human everywhere.</em></small>
          </span>
        </button>
        <div className="display-controls">
          <div className="locale-toggle" aria-label={t(locale, "languageToggle")}><button type="button" className={locale === "tr" ? "active" : ""} onClick={() => setLocale("tr")}>TR</button><button type="button" className={locale === "en" ? "active" : ""} onClick={() => setLocale("en")}>EN</button></div>
          <button type="button" className="theme-toggle" onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label={t(locale, "theme")}><span>{theme === "dark" ? "☼" : "◐"}</span>{t(locale, theme === "dark" ? "light" : "dark")}</button>
          <span className={`live-status ${countriesError ? "status-error" : ""}`}>
            <i /> {t(locale, countriesError ? "connectionProblem" : countriesLoading ? "connecting" : "connected")}
          </span>
        </div>
      </header>
      <nav className="section-nav" aria-label={t(locale, "navLabel")}>
        {viewKeys.map((item) => <button className={view === item.id ? "active" : ""} key={item.id} type="button" onClick={() => setView(item.id)}><span>{item.number}</span>{t(locale, item.key)}</button>)}
      </nav>

      {view === "birth" && (
        <main className="birth-workspace">
          <section className="globe-column">
            <div className="section-heading"><p className="eyebrow">{t(locale, "globeEyebrow")}</p><h1>{t(locale, "headlineA")}<br /><em>{t(locale, "headlineB")}</em></h1></div>
            <Suspense fallback={<div className="globe-loading">{t(locale, "globeLoading")}</div>}>
              <GlobePicker countries={countries} selectedIso3={selectedIso3} onSelect={setSelectedIso3} locale={locale} />
            </Suspense>
            {countriesError && (
              <div className="country-load-error" role="alert">
                <b>{t(locale, "loadError")}</b>
                <span>{countriesError}</span>
                <button type="button" onClick={() => void loadCountries()}>
                  {t(locale, "retry")}
                </button>
              </div>
            )}
          </section>
          <section className="analysis-column">
            <div className="analysis-card">
              <div className="card-number">01 / {t(locale, "personal").toLocaleUpperCase(locale)}</div><h2>{t(locale, "placeMoment")}</h2><p>{t(locale, "placeMomentBody")}</p>
              <div className="birth-form">
                <label className="field"><span>{t(locale, "birthDate")}</span><input type="date" min="1960-01-01" max={`${currentYear}-12-31`} value={birthDate} onChange={(event) => setBirthDate(event.target.value)} /></label>
                <label className="field"><span>{t(locale, "city")} <small>{t(locale, "contextOnly")}</small></span><input value={city} onChange={(event) => setCity(event.target.value)} placeholder="Ankara" /></label>
                <CountrySelect countries={countries} value={selectedIso3} onChange={setSelectedIso3} label={t(locale, "country")} locale={locale} />
              </div>
              <button className="primary-button wide" type="button" onClick={analyzeBirth} disabled={loading || !selected}><span>{t(locale, loading ? "calculatingWorld" : "calculate")}</span><b>↗</b></button>
              {error && <p className="error-message">{error}</p>}
            </div>
            {result ? <BirthResult result={result} locale={locale} /> : <div className="empty-insight"><span>∞</span><p>{t(locale, "emptyInsight")}</p></div>}
          </section>
        </main>
      )}
      {view === "language" && <main className="secondary-workspace"><LanguagePanel key={locale} countries={countries} locale={locale} /></main>}
      {view === "compare" && <main className="secondary-workspace"><ComparePanel countries={countries} locale={locale} /></main>}
      {view === "random" && <main className="secondary-workspace"><RandomPanel locale={locale} /></main>}
      <footer><span>{t(locale, "footerSource")}</span><span>{t(locale, "footerNote")}</span></footer>
    </div>
  );
}

export default App;
