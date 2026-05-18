# /ec-watch — Claude Watches Videos

**Give Claude the ability to watch any video.**

```
/ec-watch <url-or-path> [question]
```

Zero config to start — `yt-dlp` and `ffmpeg` install on first run. Captions cover most public videos for free. Local faster-whisper transcription requires no API key.

---

## Why This Exists

Claude can read a webpage, run a script, browse a repo. What it can't do, out of the box, is *watch a video*. You paste a YouTube link and it has to either guess from the title or pull a transcript that's missing 90% of what's on screen.

With `/ec-watch` you paste a URL or local path, ask a question, and Claude downloads the video, extracts frames at an auto-scaled rate, pulls a timestamped transcript, and analyzes each frame. By the time it answers, it has *seen* the video and *heard* the audio.

```
/ec-watch https://youtu.be/dQw4w9WgXcQ what happens at the 30 second mark?
```

## What You Can Do

**Analyze content structure.** Paste a viral video URL and ask "what hook did they open with?" Claude looks at the first frames, reads the opening transcript, breaks down the structure.

**Diagnose bugs from screen recordings.** Someone sends you a screen recording of something broken. `/ec-watch bug-repro.mov what's going wrong?` Claude watches the recording, finds the issue frame.

**Summarize videos.** `/ec-watch https://youtu.be/<video> summarize this` — pulls structure, key moments, what was actually said.

## How It Works

1. **You paste a video and a question.** URL (YouTube, Vimeo, TikTok, X, Loom, + hundreds more) or local path (`.mp4`, `.mov`, `.mkv`, `.webm`).
2. **`yt-dlp` downloads it.** For URLs into a temp directory. For local files, no download — just probed in place.
3. **`ffmpeg` extracts frames at an auto-scaled rate.** Duration-aware frame budget: ≤30s gets ~30 frames, 30-60s gets ~40, 1-3min gets ~60, 3-10min gets ~80, longer gets 100. Hard ceilings: 2 fps, 100 frames.
4. **Transcript from captions or local Whisper.** Native captions first (free). Fallback to local faster-whisper — no API key needed.
5. **Claude analyzes frames + transcript.** Answers grounded in what's actually on screen and in the audio.

## Installation

### Claude Code

```
/plugin install ec-watch
```

Or via marketplace:
```
/plugin marketplace add emir-can-tr/ec-watch
```

### Manual Install

```bash
git clone https://github.com/emir-can-tr/ec-watch.git ~/.claude/skills/ec-watch
```

## First Run

On first run, `setup.py` runs automatically:
- Checks for `ffmpeg` and `yt-dlp` — prints install commands if missing
- Sets up local Whisper (auto-downloads model on first use)
- No API key required for transcription

## Usage

```
/ec-watch <url-or-path> [question]
```

Focused mode — denser frame budget, lower token cost:
```
/ec-watch https://youtu.be/abc --start 2:15 --end 2:45
/ec-watch video.mp4 --start 50 --end 60
```

Options:
- `--start T` / `--end T` — focus on a section
- `--max-frames N` — lower frame cap
- `--resolution W` — frame width (default 512, bump to 1024 for on-screen text)
- `--fps F` — override auto-fps (max 2 fps)
- `--no-whisper` — disable transcription (frames only)

## Requirements

- `yt-dlp` — video download
- `ffmpeg` — frame extraction
- `faster-whisper` — local transcription (auto-installs model)

Install yt-dlp and ffmpeg:
```bash
# macOS
brew install yt-dlp ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install yt-dlp ffmpeg

# Windows
winget install yt-dlp ffmpeg
```

## Structure

```
.
├── SKILL.md              # Skill definition
├── scripts/
│   ├── watch.py         # Main orchestrator
│   ├── download.py      # yt-dlp wrapper
│   ├── frames.py        # ffmpeg frame extraction
│   ├── transcribe.py    # VTT + Whisper orchestration
│   ├── whisper.py       # Whisper clients
│   └── setup.py         # Preflight + installer
├── commands/
│   └── watch.md         # Slash command shim
└── hooks/
    └── SessionStart/    # Status hook
```

## License

MIT — see [LICENSE](LICENSE)
