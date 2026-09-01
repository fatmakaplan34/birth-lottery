# Birth Lottery yayınlama rehberi

Bu sürümde frontend ve backend tek Docker servisi olarak yayınlanır. Kullanıcı
yalnızca Render'ın verdiği `https://...onrender.com` adresini açar.

## 1. GitHub deposu

1. GitHub'da `birth-lottery` adında yeni bir depo oluşturun.
2. İlk yayın için depoyu `Private` seçebilirsiniz.
3. Proje kökünde aşağıdaki komutları çalıştırın:

```powershell
git init
git add .
git commit -m "Prepare Birth Lottery for deployment"
git branch -M main
git remote add origin GITHUB_REPO_ADRESINIZ
git push -u origin main
```

`git status` çıktısında `.env` görünmemelidir. API anahtarını GitHub'a kesinlikle
göndermeyin.

## 2. Render'a bağlama

1. Render hesabında **New > Blueprint** seçin.
2. GitHub hesabınızı bağlayıp `birth-lottery` deposunu seçin.
3. Render kökteki `render.yaml` dosyasını algılar.
4. `RC_API_KEY` sorulduğunda anahtarı Render ekranına girin.
5. **Deploy Blueprint** ile kurulumu başlatın.

Render Dockerfile ile önce React arayüzünü oluşturur, sonra FastAPI servisini
`PORT` ortam değişkeninde çalıştırır. Sağlık kontrolü `/health` adresidir.

## 3. Yayın sonrası kontrol

- Ana adreste arayüz açılmalı ve dünya görünmelidir.
- `/health` adresi `status: alive` döndürmelidir.
- Ülke profili, tarihsel doğum hesabı, dil dağılımı, yaşam karşılaştırması ve
  rastgele çekiliş ayrı ayrı denenmelidir.
- Production ortamında `/docs` kapalı olmalıdır.
- Tarayıcı adres çubuğunda HTTPS görünmelidir.

## 4. Domain

İlk testleri Render'ın ücretsiz `onrender.com` adresinde tamamlayın. Domaini
daha sonra Render servisindeki **Settings > Custom Domains** bölümünden
ekleyebilirsiniz. DNS doğrulamasından sonra TLS sertifikasını Render yönetir.
