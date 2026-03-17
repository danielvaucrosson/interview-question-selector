# Question Schema Reference

## Required Fields

| Field | Type | Rules |
|-------|------|-------|
| `question_id` | string | Format: `{DOMAIN}-{TECH}-{SEQ}` — e.g., `DE-SNO-001` |
| `question` | string | Verbatim question text, ready to ask in an interview |
| `question_type` | enum | One of: `definition`, `explanation`, `scenario` |
| `answer` | string | 3–5 bullets describing ideal answer components |
| `domain` | enum | Full domain name (e.g., "Data Engineering") |
| `sub_domain` | string | Single sub-domain from the taxonomy |
| `difficulty` | int | 1, 2, or 3 |

## Optional Fields

| Field | Type | Rules |
|-------|------|-------|
| `technology` | string | Comma-separated tech codes (e.g., "SNO, SQL"). Use "GEN" if agnostic |
| `other_skills` | string | Comma-separated skill codes (e.g., "CM, TC"). Leave blank if none |
| `tags` | string | Comma-separated keywords for filtering |

## Question ID Convention

**Format:** `{DOMAIN}-{TECH}-{SEQ}`

| Segment | Rules | Example |
|---------|-------|---------|
| DOMAIN | 2-letter code from taxonomy | DE, DW, DV, DA, DS, AI, CL, AR |
| TECH | 3-letter code, or GEN if agnostic | SNO, PBI, QLK, GEN |
| SEQ | 3-digit zero-padded, sequential per domain+tech | 001, 002, 003 |

**Multi-tech questions:** Use the PRIMARY technology for the ID. List all in the technology field.

**Before assigning an ID:** Check the existing Excel for the highest sequence number for that domain+tech pair and increment.

## Question Type Definitions

| Type | What It Tests | Typical Patterns |
|------|--------------|-----------------|
| `definition` | Recall & understanding | "What is X?", "Define X", "Explain X" |
| `explanation` | Compare, contrast, reason about trade-offs | "Difference between X and Y?", "Why choose X over Y?", "Walk me through X" |
| `scenario` | Applied judgment, real-world problem solving | "Tell me about a time…", "Given this situation…", "A client asks you to…" |

## Answer Formatting Rules (STRICT)

1. Exactly 3–5 bullets per question
2. Each bullet UNDER 20 words
3. Bullets start with `•` character
4. Bullets separated by `\n`
5. No sub-bullets, no paragraphs, no prose
6. Bullets describe what an ideal response INCLUDES, not the full answer itself
7. First bullet should address the most fundamental aspect of the answer
8. Last bullet can be a "bonus" or "senior-level distinction" point

## Excel Column Order

When writing to the Questions sheet:

| Column | Field |
|--------|-------|
| A | question_id |
| B | question |
| C | question_type |
| D | answer |
| E | domain |
| F | sub_domain |
| G | technology |
| H | other_skills |
| I | difficulty |
| J | tags |
