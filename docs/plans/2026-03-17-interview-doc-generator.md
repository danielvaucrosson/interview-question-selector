# Interview Document Generator — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the existing single-page question selector into a multi-page Streamlit workflow that collects interview metadata, filters/selects questions, organizes them into sections, validates difficulty distribution, and generates a formatted .docx interview document.

**Architecture:** Multi-page Streamlit app using `pages/` directory convention. Shared logic extracted into `lib/` modules. The existing `app.py` becomes a home/landing page. Each workflow step maps to a Jira task (IQS-2 through IQS-8) and a separate page file. The docx engine is a standalone module that accepts structured data and returns a BytesIO buffer.

**Tech Stack:** streamlit 1.51+, pandas 2.0+, openpyxl 3.1+, python-docx 1.1+

**Jira Mapping:**
- IQS-2 → Task 1 (Metadata form) → `pages/1_Metadata.py`
- IQS-3 → Task 2 (Job profile presets) → `pages/2_Questions.py`
- IQS-4 → Task 3 (Section assignment) → `pages/3_Sections.py`
- IQS-5 → Task 4 (Difficulty summary) → `pages/4_Review.py`
- IQS-6 → Task 5 (Docx engine) → `lib/docx_engine.py`
- IQS-7 → Task 6 (Evaluation template) → extends `lib/docx_engine.py`
- IQS-8 → Task 7 (Integration & polish) → `pages/5_Generate.py` + wiring

---

### Task 1: Extract shared data module and set up multi-page structure (IQS-2 prep)

**Files:**
- Create: `lib/__init__.py`
- Create: `lib/data.py`
- Modify: `app.py` (slim down to landing page)
- Modify: `requirements.txt` (add python-docx)

**Step 1: Create `lib/__init__.py`**

```python
# empty — marks lib as a package
```

**Step 2: Create `lib/data.py` — shared data loading and constants**

Extract from `app.py` into a reusable module:

```python
import streamlit as st
import pandas as pd
from pathlib import Path

EXCEL_PATH = Path(__file__).resolve().parent.parent / "question-bank.xlsx"

TECH_LABELS = {
    "TAB": "Tableau", "QLK": "Qlik", "PBI": "Power BI", "SNO": "Snowflake",
    "FAB": "Fabric", "AWS": "AWS", "AZR": "Azure", "GCP": "GCP",
    "DBR": "Databricks", "DBT": "dbt", "AIR": "Airflow", "SPK": "Spark",
    "KFK": "Kafka", "SQL": "SQL", "PY": "Python", "TFM": "Terraform",
    "GIT": "Git", "LKR": "Looker", "GEN": "General",
}

DIFF_LABELS = {1: "1 — Foundational", 2: "2 — Applied", 3: "3 — Architectural"}

DIFF_COLORS = {
    0: {"label": "Intro", "hex": "#2E75B6"},
    1: {"label": "Foundational", "hex": "#70AD47"},
    2: {"label": "Applied", "hex": "#ED7D31"},
    3: {"label": "Architectural", "hex": "#C00000"},
}

SENIORITY_LEVELS = ["Junior", "Mid", "Semi Senior", "Senior", "Expert/Technical Lead", "Manager/Director"]


@st.cache_data
def load_questions() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="Questions")
    df = df[df["question_id"].notna()].copy()
    df["tech_list"] = df["technology"].fillna("").str.split(r",\s*")
    df["diff_label"] = df["difficulty"].map(DIFF_LABELS)
    return df
```

**Step 3: Slim down `app.py` to a landing page**

Replace the full content of `app.py` with a home page that imports from `lib/data.py` and shows a welcome screen with navigation hints. Keep `st.set_page_config(page_title="Interview Question Selector", layout="wide")`.

The landing page should show:
- App title
- Brief instructions: "Use the sidebar to navigate through the workflow"
- Step overview: 1. Metadata → 2. Questions → 3. Sections → 4. Review → 5. Generate

**Step 4: Update `requirements.txt`**

Add `python-docx>=1.1.0` to requirements.

**Step 5: Run to verify multi-page skeleton works**

Run: `streamlit run app.py`
Expected: Landing page renders. Sidebar shows page navigation (even if pages are empty stubs).

**Step 6: Commit**

```bash
git add lib/ app.py requirements.txt
git commit -m "refactor: extract shared data module, set up multi-page structure"
```

---

### Task 2: Candidate & Interview Metadata Input Form (IQS-2)

**Files:**
- Create: `pages/1_Metadata.py`

**Step 1: Create `pages/1_Metadata.py`**

