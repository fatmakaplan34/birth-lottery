# Birth Lottery

🇹🇷 Türkçe
Birth Lottery, bir kişinin belirli bir yılda seçtiği ülkede doğma olasılığını
hesaplayan etkileşimli bir veri atlasıdır. Uygulama ayrıca resmî dil çevrelerine
göre koşullu doğum dağılımı ve iki ülke arasında yaşam standardı karşılaştırması
sunar.

![Birth Lottery ana ekranı](https://github.com/user-attachments/assets/6abc6e55-75b2-4cb6-a38a-02cc8351f169)

![Birth Lottery ayrıntı görünümü](https://github.com/user-attachments/assets/8956f50b-f018-4913-a419-02ade07f73a4)

## Neler var?

- Tarih, şehir ve ülke ile kişisel doğum olasılığı
- Mouse veya dokunmayla döndürülebilen, yakınlaştırılabilen ülke seçme küresi
- Kürede ülke adını hover ile görme ve tıklayınca ayrıntılı ülke kartı
- Türkçe/İngilizce arayüz ve koyu/aydınlık tema
- Geçmiş yıllar için aynı yılın nüfusu ve kaba doğum oranıyla hesaplama
- Güncel tarihler için en son mevcut verilerle açıkça etiketlenmiş tahmin
- Fransızca gibi bir dilin resmî olduğu ülkeler arasında koşullu olasılık
- Gelir, yaşam beklentisi, internet, kentleşme ve bebek ölümü karşılaştırması
- İkincil bir deney olarak mevcut rastgele doğum piyangosu
- Rastgele çekiliş sonucunda nüfus, dil, başkent, telefon kodu, kıta ve
  kuruluş/modern devlet tarihi kartı

## Çalıştırma

Projeyi yeni bir klasöre çıkarıyorsanız `.env.example` dosyasını `.env` olarak
kopyalayın ve mevcut REST Countries anahtarınızı `RC_API_KEY` alanına yazın.
`COUNTRY_DATA_MODE=live` seçiliyken ülke referans bilgileri öncelikle bu dış
API'den alınır. Anahtar eksik/geçersizse veya servis geçici olarak yanıt
vermezse kürenin ve ülke seçiminin tamamen kaybolmaması için paket içindeki 252
ülkelik veri otomatik yedek olarak kullanılır. Doğum ve yaşam standardı
hesaplamaları World Bank dış API verileriyle yapılmaya devam eder.

Güncelleme için mevcut proje klasörünü kullanıyorsanız çalışan `.env` dosyanızı
koruyun; güvenlik nedeniyle gerçek API anahtarı ZIP paketine eklenmez.

İki terminal açın. İlk terminalde proje kökünden backend'i başlatın:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8081
```

İkinci terminalde frontend'i başlatın:

```powershell
cd frontend
npm install
npm run dev
```

Ardından `http://localhost:5173` adresini açın. API belgeleri
`http://127.0.0.1:8081/docs` adresindedir.

## Tek linkle yayınlama

Proje production ortamında tek Docker servisi olarak çalışır. Docker önce React
arayüzünü derler, ardından FastAPI hem arayüzü hem API uçlarını aynı HTTPS
adresinden sunar. Render için hazır ayarlar `Dockerfile` ve `render.yaml`
dosyalarındadır. GitHub ve Render adımları için [DEPLOYMENT.md](DEPLOYMENT.md)
rehberini izleyin.

Production'da:

- Render'ın verdiği `PORT` değeri kullanılır.
- `/health` sağlık kontrolü olarak açıktır.
- Swagger ve OpenAPI belgeleri dışarıya kapatılır.
- API anahtarı yalnızca Render environment variable olarak saklanır.
- Güvenlik ve HTTPS yönlendirmesiyle uyumlu response başlıkları eklenir.

## Yeni API uçları

- `GET /odds/birth?country=TUR&birth_date=2004-12-14&city=Ankara`
- `GET /odds/language?language=French&year=2026`
- `GET /odds/living-standards?country1=FRA&country2=COD&year=2026`
- `GET /countries/TUR/profile`

## Veri metodolojisi

Geçmiş yıl hesabında World Bank'in o yıla ait ülke nüfusu ile kaba doğum oranı
çarpılır. Tam tarih kullanıcı bağlamı sağlar; kaynak yıllık olduğu için olasılığı
belirleyen kısım yıldır. Şehir bilgisi de şimdilik yalnızca bağlamdır ve hesap
ülke düzeyinde yapılır.

Güncel yıl için henüz kesin yıllık veri bulunmadığında uygulama en son mevcut
nüfus ve doğum oranlarını kullanır ve sonucu “son veri tahmini” olarak etiketler.

Dil ekranı konuşan kişi sayısını hesaplamaz. Sonuç, seçilen dilin resmî olarak
tanındığı ülkelerdeki tahmini doğumlar arasındaki koşullu dağılımdır.
Arnavutça/Türkçe gibi Türkçe dil adları İngilizce kaynak adlarıyla eşleştirilir.
Tamazight, Amazigh, Berber ve bölgesel Tamazight adları aynı dil çevresinde
birleştirilir. Doğum oranı verisi bulunmayan Kosova gibi ülkeler gizlenmez;
listede "doğum verisi yok" olarak gösterilir ve onlar için yüzde uydurulmaz.

Ülke kartlarındaki nüfus, telefon kodu ve ülke bilgileri REST Countries
kaynağından gelir. Canlı servis kullanılamadığında ülke seçimi için yerel veri
yedeği açılır; kart profili görüntülenirken nüfus World Bank'in erişilebilen en
son kaydıyla güncellenir. Modern devlet/bağımsızlık alanı, uygulamadaki 252 ülke ve
bölgenin tamamı için yerel veri anlık görüntüsünden okunur. Ana kaynak Wikidata
P571'dir; P571 kaydı bulunmayan bağımlı bölgeler, tartışmalı devletler ve özel
ISO grupları resmî tarihçe veya statü kaynaklarıyla ayrıca tanımlanmıştır.
Tarihin yalnızca yıl düzeyinde bilindiği kayıtlarda yapay gün ve ay gösterilmez.
Svalbard ve Jan Mayen gibi tek bir idari devlet oluşturmayan girdilerde ise
uydurma tarih yerine statünün neden tarih taşımadığı açıklanır. Her kartta kaynak
bağlantısı bulunur; canlı Wikidata sorgusu yalnızca yerel anlık görüntüde olmayan
gelecekteki yeni kayıtlar için yedek olarak kullanılır.


| 🇬🇧 English
Birth Lottery is an interactive data atlas that calculates the probability of a person being born in a selected country during a specific year. The application also provides conditional birth distributions based on official-language communities and comparisons of living standards between two countries.

![Birth Lottery ana ekranı](https://github.com/user-attachments/assets/6abc6e55-75b2-4cb6-a38a-02cc8351f169)

![Birth Lottery ayrıntı görünümü](https://github.com/user-attachments/assets/8956f50b-f018-4913-a419-02ade07f73a4)

Features
Personal birth probability based on a date, city, and country
A country-selection globe that can be rotated and zoomed using a mouse or touchscreen
Country names displayed on hover and detailed country cards displayed on click
Turkish/English interface and dark/light theme
Historical calculations using population and crude birth-rate data from the selected year
Clearly labelled estimates based on the latest available data for current dates
Conditional probabilities among countries where a language such as French is officially recognised
Comparisons of income, life expectancy, internet usage, urbanisation, and infant mortality
The existing random birth lottery as an additional experience
A result card displaying population, languages, capital, calling code, flag, continent, and establishment/modern-state date
Running the Project

If you are extracting the project into a new folder, copy .env.example as .env and enter your REST Countries API key in the RC_API_KEY field.

When COUNTRY_DATA_MODE=live is enabled, country reference information is retrieved primarily from this external API. If the API key is missing or invalid, or if the service temporarily fails to respond, the bundled dataset containing 252 countries is automatically used as a fallback so that the globe and country-selection features remain available.

Birth and living-standard calculations continue to use external World Bank API data.

If you are updating an existing project folder, preserve your working .env file. For security reasons, the actual API key is not included in the ZIP package.

Open two terminals. In the first terminal, start the backend from the project root:
```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8081
```
In the second terminal, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`. The API documentation is available at `http://127.0.0.1:8081/docs`.

Single-Link Deployment

In production, the project runs as a single Docker service. Docker first builds the React interface, after which FastAPI serves both the interface and API endpoints from the same HTTPS address.

Deployment-ready configuration for Render is provided in the Dockerfile and render.yaml files. Follow the DEPLOYMENT.md guide for the GitHub and Render deployment steps.

In production:

-The `PORT` value provided by Render is used.
-`/health` is available as the health-check endpoint.
-Swagger and OpenAPI documentation are disabled publicly.
-The API key is stored only as a Render environment variable.
-Response headers compatible with security and HTTPS redirection are included.

# New API Endpoints

- `GET /odds/birth?country=TUR&birth_date=2004-12-14&city=Ankara`
- `GET /odds/language?language=French&year=2026`
- `GET /odds/living-standards?country1=FRA&country2=COD&year=2026`
- `GET /countries/TUR/profile`

Data Methodology

For historical calculations, a country’s population in the selected year is multiplied by its crude birth rate for the same year using World Bank data.

The full date provides context for the user. However, because the source data is annual, the year is the component that determines the probability. City information currently provides context only, and calculations are performed at the country level.

When final annual data is not yet available for the current year, the application uses the latest available population and birth-rate data and labels the result as a “latest-data estimate.”

The language screen does not calculate the number of people who speak a language. Instead, the result represents the conditional distribution of estimated births among countries where the selected language is officially recognised.

Turkish language names such as “Arnavutça” and “Türkçe” are mapped to their English source names. Tamazight, Amazigh, Berber, and regional Tamazight names are grouped within the same language community.

Countries such as Kosovo, for which birth-rate data is unavailable, are not hidden. They are shown in the list as “birth data unavailable,” and no percentage is fabricated for them.

Population, calling codes, and country information displayed on country cards are obtained from REST Countries. If the live service is unavailable, the application activates its local fallback dataset for country selection. When a country profile is displayed, its population is updated using the latest accessible World Bank record.
The modern-state/independence field is read from a local data snapshot covering all 252 countries and territories in the application. The primary source is Wikidata property P571. Dependent territories, disputed states, and special ISO groups without a P571 record are separately documented using official historical or status sources.

When a date is known only at the year level, an artificial day and month are not displayed. For entries such as Svalbard and Jan Mayen, which do not form a single administrative state, the application explains why the status does not have a unified date instead of inventing one.
Each country card includes a source link. Live Wikidata queries are used only as a fallback for future records that are not included in the local snapshot.
