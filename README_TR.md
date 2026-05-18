# /ec-watch — Claude Videoları İzler

**Claude'a herhangi bir videoyu izleme yeteneği verin.**

```
/ec-watch <url-veya-dosya-yolu> [soru]
```

Kurulum gerektirmez — `yt-dlp` ve `ffmpeg` ilk çalıştırmada kurulur. Altyazılar çoğu public video için ücretsizdir. Yerel faster-whisper transkripsiyonu için API anahtarı gerekmez.

---

## Neden Var

Claude bir web sayfasını okuyabilir, bir komut çalıştırabilir, bir repo'ya göz atabilir. Ancak yapamadığı şey, videoları *izlemektir*. Bir YouTube linki yapıştırdığınızda, ya başlıktan tahmin etmesi gerekir ya da ekrandakilerin %90'ını kaçıran bir transkript alır.

`/ec-watch` ile bir URL veya yerel dosya yolu yapıştırın, bir soru sorun. Claude video indirir, kareleri otomatik ölçekli hızda çıkarır, zaman damgalı bir transkript alır ve her kareyi analiz eder. Cevap verdiğinde, video'yu *görmüş* ve sesi *duymuş* olur.

```
/ec-watch https://youtu.be/dQw4w9WgXcQ 30. saniyede ne oluyor?
```

## Ne Yapabilirsiniz

**İçerik yapısını analiz edin.** Viral bir video URL'si yapıştırın ve "Ne tür bir açılış kullandılar?" diye sorun. Claude ilk karelere bakar, açılış transkriptini okur, yapıyı analiz eder.

**Ekran kayıtlarından hata teşhisi yapın.** Size bozuk bir şeyin ekran kaydını gönderirler. `/ec-watch hata-kaydi.mov ne yanlış gidiyor?` Claude kaydı izler, sorunlu kareyi bulur.

**Videoları özetleyin.** `/ec-watch https://youtu.be/<video> bunu özetle` — yapıyı, önemli anları, söylenenleri çıkarır.

## Nasıl Çalışır

1. **Bir video ve soru yapıştırın.** URL (YouTube, Vimeo, TikTok, X, Loom, + yüzlerce site) veya yerel dosya (`.mp4`, `.mov`, `.mkv`, `.webm`).
2. **`yt-dlp` onu indirir.** URL'ler için geçici dizin. Yerel dosyalar için indirme yok — doğrudan işlenir.
3. **`ffmpeg` kareleri otomatik ölçekli hızda çıkarır.** Süreye göre kare bütçesi: ≤30sn ~30 kare, 30-60sn ~40, 1-3dk ~60, 3-10dk ~80, uzun videolar 100 kare. Sabit limitler: 2 fps, 100 kare.
4. **Transkript altyazılardan veya yerel Whisper'dan.** Önce native altyazılar (ücretsiz). Yoksa yerel faster-whisper — API anahtarı gerekmez.
5. **Claude kareleri + transkripti analiz eder.** Ekranda ne varsa ve ses ne diyorsa ona dayalı cevap verir.

## Kurulum

### Claude Code

```
/plugin install ec-watch
```

Marketplace üzerinden:
```
/plugin marketplace add emir-can-tr/ec-watch
```

### Manuel Kurulum

```bash
git clone https://github.com/emir-can-tr/ec-watch.git ~/.claude/skills/ec-watch
```

## İlk Çalıştırma

İlk çalıştırmada `setup.py` otomatik olarak çalışır:
- `ffmpeg` ve `yt-dlp` kontrolü — eksikse kurulum komutlarını yazdırır
- Yerel Whisper ayarı (ilk kullanımda modeli otomatik indirir)
- Transkripsiyon için API anahtarı gerekmez

## Kullanım

```
/ec-watch <url-veya-dosya-yolu> [soru]
```

Odaklı mod — daha yoğun kare bütçesi, daha düşük token maliyeti:
```
/ec-watch https://youtu.be/abc --start 2:15 --end 2:45
/ec-watch video.mp4 --start 50 --end 60
```

Seçenekler:
- `--start S` / `--end S` — belirli bir bölüme odaklan
- `--max-frames N` — kare limitini düşür
- `--resolution G` — kare genişliği (varsayılan 512, ekrandaki metin için 1024'e çıkar)
- `--fps F` — otomatik fps'i ez (max 2 fps)
- `--no-whisper` — transkripsiyonu kapat (sadece kareler)

## Gereksinimler

- `yt-dlp` — video indirme
- `ffmpeg` — kare çıkarma
- `faster-whisper` — yerel transkripsiyon (modeli otomatik indirir)

yt-dlp ve ffmpeg kurulumu:
```bash
# macOS
brew install yt-dlp ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install yt-dlp ffmpeg

# Windows
winget install yt-dlp ffmpeg
```

## Yapı

```
.
├── SKILL.md              # Skill tanımı
├── scripts/
│   ├── watch.py         # Ana orkestratör
│   ├── download.py      # yt-dlp sarmalayıcı
│   ├── frames.py        # ffmpeg kare çıkarma
│   ├── transcribe.py    # VTT + Whisper yönetimi
│   ├── whisper.py       # Whisper istemcileri
│   └── setup.py         # Ön kontrol + kurulum
├── commands/
│   └── watch.md         # Slash komut shim
└── hooks/
    └── SessionStart/    # Durum hook'u
```

## Lisans

MIT — bkz. [LICENSE](LICENSE)