```python
import streamlit as st
from datetime import date

st.set_page_config(page_title="Interview Metadata", layout="wide")
st.title("Interview Metadata")
st.caption("Enter candidate and interview details. All fields marked * are required.")

# Initialize session state defaults
defaults = {
    "meta_candidate": "",
    "meta_date": date.today(),
    "meta_interviewer": "",
    "meta_job_title": "",
    "meta_company": "Keyrus",
    "meta_seniority": "Mid",
    "meta_duration": "60 min",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

col1, col2 = st.columns(2)

with col1:
    st.text_input("Candidate Name *", key="meta_candidate")
    st.date_input("Interview Date *", key="meta_date")
    st.text_input("Interviewer Name *", key="meta_interviewer")

with col2:
    st.text_input("Job Title / Role *", key="meta_job_title")
    st.text_input("Company / Business Unit", key="meta_company")
    st.selectbox("Seniority Level", SENIORITY_LEVELS, key="meta_seniority")
    st.text_input("Estimated Duration", key="meta_duration")

# Validation
required = ["meta_candidate", "meta_interviewer", "meta_job_title"]
missing = [k.replace("meta_", "").replace("_", " ").title() for k in required if not st.session_state.get(k)]

if missing:
    st.warning(f"Required fields missing: {', '.join(missing)}")
else:
    st.success("Metadata complete — proceed to Questions page.")
```

Import `SENIORITY_LEVELS` from `lib.data` at the top.

**Step 2: Run to verify form renders and validation works**

Run: `streamlit run app.py`
Navigate to "Metadata" page.
Expected: Form renders with all fields. Warning shows for empty required fields. Success shows when all filled.

**Step 3: Commit**

```bash
git add pages/1_Metadata.py
git commit -m "feat(IQS-2): add candidate & interview metadata input form"
```

---

### Task 3: Smart Question Filtering with Job Profile Presets (IQS-3)

**Files:**
- Create: `pages/2_Questions.py`
- Create: `config/job_profiles.json`

**Step 1: Create `config/job_profiles.json`**

Define 3-4 starter presets:

```json
{
  "BI & Analytics Consultant — Qlik/PBI": {
    "domains": ["Data Visualization", "Data Analysis"],
    "technologies": ["QLK", "PBI", "SQL"],
    "difficulty_weights": {"Junior": [1, 1, 2], "Mid": [1, 2, 2], "Senior": [2, 2, 3], "Expert/Technical Lead": [2, 3, 3]}
  },
  "Data Engineer — Snowflake/dbt": {
    "domains": ["Data Engineering", "Data Warehousing"],
    "technologies": ["SNO", "DBT", "SQL", "PY"],
    "difficulty_weights": {"Junior": [1, 1, 2], "Mid": [1, 2, 2], "Senior": [2, 2, 3], "Expert/Technical Lead": [2, 3, 3]}
  },
  "Cloud Data Architect": {
    "domains": ["Data Architecture", "Cloud & Infrastructure", "Data Engineering"],
    "technologies": ["AWS", "AZR", "GCP", "SNO", "DBR", "TFM"],
    "difficulty_weights": {"Junior": [1, 1, 2], "Mid": [1, 2, 2], "Senior": [2, 2, 3], "Expert/Technical Lead": [2, 3, 3]}
  },
  "Data Scientist — Python/ML": {
    "domains": ["Data Science", "AI / ML Engineering", "Data Analysis"],
    "technologies": ["PY", "SPK", "SQL"],
    "difficulty_weights": {"Junior": [1, 1, 2], "Mid": [1, 2, 2], "Senior": [2, 2, 3], "Expert/Technical Lead": [2, 3, 3]}
  }
}
```

The `difficulty_weights` array maps to [Foundational, Applied, Architectural] — higher number = more questions at that level.

**Step 2: Create `pages/2_Questions.py`**

This page combines the existing filter sidebar with the new job profile preset feature. Port the existing filter + selection logic from `app.py` into this page, and add a profile selector at the top of the sidebar that auto-populates filters.

Key behavior:
- `st.sidebar.selectbox("Job Profile Preset", ["(None)", ...profiles])` at the top
- When a profile is selected, auto-set domain, technology, and difficulty filters
- Manual overrides remain available
- Selection state (`selected_ids`) persists in `st.session_state`
- The existing table layout (checkbox, ID, question, domain, tech, difficulty, type) is preserved

**Step 3: Run to verify filtering and presets work**

Run: `streamlit run app.py`
Navigate to "Questions" page.
Expected: Profile selector at top of sidebar. Selecting a profile auto-fills filters. Checkboxes work for question selection.

**Step 4: Commit**

```bash
git add pages/2_Questions.py config/job_profiles.json
git commit -m "feat(IQS-3): add job profile presets and question filtering page"
```

