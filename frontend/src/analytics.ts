export const ANALYTICS_MEASUREMENT_ID = "G-G612N3EWHF";
const CONSENT_KEY = "birth-lottery-analytics-consent";
export const REOPEN_CONSENT_EVENT = "birth-lottery-reopen-cookie-consent";

declare global {
  interface Window {
    dataLayer?: unknown[][];
    gtag?: (...args: unknown[]) => void;
    [key: `ga-disable-${string}`]: boolean | undefined;
  }
}

let initialized = false;

export function analyticsConsent() {
  return localStorage.getItem(CONSENT_KEY);
}

export function initAnalytics() {
  if (initialized || analyticsConsent() !== "granted") return;

  window[`ga-disable-${ANALYTICS_MEASUREMENT_ID}`] = false;
  window.dataLayer = window.dataLayer || [];
  window.gtag = (...args: unknown[]) => {
    window.dataLayer?.push(args);
  };
  window.gtag("js", new Date());
  window.gtag("config", ANALYTICS_MEASUREMENT_ID, {
    anonymize_ip: true,
    send_page_view: true,
  });

  const script = document.createElement("script");
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${ANALYTICS_MEASUREMENT_ID}`;
  script.dataset.birthLotteryAnalytics = "true";
  document.head.appendChild(script);
  initialized = true;
}

export function updateAnalyticsConsent(granted: boolean) {
  localStorage.setItem(CONSENT_KEY, granted ? "granted" : "denied");
  window[`ga-disable-${ANALYTICS_MEASUREMENT_ID}`] = !granted;
  if (granted) initAnalytics();
}

export function clearAnalyticsConsent() {
  localStorage.removeItem(CONSENT_KEY);
}

export function reopenCookieConsent() {
  clearAnalyticsConsent();
  window.dispatchEvent(new Event(REOPEN_CONSENT_EVENT));
}

export function trackEvent(name: string) {
  if (analyticsConsent() !== "granted") return;
  initAnalytics();
  window.gtag?.("event", name);
}
