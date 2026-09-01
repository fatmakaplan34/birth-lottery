# Birth Lottery

<p align="center">
  <strong>Explore how birthplace, year, language communities, and living standards shape the lottery of birth.</strong>
</p>

<p align="center">
  <a href="#-türkçe">🇹🇷 Türkçe</a> ·
  <a href="#-english">🇬🇧 English</a>
</p>

![Birth Lottery ana ekranı / main screen](https://github.com/user-attachments/assets/6abc6e55-75b2-4cb6-a38a-02cc8351f169)

![Birth Lottery ayrıntı görünümü / detail view](https://github.com/user-attachments/assets/8956f50b-f018-4913-a419-02ade07f73a4)

---

## 🇹🇷 Türkçe

### Proje hakkında

Birth Lottery, bir kişinin belirli bir yılda seçtiği ülkede doğma olasılığını hesaplayan etkileşimli bir veri atlasıdır. Uygulama ayrıca resmî dil çevrelerine göre koşullu doğum dağılımı ve iki ülke arasında yaşam standardı karşılaştırması sunar.

### Özellikler

- Tarih, şehir ve ülkeye göre kişisel doğum olasılığı hesaplama
- Mouse veya dokunmayla döndürülebilen ve yakınlaştırılabilen etkileşimli dünya küresi
- Ülke adını hover ile görme ve ülkeye tıklayınca ayrıntılı bilgi kartını açma
- Türkçe ve İngilizce arayüz
- Koyu ve aydınlık tema
- Geçmiş yıllar için aynı yılın nüfusu ve kaba doğum oranıyla hesaplama
- Güncel tarihler için en son mevcut verilerle açıkça etiketlenmiş tahmin
- Fransızca gibi bir dilin resmî olduğu ülkeler arasında koşullu doğum dağılımı
- Gelir, yaşam beklentisi, internet kullanımı, kentleşme ve bebek ölümü karşılaştırması
- İkincil bir deney olarak rastgele doğum piyangosu
- Nüfus, resmî diller, başkent, telefon kodu, bayrak, kıta ve modern devlet/kuruluş tarihi içeren ülke kartları

### Teknolojiler

- **Frontend:** React, TypeScript, Vite, Three.js ve `react-globe.gl`
- **Backend:** FastAPI, Uvicorn ve HTTPX
- **Veri kaynakları:** World Bank, REST Countries ve Wikidata
- **Yayınlama:** Docker ve Render

### Yerelde çalıştırma

Projeyi klonlayın:

```bash
git clone https://github.com/fatmakaplan34/birth-lottery.git
cd birth-lottery
```

Projeyi yeni bir klasöre aldıysanız `.env.example` dosyasını `.env` olarak kopyalayın ve REST Countries anahtarınızı `RC_API_KEY` alanına yazın.

`COUNTRY_DATA_MODE=live` seçiliyken ülke referans bilgileri öncelikle dış API’den alınır. Anahtar eksik veya geçersizse ya da servis geçici olarak yanıt vermezse kürenin ve ülke seçiminin kaybolmaması için paket içindeki 252 ülkelik veri otomatik yedek olarak kullanılır. Doğum ve yaşam standardı hesaplamaları World Bank API verileriyle yapılmaya devam eder.

Güncelleme için mevcut proje klasörünü kullanıyorsanız çalışan `.env` dosyanızı koruyun. Güvenlik nedeniyle gerçek API anahtarı ZIP paketine veya GitHub deposuna eklenmez.

İki terminal açın. İlk terminalde proje kökünden backend’i başlatın:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8081
```

İkinci terminalde frontend’i başlatın:

```powershell
cd frontend
npm install
npm run dev
```

Ardından `http://localhost:5173` adresini açın. API belgeleri yerel geliştirme ortamında `http://127.0.0.1:8081/docs` adresindedir.

### Tek linkle yayınlama

Proje production ortamında tek Docker servisi olarak çalışır. Docker önce React arayüzünü derler, ardından FastAPI hem arayüzü hem API uçlarını aynı HTTPS adresinden sunar.

Render için hazır ayarlar `Dockerfile` ve `render.yaml` dosyalarındadır. GitHub ve Render adımları için [DEPLOYMENT.md](DEPLOYMENT.md) rehberini izleyin.

Production ortamında:

- Render’ın verdiği `PORT` değeri kullanılır.
- `/health` sağlık kontrolü uç noktası olarak açıktır.
- Swagger ve OpenAPI belgeleri dışarıya kapatılır.
- API anahtarı yalnızca Render environment variable olarak saklanır.
- Güvenlik ve HTTPS yönlendirmesiyle uyumlu response başlıkları eklenir.

### API uçları

- `GET /odds/birth?country=TUR&birth_date=2004-12-14&city=Ankara`
- `GET /odds/language?language=French&year=2026`
- `GET /odds/living-standards?country1=FRA&country2=COD&year=2026`
- `GET /countries/TUR/profile`

### Veri metodolojisi

Geçmiş yıl hesabında World Bank’in o yıla ait ülke nüfusu ile kaba doğum oranı çarpılır. Tam tarih kullanıcı bağlamı sağlar; kaynak veriler yıllık olduğu için olasılığı belirleyen kısım yıldır. Şehir bilgisi şimdilik yalnızca bağlam sağlar ve hesap ülke düzeyinde yapılır.

Güncel yıl için kesin yıllık veri henüz bulunmadığında uygulama en son mevcut nüfus ve doğum oranını kullanır ve sonucu **son veri tahmini** olarak etiketler.

Dil ekranı bir dili konuşan kişi sayısını hesaplamaz. Sonuç, seçilen dilin resmî olarak tanındığı ülkelerdeki tahmini doğumlar arasındaki koşullu dağılımdır. Arnavutça ve Türkçe gibi Türkçe dil adları İngilizce kaynak adlarıyla eşleştirilir. Tamazight, Amazigh, Berber ve bölgesel Tamazight adları aynı dil çevresinde birleştirilir.

Doğum oranı verisi bulunmayan Kosova gibi ülkeler gizlenmez; listede **doğum verisi yok** olarak gösterilir ve bu ülkeler için yüzde uydurulmaz.

Ülke kartlarındaki nüfus, telefon kodu ve genel ülke bilgileri REST Countries kaynağından gelir. Canlı servis kullanılamadığında ülke seçimi için yerel veri yedeği açılır; ülke profili görüntülenirken nüfus, World Bank’in erişilebilen en son kaydıyla güncellenir.

Modern devlet/bağımsızlık alanı, uygulamadaki 252 ülke ve bölgenin tamamını kapsayan yerel veri anlık görüntüsünden okunur. Ana kaynak Wikidata `P571` özelliğidir. `P571` kaydı bulunmayan bağımlı bölgeler, tartışmalı devletler ve özel ISO grupları resmî tarihçe veya statü kaynaklarıyla ayrıca tanımlanmıştır.

Tarihin yalnızca yıl düzeyinde bilindiği kayıtlarda yapay gün ve ay gösterilmez. Svalbard ve Jan Mayen gibi tek bir idari devlet oluşturmayan girdilerde uydurma bir tarih yerine neden birleşik bir kuruluş tarihi bulunmadığı açıklanır. Her ülke kartında kaynak bağlantısı bulunur; canlı Wikidata sorgusu yalnızca yerel anlık görüntüde bulunmayan gelecekteki yeni kayıtlar için yedek olarak kullanılır.

---

## 🇬🇧 English

### About the project

Birth Lottery is an interactive data atlas that calculates the probability of a person being born in a selected country during a specific year. The application also provides conditional birth distributions based on official-language communities and comparisons of living standards between two countries.

### Features

- Personal birth probability calculations based on a date, city, and country
- An interactive globe that can be rotated and zoomed using a mouse or touchscreen
- Country names displayed on hover and detailed country cards displayed on selection
- Turkish and English interfaces
- Dark and light themes
- Historical calculations using population and crude birth-rate data from the selected year
- Clearly labelled estimates based on the latest available data for current dates
- Conditional birth distributions among countries where a selected language, such as French, is officially recognised
- Comparisons of income, life expectancy, internet usage, urbanisation, and infant mortality
- A random birth lottery as an additional interactive experience
- Country cards showing population, official languages, capital, calling code, flag, continent, and modern-state/establishment date

### Tech stack

- **Frontend:** React, TypeScript, Vite, Three.js, and `react-globe.gl`
- **Backend:** FastAPI, Uvicorn, and HTTPX
- **Data sources:** World Bank, REST Countries, and Wikidata
- **Deployment:** Docker and Render

### Running locally

Clone the repository:

```bash
git clone https://github.com/fatmakaplan34/birth-lottery.git
cd birth-lottery
```

If you are setting up the project in a new folder, copy `.env.example` as `.env` and enter your REST Countries API key in the `RC_API_KEY` field.

When `COUNTRY_DATA_MODE=live` is enabled, country reference information is retrieved primarily from the external API. If the key is missing or invalid, or if the service temporarily fails to respond, the bundled dataset containing 252 countries is automatically used as a fallback so that the globe and country-selection features remain available. Birth probability and living-standard calculations continue to use World Bank API data.

If you are updating an existing project folder, preserve your working `.env` file. For security reasons, real API keys are never included in ZIP packages or committed to the GitHub repository.

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

Then open `http://localhost:5173`. In the local development environment, the API documentation is available at `http://127.0.0.1:8081/docs`.

### Single-link deployment

In production, the project runs as a single Docker service. Docker first builds the React interface, after which FastAPI serves both the interface and API endpoints from the same HTTPS address.

Deployment-ready configuration for Render is provided in the `Dockerfile` and `render.yaml` files. Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide for the GitHub and Render deployment steps.

In production:

- The `PORT` value provided by Render is used.
- `/health` is available as the health-check endpoint.
- Swagger UI and OpenAPI documentation are disabled publicly.
- The API key is stored only as a Render environment variable.
- Security response headers compatible with HTTPS deployment are enabled.

### API endpoints

- `GET /odds/birth?country=TUR&birth_date=2004-12-14&city=Ankara`
- `GET /odds/language?language=French&year=2026`
- `GET /odds/living-standards?country1=FRA&country2=COD&year=2026`
- `GET /countries/TUR/profile`

### Data methodology

For historical calculations, a country’s population in the selected year is multiplied by its crude birth rate for the same year using World Bank data. The full date provides user context; because the source data is annual, the year is the component that determines the probability. City information currently provides context only, and calculations are performed at the country level.

When final annual data is not yet available for the current year, the application uses the latest available population and birth-rate data and labels the result as a **latest-data estimate**.

The language section does not calculate the number of people who speak a language. Instead, it shows the conditional distribution of estimated births among countries where the selected language is officially recognised. Turkish language names such as Arnavutça and Türkçe are mapped to their English source names. Tamazight, Amazigh, Berber, and regional Tamazight names are grouped within the same language community.

Countries such as Kosovo, for which birth-rate data is unavailable, are not hidden. They are displayed with a **birth data unavailable** label, and no artificial percentage is assigned to them.

Population, calling codes, and general country information shown on country cards are obtained from REST Countries. If the live service is unavailable, the application uses its bundled country snapshot as a fallback for country selection. When a country profile is opened, its population is updated using the latest accessible World Bank record.

Modern-state and independence information for all 252 countries and territories is read from the application’s local data snapshot. The primary source is Wikidata property `P571`. Dependent territories, disputed states, and special ISO entities without a `P571` record are documented separately using official historical or political-status sources.

When only the year of an event is known, the application does not display an artificial day or month. For entries such as Svalbard and Jan Mayen, which do not constitute a single administrative state, the application explains why no unified establishment date is available instead of inventing one. Each country card includes a source link. Live Wikidata queries are used only as a fallback for future entries that are not present in the bundled snapshot.

---

<p align="center">
  Built with React and FastAPI.
</p>
