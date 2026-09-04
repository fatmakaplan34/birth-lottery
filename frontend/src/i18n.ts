import type { Country } from "./api";

export type Locale = "tr" | "en";

const messages = {
  tr: {
    navBirth: "Doğum olasılığım", navLanguage: "Dil merceği", navCompare: "Yaşam farkı", navRandom: "Rastgele çekiliş",
    connected: "Dünya verileri bağlı", connecting: "Dünya verileri bağlanıyor", connectionProblem: "Veri bağlantısı kurulamadı", navLabel: "Uygulama bölümleri", brandSubtitle: "İnsan olasılık atlası",
    globeEyebrow: "Etkileşimli dünya · 252 bölge", headlineA: "Nerede doğma ihtimalin", headlineB: "daha yüksekti?",
    globeLoading: "Dünya hazırlanıyor…", globeHint: "Sürükle · yakınlaştır · ülkeye dokun", clickToInspect: "Bilgileri görmek için tıkla",
    personal: "Kişisel hesap", placeMoment: "Doğduğun ânı dünyaya yerleştir.", placeMomentBody: "Gün seni anlatır; hesap, o yılın küresel doğum dağılımını kullanır.",
    birthDate: "Doğum tarihi", city: "Şehir", contextOnly: "bağlam için", country: "Ülke", calculate: "Olasılığımı hesapla", calculatingWorld: "Dünya hesaplanıyor…",
    emptyInsight: "Bir tarih ve ülke seç. Sonuç burada, tek bir yoğun kartta görünecek.", birthAtlas: "doğum atlası", historical: "Tarihsel veri", latestEstimate: "Son veri tahmini",
    oneIn: "O yıl dünyaya gelen yaklaşık her {value} bebekten biri.", worldRank: "Dünya sırası", estimatedBirths: "Tahmini doğum", birthRate: "Doğum hızı", coverage: "Veri kapsamı", methodology: "Bu sayı nasıl hesaplandı?", historicalBasis: "Aynı yılın World Bank nüfusu, aynı yılın kaba doğum oranıyla çarpıldı.", latestBasis: "En güncel ülke nüfusu, mevcut en son kaba doğum oranıyla çarpıldı.", annualDateNote: "Tam tarih sonucu kişiselleştirir; yıllık kaynak kullanıldığı için olasılığı yıl belirler.", cityNote: "Şehir yalnızca bağlam olarak gösterilir; hesap ülke düzeyindedir.",
    languageEyebrow: "Dil çevresi · koşullu olasılık", languageTitle: "Seçtiğin dilin resmî olduğu ülkelerde doğumlar nasıl dağılıyor?", languageBody: "Konuşan kişi sayısını tahmin etmiyoruz. Seçilen dilin resmî olarak tanındığı ülkelerdeki tahmini doğumları karşılaştırıyoruz.",
    language: "Dil", year: "Yıl", showDistribution: "Dağılımı göster", calculating: "Hesaplanıyor…", officialLanguageContext: "resmî dil çevresi", countries: "ülke",
    languageNote: "Bu dağılım, bireysel konuşmacıların sayısını veya bir ülke nüfusunun yüzde kaçının dili konuştuğunu ölçmez. Doğum verisi bulunmayan ülkeler listede tutulur ve veri yok olarak işaretlenir.", noBirthData: "Doğum verisi yok",
    compareEyebrow: "İki ülke · aynı yıl", compareTitle: "Doğum yeri hayatı nasıl değiştiriyor?", compareBody: "Gelirden yaşam beklentisine kadar, gözlenebilir yaşam standardı göstergelerini yan yana koy.", firstCountry: "Birinci ülke", secondCountry: "İkinci ülke", compare: "Karşılaştır", comparing: "Karşılaştırılıyor…", indicator: "Gösterge",
    randomEyebrow: "Deneysel alan", randomTitle: "Bugünün doğum piyangosunu bir kez çevir.", randomBody: "Bu bölüm ana hesaplamadan bağımsızdır; tahmini doğum ağırlıklarına göre rastgele bir ülke seçer.", draw: "Piyangoyu çevir", orbiting: "Yörüngede…", drawnCountry: "Bu çekilişte doğduğun yer",
    population: "Güncel nüfus", officialLanguages: "Resmî dil / diller", capital: "Başkent", callingCode: "Telefon kodu", continent: "Kıta", founding: "Modern devlet / bağımsızlık tarihi", unavailable: "Veri mevcut değil", close: "Kapat", countryDetails: "Ülke bilgileri", sourceNote: "Tarih, modern devletin kuruluşu, bağımsızlığı veya mevcut rejimin başlangıcını ifade eder.",
    dark: "Koyu", light: "Aydınlık", theme: "Tema", languageToggle: "Arayüz dili",
    privacy: "Gizlilik", cookieSettings: "Çerez ayarları", cookieTitle: "Ziyaretçi ölçümüne izin verir misin?",
    cookieBody: "Yalnızca anonim ziyaret ve özellik kullanımını ölçmek için Google Analytics kullanıyoruz. Doğum tarihi ve şehir bilgisi gönderilmez.",
    cookieAccept: "Kabul et", cookieReject: "Reddet", cookieDetails: "Ayrıntılar",
    footerSource: "World Bank göstergeleri + REST Countries + Wikidata", footerNote: "Yıllık veriye dayalı tahmini model · kesin bireysel kader değildir",
    loadError: "Ülke verileri yüklenemedi.", retry: "Yeniden dene", calculationError: "Hesaplama yapılamadı.", comparisonError: "Karşılaştırma yapılamadı.", profileLoading: "Ülke bilgileri yükleniyor…",
    gdp_per_capita: "Kişi başı gelir", life_expectancy: "Yaşam beklentisi", internet_usage: "İnternet kullanımı", urban_population: "Kent nüfusu", infant_mortality: "Bebek ölüm oranı", birth_rate: "Doğum hızı",
    unit_gdp_per_capita: "Güncel ABD doları", unit_life_expectancy: "Yıl", unit_internet_usage: "Nüfusun yüzdesi", unit_urban_population: "Nüfusun yüzdesi", unit_infant_mortality: "1.000 canlı doğumda", unit_birth_rate: "1.000 kişide",
  },
  en: {
    navBirth: "My birth odds", navLanguage: "Language lens", navCompare: "Life comparison", navRandom: "Random draw",
    connected: "World data connected", connecting: "Connecting world data", connectionProblem: "Data connection failed", navLabel: "Application sections", brandSubtitle: "Human probability atlas",
    globeEyebrow: "Interactive world · 252 regions", headlineA: "Where were you", headlineB: "most likely to be born?",
    globeLoading: "Preparing the world…", globeHint: "Drag · zoom · select a country", clickToInspect: "Click to view details",
    personal: "Personal calculation", placeMoment: "Place your birth moment on the map.", placeMomentBody: "The date tells your story; the calculation uses the global birth distribution for that year.",
    birthDate: "Birth date", city: "City", contextOnly: "for context", country: "Country", calculate: "Calculate my odds", calculatingWorld: "Calculating the world…",
    emptyInsight: "Choose a date and country. Your result will appear here in one focused card.", birthAtlas: "birth atlas", historical: "Historical data", latestEstimate: "Latest-data estimate",
    oneIn: "Approximately one in every {value} babies born worldwide that year.", worldRank: "World rank", estimatedBirths: "Estimated births", birthRate: "Birth rate", coverage: "Data coverage", methodology: "How was this calculated?", historicalBasis: "World Bank population for the same year was multiplied by the same year's crude birth rate.", latestBasis: "The latest country population was multiplied by the latest available crude birth rate.", annualDateNote: "The full date personalizes the result; annual source data means the year determines the probability.", cityNote: "The city is shown for context only; the calculation is country-level.",
    languageEyebrow: "Language context · conditional probability", languageTitle: "How are births distributed across countries where your chosen language is official?", languageBody: "We do not estimate speaker counts. We compare estimated births across countries where the selected language is officially recognized.",
    language: "Language", year: "Year", showDistribution: "Show distribution", calculating: "Calculating…", officialLanguageContext: "official-language context", countries: "countries",
    languageNote: "This distribution does not measure individual speakers or the share of a country's population that speaks the language. Countries without birth data remain listed and are marked as unavailable.", noBirthData: "No birth data",
    compareEyebrow: "Two countries · same year", compareTitle: "How does birthplace shape life?", compareBody: "Compare observable living-standard indicators, from income to life expectancy.", firstCountry: "First country", secondCountry: "Second country", compare: "Compare", comparing: "Comparing…", indicator: "Indicator",
    randomEyebrow: "Experimental space", randomTitle: "Spin today's birth lottery once.", randomBody: "This section is separate from the main calculation and draws a country using estimated birth weights.", draw: "Spin the lottery", orbiting: "In orbit…", drawnCountry: "Your birthplace in this draw",
    population: "Current population", officialLanguages: "Official language(s)", capital: "Capital", callingCode: "Calling code", continent: "Continent", founding: "Modern-state / independence date", unavailable: "Not available", close: "Close", countryDetails: "Country details", sourceNote: "The date represents the modern state's formation, independence, or the start of its current regime.",
    dark: "Dark", light: "Light", theme: "Theme", languageToggle: "Interface language",
    privacy: "Privacy", cookieSettings: "Cookie settings", cookieTitle: "Allow anonymous visitor measurement?",
    cookieBody: "We use Google Analytics only to measure anonymous visits and feature usage. Birth dates and city information are never sent.",
    cookieAccept: "Accept", cookieReject: "Reject", cookieDetails: "Details",
    footerSource: "World Bank indicators + REST Countries + Wikidata", footerNote: "Annual-data estimate · not a statement of individual destiny",
    loadError: "Country data could not be loaded.", retry: "Try again", calculationError: "The calculation could not be completed.", comparisonError: "The comparison could not be completed.", profileLoading: "Loading country details…",
    gdp_per_capita: "GDP per capita", life_expectancy: "Life expectancy", internet_usage: "Internet usage", urban_population: "Urban population", infant_mortality: "Infant mortality", birth_rate: "Birth rate",
    unit_gdp_per_capita: "Current US$", unit_life_expectancy: "Years", unit_internet_usage: "% of population", unit_urban_population: "% of population", unit_infant_mortality: "Per 1,000 live births", unit_birth_rate: "Per 1,000 people",
  },
} as const;