---

### Task 4: Question Ordering & Section Assignment (IQS-4)

**Files:**
- Create: `pages/3_Sections.py`

**Step 1: Create `pages/3_Sections.py`**

This page lets the user organize selected questions into named sections:

Key features:
- Show all selected questions (from `st.session_state.selected_ids`)
- Default sections: "Introduction", "Core Technical", "Architecture & Design", "Communication & Client", "Closing"
- Drag questions between sections using `st.selectbox` per question (assign to section)
- Add/remove/rename sections
- Add custom questions (not from bank) with a form: question text, answer key, pseudo-ID
- Reorder questions within each section using up/down buttons
- Store result in `st.session_state.sections` as a list of dicts:
  ```python
  [
      {
          "title": "INTRODUCTION (5 MIN)",
          "subtitle": "Let the candidate settle in...",
          "questions": [{"id": "INTRO-001", "question": "...", "answer": "...", ...}]
      },
      ...
  ]
  ```

**Step 2: Run to verify section assignment works**

Run: `streamlit run app.py`
Expected: Selected questions appear. User can assign to sections, reorder, add custom questions.

**Step 3: Commit**

```bash
git add pages/3_Sections.py
git commit -m "feat(IQS-4): add question ordering and section assignment page"
```

---

### Task 5: Difficulty Distribution Summary & Validation (IQS-5)

**Files:**
- Create: `pages/4_Review.py`

**Step 1: Create `pages/4_Review.py`**

This page shows the finalized question set with distribution analysis:

Key features:
- Difficulty distribution bar: colored pills/badges showing count per level
  - Use `st.markdown` with inline CSS for colored badges
  - Colors from `DIFF_COLORS` in `lib/data.py`
- Total question count and estimated duration (assume ~5 min per question)
- Seniority warning: compare distribution to expected weights from profile
  - E.g., Senior role with >50% Foundational questions → orange warning
- Section-by-section breakdown showing questions in final order
- Expandable question details (question + answer + metadata)
- "Looks good — proceed to generate" button that sets `st.session_state.review_complete = True`

**Step 2: Run to verify distribution display and warnings work**

Run: `streamlit run app.py`
Expected: Distribution bar renders with correct colors/counts. Warnings show for skewed distributions.

**Step 3: Commit**

```bash
git add pages/4_Review.py
git commit -m "feat(IQS-5): add difficulty distribution summary and validation page"
```

---

### Task 6: Docx Generation Engine (IQS-6)

**Files:**
- Create: `lib/docx_engine.py`

**Step 1: Create `lib/docx_engine.py`**

Port the interview-prep-template.js formatting to Python using `python-docx`. The function signature:

```python
def generate_interview_docx(metadata: dict, sections: list[dict]) -> BytesIO:
    """
    Generate a formatted interview document.

    Args:
        metadata: dict with keys: candidate_name, interview_date, interviewer,
                  job_title, company, seniority, duration, question_count
        sections: list of dicts, each with keys: title, subtitle, questions
                  Each question dict has: id, question, answer, subdomain,
                  technology, difficulty, question_type

    Returns:
        BytesIO buffer containing the .docx file
    """
```

Document structure to reproduce (matching JS template exactly):

1. **Cover page:**
   - Large title: "Interview Question Set" (Arial 24pt, dark blue)
   - Job title subtitle (Arial 14pt, med blue)
   - Company — Seniority line (Arial 12pt, gray)
   - Candidate info table (5 rows: Candidate, Date, Interviewer, Questions, Duration)
   - Difficulty distribution summary line

