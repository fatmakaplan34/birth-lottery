# Birth Lottery

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