export type MessageKey = keyof typeof messages.tr;
export const t = (locale: Locale, key: MessageKey) => messages[locale][key];

const languageNamesTr: Record<string, string> = {
  Albanian: "Arnavutça", Arabic: "Arapça", Armenian: "Ermenice", Bengali: "Bengalce",
  Bosnian: "Boşnakça", Bulgarian: "Bulgarca", Chinese: "Çince", Croatian: "Hırvatça",
  Czech: "Çekçe", Danish: "Danca", Dutch: "Hollandaca", English: "İngilizce",
  Dhivehi: "Divehice", Finnish: "Fince", French: "Fransızca", Georgian: "Gürcüce", German: "Almanca",
  Greek: "Yunanca", Hausa: "Hausa", Hebrew: "İbranice", Hindi: "Hintçe", Hungarian: "Macarca",
  Icelandic: "İzlandaca", Indonesian: "Endonezce", Italian: "İtalyanca", Japanese: "Japonca",
  Korean: "Korece", Kurdish: "Kürtçe", Malay: "Malayca", Norwegian: "Norveççe",
  Persian: "Farsça", Polish: "Lehçe", Portuguese: "Portekizce", Romanian: "Romence",
  Russian: "Rusça", Serbian: "Sırpça", Slovak: "Slovakça", Spanish: "İspanyolca",
  Swahili: "Svahili", Swedish: "İsveççe", Tamazight: "Tamazight / Amazigh (Berber dilleri)", Thai: "Tayca",
  Turkish: "Türkçe", Ukrainian: "Ukraynaca", Urdu: "Urduca", Vietnamese: "Vietnamca",
};

