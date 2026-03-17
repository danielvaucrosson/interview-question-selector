---
name: question-reviewer
description: "Review and quality-check the question bank for schema compliance, difficulty calibration, and duplicate detection. Use this skill whenever the user asks to review questions, audit the question bank, check question quality, validate questions, find duplicates, check difficulty calibration, or run QA on the question bank. Also trigger when the user says things like 'review my questions', 'are there any duplicates?', 'check the difficulty levels', 'audit the question bank', 'validate the Excel', or 'run quality checks'. This skill reads the question bank Excel file, performs automated and judgment-based checks, writes review notes to a new column in the Excel, and summarizes findings in the chat."
---

# Question Reviewer Skill

## Purpose

Perform quality assurance on the question bank Excel file. Identifies schema violations, difficulty miscalibration, and duplicate/overlapping questions. Outputs findings both as a summary in the chat and as a "review_notes" column appended to the Excel.

## When to Use

- After generating a batch of new questions
- Before sharing the question bank with interviewers
- Periodically as the bank grows to catch drift
- When the user explicitly asks for a review or QA pass

## Workflow

### Step 1: Load the Question Bank

1. Check for the file at `question-bank.xlsx` in the project root (`/sessions/nice-optimistic-ptolemy/mnt/Hiring/`)
2. Load with openpyxl and read all rows from the "Questions" sheet
3. Count total questions and report: "Reviewing X questions across Y domains"

### Step 2: Schema Compliance Checks (Automated)

Run these checks on every row. Flag violations in the review_notes column.

#### Required Field Checks
- `question_id`: Must exist and follow format `{2-letter domain}-{3-letter tech}-{3-digit seq}`
- `question`: Must exist and be non-empty
- `question_type`: Must be exactly one of: `definition`, `explanation`, `scenario`
- `answer`: Must exist and be non-empty
- `domain`: Must be one of the 8 valid domains (see references/taxonomy.md)
- `sub_domain`: Must exist and be a valid sub-domain for the specified domain
- `difficulty`: Must be 1, 2, or 3

#### Answer Format Checks
- Must have 3-5 bullets (count lines starting with `•`)
- Each bullet should be under 20 words (flag if over, but don't hard-fail — some technical bullets legitimately run long)
- No sub-bullets or nested formatting

#### ID Convention Checks
- Domain code in the ID must match the domain field (e.g., ID starts with "DV" but domain says "Data Engineering" = violation)
- No duplicate question_ids across the entire sheet
- Sequence numbers should be zero-padded to 3 digits

#### Cross-Field Consistency
- Technology field should use valid codes from the taxonomy (TAB, QLK, PBI, SNO, etc.)
- If `other_skills` is populated, codes should be valid (SD, PM, CM, etc.)
- `question_type` should roughly align with difficulty:
  - Difficulty 1 questions that are `scenario` type = flag as "unusual — verify intentional"
  - Difficulty 3 questions that are `definition` type = flag as "unusual — verify intentional"

### Step 3: Difficulty Calibration Review (Judgment-Based)

For each question, assess whether the labeled difficulty matches the actual cognitive demand. Use these criteria from the taxonomy:

| Level | What It Should Test | Red Flags |
|-------|-------------------|-----------|
| 1 | Recall, definitions, core concepts | Question requires comparing trade-offs or designing a solution |
| 2 | Comparing approaches, trade-offs, solving defined problems | Question is pure recall OR requires open-ended architecture design |
| 3 | Designing solutions, navigating ambiguity, defending decisions | Question has a single correct answer or tests recall only |

**Calibration heuristics:**
- Definition questions are typically difficulty 1 (flag if labeled 2 or 3)
- Scenario questions with client dynamics, ambiguity, or multi-stakeholder complexity are typically difficulty 3
- "Compare X and Y" or "what are the trade-offs" questions are typically difficulty 2
- Questions starting with "Design...", "Architect...", or "A client has [complex situation]..." are typically difficulty 3

Write a calibration note only for questions where the labeled difficulty seems mismatched. Format: `CALIBRATION: Labeled {X}, suggest {Y} — {reason}`

### Step 4: Duplicate and Overlap Detection (Judgment-Based)

Scan all questions for conceptual overlap. Two questions overlap if:
- They test the same core concept at the same difficulty level (even with different wording)
- They cover the same technology-specific topic with only minor variation
- One question is a strict subset of another (e.g., Q1 asks "What is X?" and Q2 asks "What is X and how does it compare to Y?" — Q1 is a subset)

**Do NOT flag as duplicates:**
- Same concept at different difficulty levels (that's intentional progression)
- Same technology but different sub-domains
- Conceptually related but testing distinct skills

Format: `OVERLAP: Similar to {other_question_id} — {brief reason}`

### Step 5: Write Review Notes to Excel

Add or update column K ("review_notes") in the Questions sheet:

```python
# Add header if not present
if ws.cell(row=1, column=11).value != "review_notes":
    ws.cell(row=1, column=11, value="review_notes")
    # Apply header styling to match existing headers

# For each row, concatenate all findings
# If no issues found, write "PASS"
# If issues found, write all flags separated by " | "
```

Example review_notes values:
- `PASS`
- `SCHEMA: Answer has 6 bullets (max 5) | CALIBRATION: Labeled 1, suggest 2 — question requires trade-off comparison`
- `OVERLAP: Similar to DV-PBI-002 — both test Power BI RLS design`

### Step 6: Summarize in Chat

After writing to Excel, provide a concise summary:

```
## Question Bank Review — {date}

**Reviewed:** {N} questions across {M} domains

### Schema Compliance
- ✅ {X} questions passed all checks
- ⚠️ {Y} questions have issues:
  - {count} answer format violations (bullet count or length)
  - {count} ID convention issues
  - {count} missing or invalid fields
  - {count} cross-field inconsistencies

### Difficulty Calibration
- {X} questions may be miscalibrated:
  - {list each with ID, current level, suggested level, reason}

### Duplicate/Overlap Detection
- {X} potential overlaps found:
  - {list each pair with IDs and reason}

### Coverage Summary
{Table showing count by domain × difficulty}
```

Do NOT reproduce the full question text in the chat summary — just IDs, levels, and brief reasons.

### Step 7: Present Updated File

Save the workbook in-place at the project root and present with a computer:// link.

## Edge Cases

- **Empty rows**: Skip rows where question_id is empty
- **Large banks (100+)**: Process in batches to maintain quality of judgment-based checks
- **Partial reviews**: If user asks to review only a specific domain or batch, filter accordingly
- **Pre-existing review_notes**: Overwrite with fresh results on each review run
