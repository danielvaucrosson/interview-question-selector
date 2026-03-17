---
name: question-generator
description: "Generate calibrated technical interview questions for a question bank. Use this skill whenever the user asks to create interview questions, add questions to the question bank, seed questions for a domain or technology, generate questions for a job posting, or fill gaps in the coverage matrix. Also trigger when the user says things like 'generate 10 questions for Snowflake', 'I need scenario questions for Data Engineering', 'add difficulty 3 questions', 'create questions based on this job description', or 'fill the gaps in my question bank'. This skill handles the full workflow - researching technical areas, generating questions with ideal answers, formatting to the schema, and writing them to the Excel question bank file."
---

# Question Generator Skill

## Purpose

Generate high-quality, calibrated technical interview questions and add them to the question bank Excel file. Each question follows a strict schema and is grounded in researched technical content.

## Workflow

### Step 1: Gather Inputs

Before generating, confirm these parameters with the user (use `ask_user_input_v0` when choices are bounded):

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| Domain(s) | Yes | — | One or more from the taxonomy |
| Technology | No | GEN | Specific tech or technology-agnostic |
| Difficulty levels | No | All (1-3) | Which levels to target |
| Question count | No | 10 per domain | How many to generate |
| Target role/posting | No | — | Job posting URL or description for calibration |
| Difficulty distribution | No | 3/4/3 | Split across levels 1/2/3 for a set of 10 |

If the user provides a job posting, fetch it with `web_fetch` and extract the relevant domains, technologies, and seniority level before generating.

### Step 2: Research

For each domain+technology combination, use `web_search` and `web_fetch` to research:

- Official documentation for the technology (e.g., Qlik Help, Microsoft Learn, Snowflake docs)
- Best practices and common patterns
- Known trade-offs and architectural decisions
- Real-world scenarios that consultants encounter

Research is essential for producing technically accurate answer keys. Do NOT generate questions from memory alone — always ground in current sources.

### Step 3: Generate Questions

Read `references/taxonomy.md` for valid domains, sub-domains, technologies, and codes.
Read `references/schema.md` for the exact question schema and formatting rules.
Read `references/examples.md` for calibration examples at each difficulty level.

Apply these generation rules:

**Question Type Distribution** (per 10 questions):
- Difficulty 1: Lean toward `definition` and `explanation` types
- Difficulty 2: Mix of `explanation` and `scenario` types
- Difficulty 3: Lean toward `scenario` types

**Answer Format** (STRICT):
- 3–5 bullets per question, no exceptions
- Each bullet UNDER 20 words
- Bullets start with `•` character
- Bullets are separated by `\n`
- No sub-bullets, no paragraphs, no prose

**Question ID Convention**: `{DOMAIN_CODE}-{TECH_CODE}-{SEQ}`
- Check the existing Excel file for the highest existing sequence number for that domain+tech combo
- Increment from there (e.g., if DV-QLK-003 exists, next is DV-QLK-004)

**Quality Checks** before finalizing:
- Every question must map to exactly one sub-domain from the taxonomy
- No two questions should test the same concept at the same difficulty level
- Scenario questions (difficulty 2-3) should reflect real consulting situations
- Technology-specific questions must include accurate, current technical details
- Answer bullets should describe what an ideal response *includes*, not the full answer itself

### Step 4: Write to Excel

After generating questions, write them to the question bank Excel file.

1. Check for the question bank file:
   - Look at `question-bank.xlsx` in the project root (`/sessions/nice-optimistic-ptolemy/mnt/Hiring/`)
   - If it doesn't exist, create a new template (see Step 4a below)

2. Load the workbook and find the next empty row in the "Questions" sheet

3. Write each question with proper formatting:
```python
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side

BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_CENTER = Alignment(wrap_text=True, vertical="top", horizontal="center")
THIN_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

# Column order: A=question_id, B=question, C=question_type, D=answer,
# E=domain, F=sub_domain, G=technology, H=other_skills, I=difficulty, J=tags
```

4. Save the workbook in-place at the project root and present with a computer:// link.

**Step 4a: Creating a new template** (only if no existing file found):
- Create workbook with three sheets: "Questions", "Taxonomy", "Coverage Matrix"
- Add headers with dark blue fill (1F3864), white bold Arial 11pt font
- Add data validations for question_type (definition/explanation/scenario), difficulty (1/2/3), and domain (all 8 domains)
- Add auto-filter and freeze panes on row 1
- Populate "Taxonomy" sheet with all domains, sub-domains, technologies, and skills from `references/taxonomy.md`

### Step 5: Summarize

After writing, provide a brief summary table:

```
Added X questions to the question bank:
| Domain | Technology | Diff 1 | Diff 2 | Diff 3 | Total |
|--------|-----------|--------|--------|--------|-------|
| ...    | ...       | ...    | ...    | ...    | ...   |
```

Do NOT list every question in the chat — the user can see them in the file.

## Edge Cases

- **Duplicate detection**: Before adding, scan existing question_id values. If the same domain+tech+seq already exists, increment the sequence.
- **Multi-technology questions**: Use the primary technology for the ID. List all relevant technologies in the technology field, comma-separated.
- **Soft-skill-only questions**: Use domain code `SK` with the skill code in the tech position (e.g., `SK-CM-001`).
- **Large batches**: If generating 20+ questions, research and write in batches of 10 per domain to avoid quality degradation.
