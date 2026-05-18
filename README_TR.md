# 🎬 /ec-watch — Claude Videoları İzler

> **Claude'a herhangi bir videoyu izleme yeteneği verin.** Bir URL veya yerel dosya yolu yapıştırın, soru sorun — ekranda ne olduğuna dayalı cevaplar alın.

[![MIT Lisansı](https://img.shields.io/badge/Lisans-MIT-purple.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-green.svg)](https://claude.ai)

```
/ec-watch https://youtu.be/dQw4w9WgXcQ 30. saniyede ne oluyor?
```

---

## ✨ Ne Yapar

| Özellik | Açıklama |
|---------|-------------|
| **URL Desteği** | YouTube, Vimeo, TikTok, X, Loom ve 500+ diğer site `yt-dlp` ile |
| **Yerel Dosyalar** | `.mp4`, `.mov`, `.mkv`, `.webm`, `.avi` ve fazlası |
| **Otomatik Kareler** | Süreye göre kare çıkarma (max 2 fps, 100 kare limiti) |
| **Ücretsiz Transkripsiyon** | Önce native altyazılar, sonra yerel faster-whisper (API anahtarı gerekmez) |
| **AI Analizi** | Her kareyi multimodal AI ile okur, transkriptle birleştirir |

---

## 🚀 Hızlı Başlangıç

### Kurulum

```bash
# Claude Code
/plugin install ec-watch

# Veya marketplace'den
/plugin marketplace add emir-can-tr/ec-watch
```

### Kullanım

```bash
/ec-watch <url-veya-dosya-yolu> [soru]
```

### Örnekler

```bash
# Viral bir videoyu analiz et
/ec-watch https://youtu.be/dQw4w9WgXcQ ne tür bir açılış kullandılar?

# Ekran kaydından hatayı teşhis et
/ec-watch ~/Downloads/hata-kaydi.mov ne yanlış gidiyor?

# Uzun bir videoyu özetle
/ec-watch https://youtu.be/abc önemli noktaları özetle

# Belirli bir bölüme odaklan
/ec-watch https://youtu.be/xyz --start 2:15 --end 2:45
```

---

## 🔧 Nasıl Çalışır

```
┌─────────────────────────────────────────────────────────────┐
│  1. İNDİRME                                                │
│     yt-dlp video çeker → geçici dizin                       │
│     Altyazılar otomatik çıkarılır (ücretsiz)               │
├─────────────────────────────────────────────────────────────┤
│  2. KARE ÇIKARMA                                           │
│     ffmpeg kareleri otomatik fps ile çıkarır               │
│     Bütçe: ≤30sn→30k, 30-60sn→40k, 1-3dk→60k, 3-10dk→80k│
├─────────────────────────────────────────────────────────────┤
│  3. TRANSKRİPSİYON                                         │
│     Native altyazılar (ücretsiz) veya yerel faster-whisper  │
│     Transkripsiyon için API anahtarı gerekmez               │
├─────────────────────────────────────────────────────────────┤
│  4. AI ANALİZİ                                             │
│     Claude her kareyi + transkripti okur                    │
│     Cevaplar görsel + ses içeriğine dayalı                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Kare Bütçesi

| Süre | Kareler | Kullanım |
|------|---------|----------|
| ≤30sn | ~30 | Yoğun — her ana an |
| 30sn - 1dk | ~40 | Hâlâ yoğun |
| 1 - 3dk | ~60 | Rahat |
| 3 - 10dk | ~80 | Seyrek ama kullanılabilir |
| >10dk | 100 | Seyrek tarama — odaklı yeniden çalıştır |

Belirli bölümler için `--start` / `--end` kullan.

---

## ⚙️ Seçenekler

| Bayrak | Varsayılan | Açıklama |
|--------|------------|----------|
| `--start S` | - | Başlangıç zamanı (SS, DD:SS veya SS:DD:SS) |
| `--end S` | - | Bitiş zamanı |
| `--max-frames N` | 80 | Kare limiti (max 100) |
| `--resolution G` | 512 | Kare genişliği (piksel) |
| `--fps F` | otomatik | fps'i ez (max 2 fps) |
| `--no-whisper` | - | Transkripsiyonu kapat (sadece kareler) |

---

## 🔒 Gizlilik & Güvenlik

- **Yerel İşleme** — Video geçici dizine indirilir, ses yerel olarak transkribe edilir
- **Veri Gönderilmez** — faster-whisper tamamen makinenizde çalışır
- **Otomatik Temizlik** — İşlem bitince çalışma dizini silinir
- **API Anahtarı Gerekmez** — Transkripsiyon çevrimdışı çalışır

---

## 📁 Proje Yapısı

```
ec-watch/
├── SKILL.md              # Skill tanımı (Claude Code)
├── commands/
│   └── watch.md         # Slash komut shim
├── scripts/
│   ├── watch.py         # Ana orkestratör
│   ├── download.py      # yt-dlp sarmalayıcı
│   ├── frames.py        # ffmpeg kare çıkarma
│   ├── transcribe.py    # VTT + Whisper yönetimi
│   ├── whisper.py       # Yerel faster-whisper istemcisi
│   └── setup.py         # Ön kontrol + kurulum
└── hooks/
    └── SessionStart/    # Durum hook'u
```

---

## 🛠️ Gereksinimler

| Araç | Amaç | Kurulum |
|------|------|---------|
| `yt-dlp` | Video indirme | `brew install yt-dlp` / `winget install yt-dlp` |
| `ffmpeg` | Kare çıkarma | `brew install ffmpeg` / `winget install Gyan.FFmpeg` |
| `faster-whisper` | Yerel transkripsiyon | İlk kullanımda otomatik kurulur |

---

## 🌐 Diller

> Read this in English: [README.md](README.md)

---

## Kaynak

https://github.com/bradautomates/claude-video

---

## 📜 Lisans

MIT Lisansı — bkz. [LICENSE](LICENSE)
