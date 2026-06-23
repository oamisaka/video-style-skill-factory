# Style Card Schema

Use this schema when turning transcript material into a portable copywriting skill. Keep the card concise enough to live inside the generated `SKILL.md`.

## Required Fields

### Style identity
- `creator_or_style_name`: Creator, channel, or invented style name.
- `best_for`: Video categories this style fits.
- `not_for`: Topics or contexts where the style should not be used.
- `audience`: Expected viewer knowledge level, emotional state, and viewing context.

### Opening pattern
- Typical hook type: question, conflict, surprising claim, story, direct promise, or scene setup.
- First 15-second pacing: how quickly the script introduces stakes and payoff.
- Common opening moves to reuse.

### Structure pattern
- Usual macro-structure, such as hook -> setup -> evidence -> turn -> takeaway.
- Segment length and density.
- How the script moves between points.
- How examples, anecdotes, data, and opinions are sequenced.

### Voice and tone
- Persona: teacher, friend, critic, operator, storyteller, analyst, host, or hybrid.
- Emotional temperature: calm, sharp, excited, intimate, skeptical, humorous, dramatic.
- Degree of certainty: tentative, balanced, decisive, provocative.
- Relationship with viewer: peer, mentor, insider, challenger, companion.

### Sentence rhythm
- Average sentence length.
- Use of short punch lines, pauses, rhetorical questions, repetition, lists, or contrast.
- Spoken-language habits and filler patterns worth imitating.
- Formatting expectations for readable oral delivery.

### Rhetorical habits
- Favorite persuasion moves.
- How claims are supported.
- How objections are handled.
- How conflict, curiosity, and payoff are created.

### Ending pattern
- Typical conclusion shape.
- Call-to-action strength.
- Final emotional note.

### Must imitate
- 5 to 10 concrete style rules the generated skill must follow.

### Avoid
- 5 to 10 things the generated skill must not do.
- Include safety, accuracy, and copyright boundaries.

### Default output
- Title suggestions.
- Full script.
- Segment structure.
- Style self-check.

## Extraction Guidance

- Prefer patterns that appear across multiple sections or videos.
- Distinguish content preferences from writing style. A style skill should work on new topics.
- Do not preserve long source excerpts. Paraphrase style features instead.
- Mark uncertain conclusions as tentative when the source is short or noisy.
- If the source has both narration and dialogue, focus on the dominant script voice unless the user asks for dialogue writing.
- If a creator's style includes unsafe, hateful, deceptive, or impersonation-heavy behavior, transform it into a safe adjacent style rule.

## Markdown Template

```markdown
# <Creator Or Style Name> Copywriting Style Card

## Style Identity
- Best for:
- Not for:
- Audience:

## Opening Pattern

## Structure Pattern

## Voice And Tone

## Sentence Rhythm

## Rhetorical Habits

## Ending Pattern

## Must Imitate
- 

## Avoid
- 

## Default Output
- Title suggestions
- Full script
- Segment structure
- Style self-check
```
