---
name: create-video-style-skill
description: Create portable creator-specific copywriting skills from video sources. Use when the user wants Codex to learn a video or creator's script style from YouTube, Bilibili, or another yt-dlp-supported URL, extract or transcribe the source text, summarize the reusable style, and generate one independent research-first copywriting skill per style that can write new Chinese video scripts from a topic, question, product, trend, rough direction, or outline.
---

# Create Video Style Skill

Use this skill to build a new, portable "style copywriter" skill from a reference video or creator. The final generated skill must work without the original URL, subtitles, audio, or local transcript; it should carry only a reusable style card, writing workflow, output format, and self-check rules.

## Workflow

1. Create a temporary working folder outside the final skill directory.
2. Run `scripts/fetch_video_text.py` against the user's video or creator URL.
   - Prefer subtitles and auto-captions.
   - If no subtitle text is available, use the downloaded audio files listed in `transcription_request.json` and transcribe them with the best available local transcription route.
   - Keep transcripts temporary. Do not copy full transcripts into the generated style skill.
3. Read `references/style-card-schema.md` before analyzing style.
4. Produce a concise style card draft from the transcript material.
5. Show the user the draft style card, proposed skill name, intended use cases, and banned behaviors. Ask for confirmation or corrections before writing the final style skill.
6. After confirmation, save the style card to a temporary Markdown file and run `scripts/init_style_skill.py` to create the final style skill.
7. Validate both the generated style skill and this parent skill with the Skill Creator validator when practical.

## Style Extraction Rules

- Extract transferable writing behavior, not source facts.
- Preserve the creator's structural habits, pacing, tone, and rhetorical moves.
- Avoid storing full subtitles or long verbatim source passages in the generated skill.
- If short examples are useful, paraphrase them or keep them under copyright-safe limits.
- Separate "must imitate" traits from "do not imitate" traits, especially misinformation habits, sensitive claims, harassment, or unsafe persuasion.
- Make the generated style skill useful for new topics: describe how to adapt the style, not only how the original videos were structured.

## Generated Skill Requirements

Each generated style skill should:

- Have a lowercase hyphenated name, usually derived from the creator/channel name plus `copywriter`.
- Use ASCII-friendly wording in the final generated skill files when portability matters, even if the working analysis and user conversation happen in Chinese.
- Include only `SKILL.md` and `agents/openai.yaml` unless the user explicitly wants extra resources.
- Trigger when the user asks to research, write, rewrite, polish, or outline Chinese video scripts in that specific style.
- Accept a topic, question, product name, trend, or rough direction as the minimum input; an outline must be optional.
- Browse current web sources before drafting when the subject is time-sensitive, factual, comparative, or product-specific.
- Default to this output shape:
  1. Title suggestions
  2. Full video script
  3. Segment structure
  4. Source notes, when research was used
  5. Short style self-check
- Ask for missing topic, audience, target length, or outline only when the request cannot be completed responsibly with reasonable assumptions.
- Never claim to be the original creator and never imply endorsement by the creator.

## Scripts

Use the bundled scripts from this skill directory:

```powershell
python scripts/fetch_video_text.py --url "<video-or-creator-url>" --out "<temporary-work-dir>" --max-videos 3 --language zh
```

If the output contains `transcript.txt`, use it for style analysis. If it contains `transcription_request.json`, transcribe the listed audio files, write the cleaned transcript to the same work directory, then continue.

After the user confirms the style card:

```powershell
python scripts/init_style_skill.py --style-card "<confirmed-style-card.md>" --creator-name "<creator-name>" --output-dir "C:\Users\26270\.codex\skills"
```

Pass `--skill-name` when the user provides a preferred exact skill name.

## Failure Handling

- If `yt_dlp` is unavailable, tell the user the parent skill needs the Python `yt_dlp` package or the `yt-dlp` executable.
- If subtitles and audio download both fail, report the platform, URL, and error summary.
- If transcription tools are unavailable, stop after preparing `transcription_request.json` and ask the user to provide a transcript or enable a transcription route.
- If the target environment or validator is sensitive to local encodings, transliterate creator names and store the final skill instructions in ASCII-friendly wording for maximum portability.
- If the generated skill name already exists, do not overwrite it unless the user explicitly approves replacing it.
