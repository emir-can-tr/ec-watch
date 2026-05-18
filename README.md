# 🎬 /ec-watch — Claude Watches Videos

> **Give Claude the ability to watch any video.** Paste a URL or local path, ask a question — get answers grounded in what's actually on screen.

[![MIT License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-green.svg)](https://claude.ai)

```
/ec-watch https://youtu.be/dQw4w9WgXcQ what happens at the 30 second mark?
```

---

## ✨ What It Does

| Feature | Description |
|---------|-------------|
| **URL Support** | YouTube, Vimeo, TikTok, X, Loom, and 500+ other sites via `yt-dlp` |
| **Local Files** | `.mp4`, `.mov`, `.mkv`, `.webm`, `.avi` and more |
| **Auto-Scaled Frames** | Duration-aware frame extraction (2 fps max, 100 frames cap) |
| **Free Transcription** | Native captions first, local faster-whisper fallback (no API key) |
| **AI Analysis** | Reads each frame with multimodal AI, combines with transcript |

---

## 🚀 Quick Start

### Install

```bash
# Claude Code
/plugin install ec-watch

# Or from marketplace
/plugin marketplace add emir-can-tr/ec-watch
```

### Use

```bash
/ec-watch <url-or-path> [question]
```

### Examples

```bash
# Analyze a viral video
/ec-watch https://youtu.be/dQw4w9WgXcQ what hook did they open with?

# Diagnose a screen recording
/ec-watch ~/Downloads/bug-repro.mov what is going wrong?

# Summarize a long video
/ec-watch https://youtu.be/abc summarize the key points

# Focus on a specific section
/ec-watch https://youtu.be/xyz --start 2:15 --end 2:45
```

---

## 🔧 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. DOWNLOAD                                                │
│     yt-dlp fetches video → temp directory                   │
│     Captions extracted automatically (free)                  │
├─────────────────────────────────────────────────────────────┤
│  2. FRAME EXTRACTION                                        │
│     ffmpeg extracts frames at auto-scaled fps              │
│     Budget: ≤30s→30f, 30-60s→40f, 1-3min→60f, 3-10min→80f   │
├─────────────────────────────────────────────────────────────┤
│  3. TRANSCRIPTION                                           │
│     Native captions (free) or local faster-whisper          │
│     No API key required for transcription                   │
├─────────────────────────────────────────────────────────────┤
│  4. AI ANALYSIS                                             │
│     Claude reads each frame + transcript                    │
│     Answers grounded in visual + audio content              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Frame Budget

| Duration | Frames | Use Case |
|----------|--------|----------|
| ≤30s | ~30 | Dense — every key moment |
| 30s - 1min | ~40 | Still dense |
| 1 - 3min | ~60 | Comfortable |
| 3 - 10min | ~80 | Sparse but workable |
| >10min | 100 | Sparse scan — re-run focused |

Use `--start` / `--end` for denser coverage on specific sections.

---

## ⚙️ Options

| Flag | Default | Description |
|------|---------|-------------|
| `--start T` | - | Range start (SS, MM:SS, or HH:MM:SS) |
| `--end T` | - | Range end |
| `--max-frames N` | 80 | Lower frame cap (max 100) |
| `--resolution W` | 512 | Frame width in pixels |
| `--fps F` | auto | Override auto-fps (max 2 fps) |
| `--no-whisper` | - | Disable transcription (frames only) |

---

## 🔒 Privacy & Security

- **Local Processing** — Video downloaded to temp directory, audio transcribed locally
- **No Data Sent** — faster-whisper runs entirely on your machine
- **Auto-Cleanup** — Working directory deleted when done
- **No API Key Required** — Transcription works offline

---

## 📁 Project Structure

```
ec-watch/
├── SKILL.md              # Skill definition (Claude Code)
├── commands/
│   └── watch.md         # Slash command shim
├── scripts/
│   ├── watch.py         # Main orchestrator
│   ├── download.py      # yt-dlp wrapper
│   ├── frames.py        # ffmpeg frame extraction
│   ├── transcribe.py    # VTT + Whisper orchestration
│   ├── whisper.py       # Local faster-whisper client
│   └── setup.py         # Preflight + installer
└── hooks/
    └── SessionStart/    # Status hook
```

---

## 🛠️ Requirements

| Tool | Purpose | Install |
|------|---------|---------|
| `yt-dlp` | Video download | `brew install yt-dlp` / `winget install yt-dlp` |
| `ffmpeg` | Frame extraction | `brew install ffmpeg` / `winget install Gyan.FFmpeg` |
| `faster-whisper` | Local transcription | Auto-installed on first use |

---

## 🌐 Languages

> Read this in Turkish: [README_TR.md](README_TR.md)

---

## Credit

https://github.com/bradautomates/claude-video

---

## 📜 License

MIT License — see [LICENSE](LICENSE)
