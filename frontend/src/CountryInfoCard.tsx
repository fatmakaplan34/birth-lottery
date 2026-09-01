import type { CountryProfile } from "./api";
import {
  formatLocalizedDate, formatLocalizedNumber, languageLabel,
  localizedCountryName, localizedOfficialName, regionLabel, t,
} from "./i18n";
import type { Locale } from "./i18n";

export function CountryInfoCard({ profile, locale, onClose, probability }: {
  profile: CountryProfile; locale: Locale; onClose?: () => void; probability?: number;
}) {
  const noData = t(locale, "unavailable");
  return (
    <article className="country-info-card" aria-label={t(locale, "countryDetails")}>
      <header>
        <div className="country-flag-wrap">
          {profile.flag_svg ? <img src={profile.flag_svg} alt="" /> : <span>{profile.flag_emoji}</span>}
        </div>
        <div>
          <p>{profile.iso3} · {regionLabel(profile.region, locale)}</p>
          <h3>{localizedCountryName(profile, locale)}</h3>
          <small>{localizedOfficialName(profile, locale)}</small>
        </div>
        {onClose && <button type="button" className="card-close" onClick={onClose} aria-label={t(locale, "close")}>×</button>}
      </header>
      {probability !== undefined && <div className="card-probability"><span>{t(locale, "drawnCountry")}</span><b>%{probability.toFixed(2)}</b></div>}
      <dl>
        <div><dt>{t(locale, "population")}</dt><dd>{formatLocalizedNumber(profile.population, locale)}</dd></div>
        <div><dt>{t(locale, "capital")}</dt><dd>{profile.capital || noData}</dd></div>
        <div className="wide"><dt>{t(locale, "officialLanguages")}</dt><dd>{profile.languages.length ? profile.languages.map((item) => languageLabel(item, locale)).join(", ") : noData}</dd></div>
        <div><dt>{t(locale, "callingCode")}</dt><dd>{profile.calling_codes?.join(", ") || noData}</dd></div>
        <div><dt>{t(locale, "continent")}</dt><dd>{profile.continents?.length ? profile.continents.map((item) => regionLabel(item, locale)).join(", ") : regionLabel(profile.region, locale) || noData}</dd></div>
        <div className="wide">
          <dt>{t(locale, "founding")}</dt>
          <dd>
            {profile.founding?.date || profile.founding?.event ? (
              <>
                {profile.founding.date && formatLocalizedDate(
                  profile.founding.date,
                  locale,
                  profile.founding.precision ?? 11,
                )}
                {profile.founding.event && (
                  <small>{profile.founding.event[locale]}</small>
                )}
              </>
            ) : noData}
          </dd>
        </div>
      </dl>
      {(profile.founding?.date || profile.founding?.event) && (
        <p className="country-source-note">
          {t(locale, "sourceNote")} · {profile.founding.source_url ? (
            <a href={profile.founding.source_url} target="_blank" rel="noreferrer">
              {profile.founding.source}
            </a>
          ) : profile.founding.source}
        </p>
      )}
    </article>
  );
}