2. **Question sections** (page break before first section):
   - Section header: dark blue (#1F3864) background, white text, Arial 12pt bold
   - Section subtitle: italic, Arial 9.5pt
   - Per question:
     - Metadata table: 5 columns (ID, Domain, Technology, Difficulty, Type)
       - Header row: dark blue bg, white text
       - Data row: normal text, difficulty color-coded
     - Question text: "Q: " bold blue + question text
     - "Ideal Answer Components:" header with light blue (#D6E4F0) background
     - Answer bullets: indented, Arial 9.5pt
     - Notes box: bordered table cell, #FAFAFA fill, min height
     - Rating row: "1 (Weak) 2 (Below) 3 (Meets) 4 (Strong) 5 (Exceptional)" + input box
     - Blue separator line between questions

3. **Overall Assessment page** (page break):
   - Dark blue header: "OVERALL ASSESSMENT"
   - Per dimension (6 configurable rows):
     - Label + "1–5:" + input box in a row
     - Notes box below
   - Overall Recommendation: "Strong Hire / Hire / Maybe / No Hire" + input box
   - Summary Notes: large notes box

**Key styling constants (from JS template):**
- DARK_BLUE = "1F3864"
- MED_BLUE = "2E75B6"
- LIGHT_BLUE = "D6E4F0"
- LIGHT_GRAY = "F2F2F2"
- Font: Arial throughout
- Input boxes: bordered cells with FAFAFA fill
- Page size: Letter (8.5" × 11"), 1" margins

**Step 2: Write a quick smoke test**

Create a minimal test script (not committed) to verify the docx generates without errors:

```python
from lib.docx_engine import generate_interview_docx
buf = generate_interview_docx(
    metadata={"candidate_name": "Test", "interview_date": "2026-03-17", ...},
    sections=[{"title": "Test Section", "subtitle": "...", "questions": [...]}]
)
with open("test_output.docx", "wb") as f:
    f.write(buf.getvalue())
```

Run: `python test_docx.py`
Expected: `test_output.docx` is created and opens correctly in Word with proper formatting.

**Step 3: Commit**

```bash
git add lib/docx_engine.py
git commit -m "feat(IQS-6): implement docx generation engine with full formatting"
```

---

### Task 7: TeamTailor Evaluation Template (IQS-7)

**Files:**
- Modify: `lib/docx_engine.py` (add evaluation sections)

**Step 1: Extend `generate_interview_docx` to include evaluation pages**

Add two additional pages after the Overall Assessment:

**ATS Evaluation page:**
- Header: dark blue bar "ATS EVALUATION — Technical Interview | General Template"
- Subtitle: "Complete this section after the interview and transfer responses to your ATS."
- 6 evaluation dimensions (configurable list):
  1. Tech Skills (rating + notes)
  2. Consulting Skills (rating + notes)
  3. Seniority (rating + notes)
  4. Communication (rating + notes)
  5. Cultural Fit (rating + notes)
  6. Weaknesses / Areas for Improvement (notes only, no rating)
- Each dimension:
  - Light blue header bar with label
  - Prompt text
  - Rating row (if applicable): "Rating (1–5): 1 (Weak) ... 5 (Exceptional)" + input box
  - Notes box

**Internal Only page:**
- Header: RED (#C00000) background bar "INTERNAL ONLY"
- Seniority Classification: options as text + input box
- Recommendation: "Yes / No" + input box
- Feedback and Comments: large notes box

Make the evaluation dimensions configurable via a parameter with sensible defaults.

**Step 2: Test with full document generation**

Run the smoke test again and verify the evaluation pages appear correctly.

**Step 3: Commit**

```bash
git add lib/docx_engine.py
git commit -m "feat(IQS-7): add TeamTailor evaluation and internal-only sections to docx"
```

---

### Task 8: Generate Page & End-to-End Integration (IQS-8)

**Files:**
- Create: `pages/5_Generate.py`
- Modify: `app.py` (add workflow status overview)
- Modify: `README.md` (update with new workflow docs)

**Step 1: Create `pages/5_Generate.py`**

This page shows a pre-generation summary and the download button:

Key features:
- Validation gate: check that metadata is complete, questions are selected, sections are assigned
- Show missing steps as warnings with links to the relevant page
- Document outline preview: list sections with question counts
- "Generate Interview Document" button that calls `generate_interview_docx()`
- `st.download_button` for the generated .docx file
- Success message with option to start a new interview (clear session state)

**Step 2: Update `app.py` landing page**

Add a workflow status dashboard showing completion state of each step:
- Metadata: complete/incomplete
- Questions selected: count
- Sections organized: yes/no
- Review: approved/pending

**Step 3: Update `README.md`**

Add workflow documentation describing the 5-step process, new dependencies, and updated project structure.

**Step 4: Run full end-to-end test**

Run: `streamlit run app.py`
Walk through: Metadata → Questions → Sections → Review → Generate → Download
Expected: Complete workflow produces a properly formatted .docx matching the reference output.

**Step 5: Commit**

```bash
git add pages/5_Generate.py app.py README.md
git commit -m "feat(IQS-8): add generate page and end-to-end integration"
```

---

### Task 9: Final polish and dependency cleanup

**Files:**
- Modify: `requirements.txt`
- Modify: `.devcontainer/devcontainer.json` (if needed)

**Step 1: Verify `requirements.txt` has all dependencies**

Ensure these are listed:
```
streamlit>=1.51.0
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=1.1.0
```

**Step 2: Clean install and full test**

```bash
pip install -r requirements.txt
streamlit run app.py
```

Walk through the full workflow end-to-end.

**Step 3: Final commit**

```bash
git add -A
git commit -m "chore: finalize dependencies and polish"
```
