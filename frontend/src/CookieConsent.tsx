import { useEffect, useState } from "react";
import {
  analyticsConsent,
  REOPEN_CONSENT_EVENT,
  updateAnalyticsConsent,
} from "./analytics";
import { t } from "./i18n";
import type { Locale } from "./i18n";

export function CookieConsent({ locale }: { locale: Locale }) {
  const [decision, setDecision] = useState<string | null>(() => analyticsConsent());

  useEffect(() => {
    const reopen = () => setDecision(null);
    window.addEventListener(REOPEN_CONSENT_EVENT, reopen);
    return () => window.removeEventListener(REOPEN_CONSENT_EVENT, reopen);
  }, []);

  if (decision !== null) return null;

  function decide(granted: boolean) {
    updateAnalyticsConsent(granted);
    setDecision(granted ? "granted" : "denied");
  }

  return (
    <aside className="cookie-consent" role="dialog" aria-live="polite" aria-label={t(locale, "cookieTitle")}>
      <div className="cookie-consent-copy">
        <h2>{t(locale, "cookieTitle")}</h2>
        <p>
          {t(locale, "cookieBody")}{" "}
          <a href="/privacy.html">{t(locale, "cookieDetails")}</a>
        </p>
      </div>
      <div className="cookie-actions">
        <button type="button" onClick={() => decide(false)}>{t(locale, "cookieReject")}</button>
        <button className="cookie-accept" type="button" onClick={() => decide(true)}>{t(locale, "cookieAccept")}</button>
      </div>
    </aside>
  );
}
