# Video Style Skill Factory

Create portable Codex copywriting skills from video sources.

This repository contains a parent skill, `create-video-style-skill`, that helps Codex learn the script style of a reference video or creator, summarize the transferable writing pattern, and generate one independent research-first copywriting skill per style.

The generated style skills are designed to work without the original video URL, subtitles, audio, or transcript. They keep only a reusable style card, research workflow, writing workflow, output format, and safety guardrails.

## What This Is

- A Codex skill for creating creator-specific or style-specific copywriting skills.
- A workflow for extracting subtitles first, then falling back to audio transcription when subtitles are unavailable.
- A template generator for portable research-first copywriting skills.
- An example generated skill and example script output.

## What This Is Not

- It is not a transcript archive.
- It is not a tool for impersonating a creator.
- It does not include original subtitles, audio, or copyrighted scripts from reference videos.
- It does not imply endorsement by any creator, channel, or brand used in examples.

## Repository Structure

```text
video-style-skill-factory/
  create-video-style-skill/
    SKILL.md
    agents/openai.yaml
    scripts/
      fetch_video_text.py
      init_style_skill.py
    references/
      style-card-schema.md
  examples/
    yingshi-jufeng-copywriter/
      SKILL.md
      agents/openai.yaml
    outputs/
      benda-black-flag-600-yingshi-jufeng-script.md
  LICENSE
  README.md
```

## How It Works

1. Provide a video URL, playlist URL, channel URL, or creator URL.
2. The parent skill fetches available subtitles with `yt_dlp`.
3. If subtitles are unavailable, it downloads audio and prepares a transcription request.
4. Codex analyzes the temporary transcript material and drafts a concise style card.
5. After confirmation, the parent skill generates a portable copywriting skill for that style.
6. The generated skill can write new Chinese video scripts from only a topic, question, product, trend, rough direction, or outline.

## Requirements

- Codex with skill support.
- Python 3.10 or newer.
- `yt_dlp` Python package or `yt-dlp` availability through the Python environment.
- A transcription route such as Whisper when subtitle extraction fails.

## Install

Copy `create-video-style-skill/` into your Codex skills directory, usually:

```text
~/.codex/skills/create-video-style-skill
```

On Windows, this is commonly:

```text
C:\Users\<you>\.codex\skills\create-video-style-skill
```

Then invoke it from Codex:

```text
Use $create-video-style-skill to learn a creator's video style from this URL and create a reusable copywriting skill.
```

## Example

The `examples/yingshi-jufeng-copywriter/` folder shows a generated style skill. It is included as a demonstration of the output shape.

The `examples/outputs/benda-black-flag-600-yingshi-jufeng-script.md` file shows an AI-generated script output from that generated skill.

Before publishing any generated script, re-check time-sensitive facts, prices, release status, and technical specifications against current sources.

## Safety And Copyright Notes

- Keep transcripts temporary.
- Do not store full subtitles or long verbatim passages inside generated skills.
- Extract style patterns, not source text.
- Generated skills should never claim to be the original creator.
- Generated scripts should not imply endorsement by the original creator.
- Treat creator names in examples as descriptive references, not branding or affiliation.

## License

MIT. See `LICENSE`.
