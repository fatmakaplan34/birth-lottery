import { useEffect, useMemo, useRef, useState } from "react";
import Globe, { type GlobeMethods } from "react-globe.gl";
import { MeshPhongMaterial } from "three";
import { feature } from "topojson-client";
import type { GeometryCollection, Topology } from "topojson-specification";
import countriesAtlas from "world-atlas/countries-110m.json";
import isoCountries from "i18n-iso-countries";
import { CountryInfoCard } from "./CountryInfoCard";
import { getCountryProfile } from "./api";
import type { Country, CountryProfile } from "./api";
import { localizedCountryName, t } from "./i18n";
import type { Locale } from "./i18n";

type Props = {
  countries: Country[];
  selectedIso3: string;
  onSelect: (iso3: string) => void;
  locale: Locale;
};
type WorldFeature = {
  id?: string | number; properties?: { name?: string }; geometry: object; iso3: string;
};

export function GlobePicker({ countries, selectedIso3, onSelect, locale }: Props) {
  const wrapperRef = useRef<HTMLDivElement>(null);
  const globeRef = useRef<GlobeMethods | undefined>(undefined);
  const [size, setSize] = useState({ width: 560, height: 520 });
  const [hoveredIso3, setHoveredIso3] = useState<string | null>(null);
  const [profile, setProfile] = useState<CountryProfile | null>(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const globeMaterial = useMemo(() => new MeshPhongMaterial({
    color: "#071c2d", emissive: "#02101b", shininess: 18,
  }), []);

  const polygons = useMemo(() => {
    const topology = countriesAtlas as unknown as Topology<{
      countries: GeometryCollection; land: GeometryCollection;
    }>;
    const collection = feature(topology, topology.objects.countries) as unknown as {
      features: Array<Omit<WorldFeature, "iso3">>;
    };
    return collection.features.map((item) => ({
      ...item,
      iso3: isoCountries.numericToAlpha3(String(item.id).padStart(3, "0")) || "",
    }));
  }, []);

  const countryByIso3 = useMemo(
    () => new Map(countries.map((country) => [country.iso3, country])),
    [countries],
  );
  const hoveredCountry = hoveredIso3 ? countryByIso3.get(hoveredIso3) : undefined;

  useEffect(() => {
    if (!wrapperRef.current) return;
    const observer = new ResizeObserver(([entry]) => {
      const width = entry.contentRect.width;
      setSize({ width, height: Math.min(560, Math.max(390, width * 0.88)) });
    });
    observer.observe(wrapperRef.current);
    return () => observer.disconnect();
  }, []);

  function stopRotation() {
    const controls = globeRef.current?.controls();
    if (controls) controls.autoRotate = false;
  }

  async function inspectCountry(iso3: string) {
    onSelect(iso3);
    setProfileLoading(true);
    setProfile(null);
    try { setProfile(await getCountryProfile(iso3)); }
    catch {
      const country = countryByIso3.get(iso3);
      if (country) {
        setProfile({
          ...country,
          founding: { date: null, source: "Wikidata P571", definition: "" },
        });
      }
    }
    finally { setProfileLoading(false); }
  }

  return (
    <div className="globe-shell" ref={wrapperRef} onPointerDown={stopRotation}
      aria-label={locale === "tr" ? "Döndürülebilir ülke seçme küresi" : "Rotatable country selection globe"}>
      <div className="globe-hint"><span className="pulse-dot" /> {t(locale, "globeHint")}</div>
      {hoveredCountry && !profile && (
        <div className="globe-hover-name">
          <b>{hoveredCountry.flag_emoji} {localizedCountryName(hoveredCountry, locale)}</b>
          <span>{t(locale, "clickToInspect")}</span>
        </div>
      )}
      {profileLoading && <div className="profile-loading">{t(locale, "profileLoading")}</div>}
      {profile && <div className="globe-profile"><CountryInfoCard profile={profile} locale={locale} onClose={() => setProfile(null)} /></div>}
      <Globe
        ref={globeRef} width={size.width} height={size.height}
        backgroundColor="rgba(0,0,0,0)" globeMaterial={globeMaterial}
        showAtmosphere atmosphereColor="#4ed6c4" atmosphereAltitude={0.16}
        polygonsData={polygons}
        polygonGeoJsonGeometry={(item) => (item as WorldFeature).geometry as never}
        polygonCapColor={(item) => {
          const iso3 = (item as WorldFeature).iso3;
          if (iso3 === selectedIso3) return "#f2b66d";
          if (iso3 === hoveredIso3) return "#52d6c4";
          return countryByIso3.has(iso3) ? "#17445a" : "#102b3c";
        }}
        polygonSideColor={() => "rgba(2, 13, 22, .82)"}
        polygonStrokeColor={() => "rgba(163, 220, 216, .28)"}
        polygonAltitude={(item) => (item as WorldFeature).iso3 === selectedIso3 ? 0.025 : 0.009}
        polygonLabel={() => ""}
        onPolygonHover={(item) => setHoveredIso3(item ? (item as WorldFeature).iso3 : null)}
        onPolygonClick={(item) => {
          const iso3 = (item as WorldFeature).iso3;
          if (countryByIso3.has(iso3)) void inspectCountry(iso3);
          stopRotation();
        }}
        onGlobeReady={() => {
          const controls = globeRef.current?.controls();
          if (!controls) return;
          controls.autoRotate = true; controls.autoRotateSpeed = 0.32;
          controls.enablePan = false; controls.minDistance = 145; controls.maxDistance = 330;
        }}
      />
      <div className="globe-orbit globe-orbit-one" />
      <div className="globe-orbit globe-orbit-two" />
    </div>
  );
}