export function languageLabel(language: string, locale: Locale) {
  if (/tamazigh|tamazight|amazigh|berber/i.test(language)) {
    return locale === "tr"
      ? "Tamazight / Amazigh (Berber dilleri)"
      : "Tamazight / Amazigh (Berber languages)";
  }
  if (locale === "en") return language;
  return languageNamesTr[language] || language;
}

export function localizedCountryName(country: Country, locale: Locale) {
  return locale === "tr" ? country.name_tr || country.name : country.name;
}

export function localizedOfficialName(country: Country, locale: Locale) {
  return locale === "tr"
    ? country.official_name_tr || country.official_name
    : country.official_name;
}

const regionsTr: Record<string, string> = {
  Africa: "Afrika", Americas: "Amerika", America: "Amerika", Asia: "Asya",
  Europe: "Avrupa", Oceania: "Okyanusya", Antarctic: "Antarktika",
  Antarctica: "Antarktika",
};

export function regionLabel(region: string, locale: Locale) {
  return locale === "tr" ? regionsTr[region] || region : region;
}

export function formatLocalizedNumber(value: number, locale: Locale, digits = 0) {
  return new Intl.NumberFormat(locale === "tr" ? "tr-TR" : "en-US", {
    maximumFractionDigits: digits,
  }).format(value);
}

export function formatLocalizedDate(value: string, locale: Locale, precision = 11) {
  const [year, month, day] = value.split("-").map(Number);
  if (precision <= 8) {
    return locale === "tr" ? `${year} civarı` : `c. ${year}`;
  }
  if (precision === 9) return String(year);
  if (precision === 10) {
    return new Intl.DateTimeFormat(locale === "tr" ? "tr-TR" : "en-US", {
      month: "long", year: "numeric", timeZone: "UTC",
    }).format(new Date(Date.UTC(year, month - 1, 1)));
  }
  return new Intl.DateTimeFormat(locale === "tr" ? "tr-TR" : "en-US", {
    day: "2-digit", month: "2-digit", year: "numeric", timeZone: "UTC",
  }).format(new Date(Date.UTC(year, month - 1, day)));
}
