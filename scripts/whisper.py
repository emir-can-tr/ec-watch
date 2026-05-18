#!/usr/bin/env python3
"""Transcribe a video using local Whisper (faster-whisper).

Uses faster-whisper for local transcription - no API key required.
Downloads the model automatically on first use.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def load_api_key(preferred: str | None = None) -> tuple[str | None, str | None]:
    """For local whisper, backend is always 'local', no API key needed."""
    return ("local", None)


def extract_audio(video_path: str, out_path: Path) -> Path:
    """Extract mono 16kHz wav — optimal for faster-whisper."""
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is not installed. Install with: brew install ffmpeg")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", str(Path(video_path).resolve()),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(out_path.resolve()),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg audio extraction failed: {result.stderr.strip()}")
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise SystemExit("ffmpeg produced no audio — video may have no audio track")
    return out_path


def transcribe_video(
    video_path: str,
    audio_out: Path,
    backend: str | None = None,
    api_key: str | None = None,
) -> tuple[list[dict], str]:
    """Run local transcription via faster-whisper.

    Returns (segments, "local"). Raises SystemExit on any failure.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit(
            "faster-whisper not installed. Install with: pip install faster-whisper"
        )

    print("[ec-watch] extracting audio for local Whisper…", file=sys.stderr)
    audio_path = extract_audio(video_path, audio_out)
    size_kb = audio_path.stat().st_size / 1024
    print(f"[ec-watch] audio: {size_kb:.0f} kB — transcribing with faster-whisper…", file=sys.stderr)

    # Use base model for balance of speed/accuracy, download if not cached
    model = WhisperModel("base", device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        str(audio_path),
        language=None,
        beam_size=5,
        vad_filter=True,
    )

    result = []
    for seg in segments:
        text = (seg.text or "").strip()
        if text:
            result.append({
                "start": round(float(seg.start), 2),
                "end": round(float(seg.end), 2),
                "text": text,
            })

    if not result:
        raise SystemExit("Whisper returned no transcript segments")

    print(
        f"[ec-watch] transcribed {len(result)} segments via local faster-whisper "
        f"(language: {info.language}, duration: {info.duration:.1f}s)",
        file=sys.stderr,
    )
    return result, "local"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: whisper.py <video-path> [<audio-out.wav>]", file=sys.stderr)
        raise SystemExit(2)

    video = sys.argv[1]
    audio_out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("audio.wav")

    segments, backend = transcribe_video(video, audio_out)
    print(json.dumps({"backend": backend, "segments": segments}, indent=2))