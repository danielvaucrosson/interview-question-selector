# Interview Question Selector — Design

## Purpose

Streamlit app to filter and select interview questions from `question-bank.xlsx` based on domain, technology, difficulty, and other criteria. Export selected questions to Excel for use in interviews.

## Data Source

`question-bank.xlsx` — 100 questions across 3 sheets:
- **Questions**: ID, question, type, answer, domain, sub_domain, technology, other_skills, difficulty (1-3), tags, review_notes
- **Taxonomy**: reference data for domains, technologies, skills, difficulty labels
- **Coverage Matrix**: summary statistics (read-only, not used by app)

## Layout

### Sidebar — Filters
- **Domain** multi-select (8 domains: Data Engineering, Data Visualization, etc.)
- **Sub-domain** multi-select (dynamically filtered by selected domains)
- **Technology** multi-select (individual tech codes: QLK, PBI, SQL, SNO, etc.)
- **Difficulty** checkboxes (1=Foundational, 2=Applied, 3=Architectural)
- **Question type** multi-select (definition, explanation, scenario)
- **Max questions** slider (5–30, default 15)

### Main Area
1. Filtered results table — columns: ID, question (truncated), domain, tech, difficulty, type
2. Per-row checkbox selection
3. "Select All Visible" / "Clear Selection" buttons
4. Selected questions panel — expandable cards with full question + answer + metadata
5. Export button — download selected questions as Excel

## Filter Logic

- **Between categories**: AND (domain AND tech AND difficulty)
- **Within a category**: OR (PBI OR QLK)
- **Multi-tech questions**: "QLK, PBI" matches if user selects either QLK or PBI
- **Sub-domain**: options update dynamically based on selected domains

## Export Format

Excel (.xlsx) with columns: question_id, question, answer, domain, sub_domain, technology, difficulty, question_type, tags

## Tech Stack

- `streamlit` — UI framework
- `pandas` + `openpyxl` — read Excel
- `xlsxwriter` — write export Excel
- No LLM, no external APIs

## Non-Goals

- No file uploads (JD/resume)
- No AI-powered question recommendation
- No PDF export
- No persistent state / database
