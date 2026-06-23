#!/usr/bin/env python3
"""Create a portable creator-specific copywriting skill from a style card."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str, fallback: str = "creator") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or fallback


def normalize_skill_name(skill_name: str | None, creator_name: str) -> str:
    if skill_name:
        base = slugify(skill_name, "style-copywriter")
    else:
        base = f"{slugify(creator_name, 'creator')}-copywriter"
    if not base.endswith("copywriter"):
        base = f"{base}-copywriter"
    return base[:63].strip("-") or "style-copywriter"


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_skill_md(skill_name: str, creator_name: str, style_card: str) -> str:
    safe_creator = creator_name.strip() or skill_name
    description = (
        f"Write, rewrite, research, outline, and polish Chinese video scripts in the portable {safe_creator} style. "
        "Use when the user provides a topic, question, product, trend, or rough direction, with or without an outline, and wants Codex to research current information, build the angle, compare related subjects, and draft a style-consistent video script."
    )
    return f"""---
name: {skill_name}
description: {yaml_quote(description)}
---

# {safe_creator} Copywriter

Use this skill to write new Chinese video scripts in the style captured below. Treat the style card as a reusable writing system, not as source material to quote. Do not claim to be the original creator, imply endorsement, or copy long phrases from reference videos.

## Inputs

Minimum viable input: a topic, question, product name, trend, or rough direction. An outline is optional.

If the user does not provide every field, make reasonable assumptions and state them briefly:

- Topic or core claim
- Optional outline or key points
- Target audience
- Target length or platform
- Desired intensity, such as sharper, warmer, denser, or more conversational

Default assumptions when unspecified:

- Chinese spoken video script.
- 6 to 10 minute explainer or documentary-style video.
- Audience: curious general viewers with some interest in the subject.
- Goal: make the viewer understand why this topic matters, not just what happened.

## Research-First Mode

Use this mode whenever the user gives only a topic, question, product, market direction, or a time-sensitive subject. Do the research before drafting.

Research targets:

- Current status: launch date, availability, price, model names, official claims, and what is still uncertain.
- Core facts: specs, configuration, mechanism, use cases, and constraints.
- Comparison set: predecessor, direct rivals, adjacent alternatives, and one or two broader reference points when useful.
- Viewer stakes: why an ordinary viewer or potential buyer should care.
- Bigger question: what this case says about the industry, creators, consumers, or technology.

Source rules:

- For specs, prices, release status, and official positioning, prefer manufacturer pages, launch materials, verified official accounts, filings, or reputable media reports.
- Use forums, social platforms, short videos, and comments only for sentiment, questions, and user pain points; do not treat them as hard facts without confirmation.
- For current or upcoming products, browse the web and compare source dates. Do not rely on memory.
- If sources conflict, say so briefly and build the script around the uncertainty instead of hiding it.
- Do not invent numbers, prices, release dates, weights, horsepower, torque, battery specs, or fuel specs.
- Include a compact source note with the final answer when web research was used.

Research-to-script workflow:

1. Turn the user direction into one central viewer question.
2. Build a short research brief: what is known, what is interesting, what is uncertain, what comparisons matter.
3. Choose the style angle: object-first, scene-first, problem-first, or contradiction-first.
4. Create the segment plan before drafting.
5. Draft the script in style, keeping research facts visible but not list-like.

## Writing Workflow

1. Infer the video's viewer promise and emotional payoff from the topic or research brief.
2. Build a segment plan that follows the style card's structure pattern.
3. Draft the script in spoken Chinese with readable paragraph breaks.
4. Preserve the style's rhythm and rhetorical habits while adapting facts to the new topic.
5. Add title suggestions, segment structure, source notes when researched, and a short style self-check.

## Default Output

1. Title suggestions
2. Full script
3. Segment structure
4. Source notes, when research was used
5. Style self-check

## Style Card

{style_card.strip()}

## Guardrails

- Keep factual claims grounded. If a claim is uncertain, soften it or flag it.
- Do not include full transcript excerpts from reference videos.
- Do not imitate harmful, deceptive, hateful, or privacy-invasive behavior.
- Do not present the generated script as the original creator's words.
"""


def build_openai_yaml(skill_name: str, creator_name: str) -> str:
    display = f"{creator_name.strip() or skill_name} Copywriter"
    short = "Research and write Chinese video scripts in a captured creator style"
    prompt = f"Use ${skill_name} to research this topic or question and write a Chinese video script in this captured style."
    return (
        "interface:\n"
        f"  display_name: {yaml_quote(display)}\n"
        f"  short_description: {yaml_quote(short)}\n"
        f"  default_prompt: {yaml_quote(prompt)}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style-card", required=True, help="Confirmed Markdown style card.")
    parser.add_argument("--creator-name", required=True, help="Creator or style display name.")
    parser.add_argument("--skill-name", help="Optional exact skill name. Normalized to lowercase hyphen case.")
    parser.add_argument(
        "--output-dir",
        default=str(Path.home() / ".codex" / "skills"),
        help="Directory that will contain the generated skill folder.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing generated skill folder.")
    args = parser.parse_args()

    style_card_path = Path(args.style_card).expanduser().resolve()
    if not style_card_path.exists():
        raise SystemExit(f"Style card not found: {style_card_path}")
    style_card = style_card_path.read_text(encoding="utf-8")
    if not style_card.strip():
        raise SystemExit("Style card is empty.")

    skill_name = normalize_skill_name(args.skill_name, args.creator_name)
    output_dir = Path(args.output_dir).expanduser().resolve()
    skill_dir = output_dir / skill_name

    if skill_dir.exists() and not args.overwrite:
        raise SystemExit(f"Skill already exists: {skill_dir}. Re-run with --overwrite only after user approval.")

    skill_dir.mkdir(parents=True, exist_ok=True)
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    (skill_dir / "SKILL.md").write_text(
        build_skill_md(skill_name, args.creator_name, style_card),
        encoding="utf-8",
    )
    (agents_dir / "openai.yaml").write_text(
        build_openai_yaml(skill_name, args.creator_name),
        encoding="utf-8",
    )

    print(str(skill_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
