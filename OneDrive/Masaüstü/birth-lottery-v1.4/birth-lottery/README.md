# Birth Lottery / Doğum Piyangosı

---

## 🇹🇷 Türkçe

### Doğum Piyangosı

Doğum Piyangosı, bir kişinin belirli bir yılda seçtiği ülkede doğma olasılığını
hesaplayan etkileşimli bir veri atlasıdır. Uygulama ayrıca resmî dil çevrelerine
göre koşullu doğum dağılımı ve iki ülke arasında yaşam standardı karşılaştırması
sunar.

### Neler var?

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

### Çalıştırma

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

### Yeni API Uçları

- `GET /odds/birth?country=TUR&birth_date=2004-12-14&city=Ankara`
- `GET /odds/language?language=French&year=2026`
- `GET /odds/living-standards?country1=FRA&country2=COD&year=2026`
- `GET /countries/TUR/profile`

### Veri Metodolojisi

Geçmiş yıl hesabında World Bank'in o yıla ait ülke nüfusu ile kaba doğum oranı
çarpılır. Tam tarih kullanıcı bağlamı sağlar; kaynak yıllık olduğu için olasılığı
belirleyen kısım yıldır. Şehir bilgisi de şimdilik yalnızca bağlamdır ve hesap
ülke düzeyinde yapılır.

Güncel yıl için henüz kesin yıllık veri bulunmadığında uygulama en son mevcut
nüfus ve doğum oranlarını kullanır ve sonucu "son veri tahmini" olarak etiketler.

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

---

## 🇬🇧 English

### Birth Lottery

Birth Lottery is an interactive data atlas that calculates the probability of a 
person being born in a selected country in a given year. The application also 
provides conditional birth distribution by official language environment and 
living standards comparison between two countries.

### Features

- Personal birth probability by date, city, and country
- Interactive globe for country selection that can be rotated and zoomed with mouse or touch
- Hover to see country names on the globe and click for detailed country card
- Turkish/English interface with dark/light theme
- For past years, calculation using that year's population and crude birth rate
- For current dates, clearly labeled forecast using the most recent available data
- Conditional probability among countries where a language like French is official
- Comparison of income, life expectancy, internet access, urbanization, and infant mortality
- Secondary experimental feature: current random birth lottery
- Random draw result card showing population, language, capital, phone code, continent, and 
  establishment/modern state date

### Running the Application

If you're extracting the project to a new folder, copy the `.env.example` file as `.env` 
and add your REST Countries API key to the `RC_API_KEY` field. When `COUNTRY_DATA_MODE=live` 
is set, country reference data is primarily fetched from this external API. If the key is 
missing/invalid or the service is temporarily unavailable, a built-in backup of 252 countries 
is used to prevent the globe and country selection from being completely lost. Birth probability 
and living standards calculations continue to use World Bank external API data.

If you're using an existing project folder for updates, preserve your working `.env` file; 
for security reasons, actual API keys are not included in the ZIP package.

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

Then open `http://localhost:5173`. API documentation is available at
`http://127.0.0.1:8081/docs`.

### New API Endpoints

- `GET /odds/birth?country=TUR&birth_date=2004-12-14&city=Ankara`
- `GET /odds/language?language=French&year=2026`
- `GET /odds/living-standards?country1=FRA&country2=COD&year=2026`
- `GET /countries/TUR/profile`

### Data Methodology

For historical year calculations, the application multiplies World Bank's country population 
for that year by the crude birth rate. The full date provides user context; since the source 
data is annual, the year is the factor that determines probability. City information is 
currently context only; calculations are performed at the country level.

When exact annual data is not yet available for the current year, the application uses the 
most recent available population and birth rate, labeling the result as "latest data estimate".

The language screen does not calculate number of speakers. The result is the conditional 
distribution among estimated births in countries where the selected language is officially 
recognized. Turkish language names like Albanian/Turkish are matched with English source names. 
Tamazight, Amazigh, Berber, and regional Tamazight names are consolidated under the same 
language environment. Countries like Kosovo without birth rate data are not hidden; they are 
listed as "no birth data" and no percentages are generated for them.

Population, phone code, and country information in country cards come from the REST Countries 
source. When the live service is unavailable, local data backup is used for country selection; 
when viewing the card profile, population is updated with World Bank's most recent accessible 
record. The modern state/independence field is read from a local data snapshot for all 252 
countries and territories in the application. The primary source is Wikidata P571; dependent 
territories, disputed states, and special ISO groupings without P571 records are separately 
defined using official history or status sources. For records where the date is only known 
at the year level, artificial day and month are not shown. For entries like Svalbard and 
Jan Mayen that do not form a single administrative state, a status explanation is provided 
instead of a fabricated date. Each card includes source links; live Wikidata queries are 
used only as a backup for future new records not in the local snapshot.
