---
name: coverage-matrix
description: "Generate and populate the coverage matrix for the question bank. Use this skill whenever the user asks to see coverage, find gaps, check what's missing, update the coverage matrix, show the coverage summary, identify which domains or technologies need more questions, or analyze the distribution of questions. Also trigger when the user says things like 'show me the gaps', 'what's missing in the question bank?', 'update the coverage matrix', 'where do I need more questions?', 'show coverage by technology', or 'which difficulty levels are underrepresented?'. This skill reads the question bank Excel, computes counts across multiple dimensions (domain, sub-domain, technology, difficulty, question type), populates the Coverage Matrix sheet in the Excel, and presents a gap analysis summary in the chat with prioritized recommendations."
---

# Coverage Matrix Skill

## Purpose

Analyze the question bank for coverage across all taxonomy dimensions, populate the Coverage Matrix sheet in the Excel, and surface gaps with prioritized recommendations for where to generate next.

## When to Use

- After adding a batch of new questions
- When planning which domain/technology to seed next
- When preparing interview question sets for a specific role
- When the user asks about gaps, coverage, or distribution

## Workflow

### Step 1: Load the Question Bank

1. Check for the file at `question-bank.xlsx` in the project root (`/sessions/nice-optimistic-ptolemy/mnt/Hiring/`)
2. Load with openpyxl and read all rows from the "Questions" sheet
3. Parse each row into a structured record with all fields

### Step 2: Compute Coverage Counts

Build these cross-tabulations from the data:

#### Matrix 1: Domain × Difficulty
- Rows: Each domain (8 domains)
- Columns: Difficulty 1, Difficulty 2, Difficulty 3, Total
- This is the primary coverage view

#### Matrix 2: Domain × Sub-Domain
- Rows: Each domain
- Sub-rows: Each sub-domain within that domain
- Columns: Count, Difficulty spread (1/2/3)
- Highlights which sub-domains have zero coverage

#### Matrix 3: Technology Coverage
- Rows: Each technology code that appears in the bank
- Columns: Count, Domains covered, Difficulty spread
- Note: a question with "QLK, PBI" counts toward both technologies

#### Matrix 4: Question Type Distribution
- Rows: Each domain
- Columns: definition, explanation, scenario, Total
- Helps ensure good type mix per domain

### Step 3: Populate the Coverage Matrix Sheet

Write results to the "Coverage Matrix" sheet in the Excel workbook. If the sheet already has data, clear it first and rewrite.

**Layout:**

```
Row 1: "Coverage Matrix — Generated {date}" (merged across columns, bold)
Row 2: blank
Row 3: "DOMAIN × DIFFICULTY" section header
Row 4: Column headers (domain, sub_domain, technology, diff_1_count, diff_2_count, diff_3_count, total)
Row 5+: Data rows
... blank row ...
Next section: "TECHNOLOGY COVERAGE" header
... data rows ...
... blank row ...
Next section: "QUESTION TYPE DISTRIBUTION" header
... data rows ...
... blank row ...
Next section: "GAP ANALYSIS" header
... gap rows ...
```

**Formatting:**
- Section headers: Bold, dark blue fill (1F3864), white text
- Column headers: Bold, medium blue fill (2E75B6), white text
- Data cells: Arial 10pt, thin borders, wrap text
- Zero-count cells: Red fill (FFC7CE) to highlight gaps
- Totals row: Bold, light gray fill (F2F2F2)

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import date

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
SUBHEADER_FILL = PatternFill("solid", fgColor="2E75B6")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=11)
SUBHEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=10)
BODY_FONT = Font(name="Arial", size=10)
BOLD_FONT = Font(name="Arial", bold=True, size=10)
ZERO_FILL = PatternFill("solid", fgColor="FFC7CE")
TOTAL_FILL = PatternFill("solid", fgColor="F2F2F2")
THIN_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)
```

### Step 4: Gap Analysis

Identify and rank gaps by priority. A "gap" is any combination that has zero or very few questions relative to what's expected.

**Gap Categories:**

1. **Empty domains** — Any domain with 0 questions (critical)
2. **Empty sub-domains** — Sub-domains within populated domains that have 0 questions (high)
3. **Missing difficulty levels** — A domain that has questions but is missing an entire difficulty level (high)
4. **Technology gaps** — Technologies in the taxonomy that have 0 questions (medium)
5. **Type imbalance** — A domain where >70% of questions are a single type (low)
6. **Thin coverage** — A domain with fewer than 5 questions total (medium)

Write gap rows to the Coverage Matrix sheet in a dedicated "GAP ANALYSIS" section:

| Priority | Gap Type | Domain | Detail | Recommendation |
|----------|----------|--------|--------|----------------|
| CRITICAL | Empty domain | Data Science | 0 questions | Generate 10 questions |
| HIGH | Empty sub-domain | DE / Streaming & Real-Time | 0 questions | Add 2-3 questions |
| HIGH | Missing difficulty | DV | No difficulty 3 questions | Add 3 scenario questions |
| MEDIUM | Technology gap | KFK (Kafka) | 0 questions | Add if relevant to roles |

### Step 5: Summarize in Chat

Present a concise summary covering:

1. **Overall stats**: Total questions, domains covered, technologies represented
2. **Domain × Difficulty table** (compact)
3. **Top 5 gaps** ranked by priority
4. **Recommendation**: Which domain/technology/difficulty to generate next

Format as a clean table — do NOT dump the full matrix into the chat. The user can see the detail in the Excel.

### Step 6: Present Updated File

Save the workbook in-place at the project root and present with a computer:// link.

## Edge Cases

- **Empty question bank**: Report "No questions found" and recommend starting with the question-generator skill
- **Single domain**: Still generate full matrix showing empty rows for other domains
- **Multi-technology questions**: Count toward each technology listed (e.g., "QLK, PBI" adds 1 to both)
- **Custom questions without sub-domains**: Flag as "Uncategorized" in the matrix
