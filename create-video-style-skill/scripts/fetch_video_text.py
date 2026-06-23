#!/usr/bin/env python3
"""Fetch subtitle text or audio from a video/creator URL for style analysis."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SUBTITLE_EXTENSIONS = {".vtt", ".srt", ".ass", ".ttml", ".srv1", ".srv2", ".srv3", ".json3"}
AUDIO_EXTENSIONS = {".m4a", ".mp3", ".opus", ".ogg", ".webm", ".wav", ".aac", ".flac"}


def import_yt_dlp():
    try:
        import yt_dlp  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on host environment
        raise SystemExit(
            "Missing dependency: install the Python package 'yt_dlp' or run from an environment that provides it."
        ) from exc
    return yt_dlp


def slugify(value: str, fallback: str = "video-style") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        value = fallback
    # Skill names must be ASCII lowercase, digits, and hyphens. Keep a simple
    # romanization-free fallback when the creator name is non-ASCII.
    ascii_value = re.sub(r"[^a-z0-9-]+", "", value)
    ascii_value = re.sub(r"-+", "-", ascii_value).strip("-")
    return ascii_value or fallback


def detect_source_kind(info: dict[str, Any]) -> str:
    if info.get("_type") in {"playlist", "multi_video"} or info.get("entries"):
        return "creator_or_playlist"
    return "single_video"


def get_metadata(yt_dlp: Any, url: str, max_videos: int) -> dict[str, Any]:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
        "playlistend": max_videos,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if not info:
        return {"source_url": url, "source_kind": "unknown"}

    creator = (
        info.get("uploader")
        or info.get("channel")
        or info.get("playlist_uploader")
        or info.get("title")
        or "video-style"
    )
    title = info.get("title") or creator
    suggested = f"{slugify(str(creator))}-copywriter"
    return {
        "source_url": url,
        "source_kind": detect_source_kind(info),
        "creator_name": creator,
        "title": title,
        "suggested_skill_name": suggested,
        "entry_count_seen": len(info.get("entries") or []),
    }


def clean_subtitle_text(raw: str, suffix: str) -> str:
    lines: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line in {"WEBVTT", "Kind: captions", "Language: en", "Language: zh"}:
            continue
        if re.match(r"^\d+$", line):
            continue
        if "-->" in line:
            continue
        if suffix == ".json3":
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\{\\.*?\}", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)

    deduped: list[str] = []
    previous = ""
    for line in lines:
        if line != previous:
            deduped.append(line)
        previous = line
    return "\n".join(deduped)


def subtitle_sort_key(path: Path) -> tuple[int, str]:
    name = path.name.lower()
    if ".zh" in name or ".chi" in name or ".cn" in name:
        priority = 0
    elif ".en" in name:
        priority = 1
    else:
        priority = 2
    return (priority, name)


def collect_subtitle_text(work_dir: Path) -> tuple[str, list[str]]:
    subtitle_files = sorted(
        [p for p in work_dir.rglob("*") if p.is_file() and p.suffix.lower() in SUBTITLE_EXTENSIONS],
        key=subtitle_sort_key,
    )
    chunks: list[str] = []
    used: list[str] = []
    for path in subtitle_files:
        if path.suffix.lower() == ".json3":
            # yt-dlp can emit json3 when no vtt conversion is available. Avoid
            # fragile partial parsing here and let the agent decide whether to
            # inspect it manually.
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        text = clean_subtitle_text(raw, path.suffix.lower())
        if text:
            chunks.append(f"[Source: {path.name}]\n{text}")
            used.append(str(path))
    return "\n\n".join(chunks).strip(), used


def download_subtitles(yt_dlp: Any, url: str, out_dir: Path, max_videos: int, language: str) -> None:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": [language, "zh-Hans", "zh-CN", "zh", "en"],
        "subtitlesformat": "vtt/srt/best",
        "playlistend": max_videos,
        "outtmpl": str(out_dir / "%(playlist_index|)s%(title).80s-%(id)s.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


def download_audio(yt_dlp: Any, url: str, out_dir: Path, max_videos: int) -> list[str]:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "format": "bestaudio/best",
        "playlistend": max_videos,
        "outtmpl": str(out_dir / "%(playlist_index|)s%(title).80s-%(id)s.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    audio_files = sorted(
        str(p) for p in out_dir.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    )
    return audio_files


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Video, playlist, channel, or creator URL.")
    parser.add_argument("--out", required=True, help="Temporary output directory.")
    parser.add_argument("--max-videos", type=int, default=3, help="Maximum videos to sample from a creator URL.")
    parser.add_argument("--language", default="zh", help="Preferred subtitle language code.")
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    source_dir = out_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    yt_dlp = import_yt_dlp()
    metadata = get_metadata(yt_dlp, args.url, args.max_videos)
    metadata.update({"max_videos": args.max_videos, "preferred_language": args.language})

    download_subtitles(yt_dlp, args.url, source_dir, args.max_videos, args.language)
    transcript, subtitle_files = collect_subtitle_text(source_dir)

    if transcript:
        transcript_path = out_dir / "transcript.txt"
        transcript_path.write_text(transcript, encoding="utf-8")
        metadata.update(
            {
                "status": "transcript_ready",
                "transcript_path": str(transcript_path),
                "subtitle_files": subtitle_files,
                "need_audio_transcription": False,
            }
        )
        write_json(out_dir / "source_metadata.json", metadata)
        print(str(transcript_path))
        return 0

    audio_files = download_audio(yt_dlp, args.url, source_dir, args.max_videos)
    metadata.update(
        {
            "status": "audio_downloaded" if audio_files else "failed",
            "audio_files": audio_files,
            "need_audio_transcription": bool(audio_files),
            "transcription_request_path": str(out_dir / "transcription_request.json"),
        }
    )
    write_json(out_dir / "source_metadata.json", metadata)
    write_json(
        out_dir / "transcription_request.json",
        {
            "audio_files": audio_files,
            "language": args.language,
            "write_transcript_to": str(out_dir / "transcript.txt"),
            "note": "Transcribe these audio files, clean the text, then continue style extraction. Do not copy raw transcript into the final style skill.",
        },
    )

    if audio_files:
        print(str(out_dir / "transcription_request.json"))
        return 2

    print("No subtitles or audio could be downloaded. See source_metadata.json.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
