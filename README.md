# Interview Question Selector

A Streamlit-based web application for filtering, selecting, and exporting interview questions from a curated question bank. Designed for interviewers preparing technical assessments across data and analytics domains.

**Live app:** [interview-question-selector.streamlit.app](https://interview-question-selector-ftivfsozkvakxgd9dl2rzk.streamlit.app/)

## Workflow

The app guides you through a 5-step process to build a complete interview document:

1. **Metadata** — Enter candidate name, interviewer, job title, company, seniority, and interview date
2. **Questions** — Browse the question bank with multi-dimensional filters and select questions
3. **Sections** — Organise selected questions into titled interview sections
4. **Review** — Preview the full interview document before export
5. **Generate** — Validate, preview the document outline, and download a formatted `.docx` file

## Features

- **Multi-dimensional filtering** — Filter by domain, sub-domain, technology, difficulty level, and question type
- **Bulk selection** — Select all visible questions or clear selections with one click
- **Detailed review** — Expand any question to see the full text, expected answer, and metadata
- **Section organisation** — Group questions into logical interview sections with titles and subtitles
- **Document generation** — Export a professionally formatted `.docx` interview document with cover page, question sections, assessment rubrics, and evaluation forms
- **Reset filters** — Quickly clear all filters to start a fresh search
- **Workflow dashboard** — Landing page shows real-time completion status for each step

## Tech Stack

- **Python 3.11+**
- **Streamlit** — Interactive web UI
- **pandas** — Data processing
- **openpyxl** — Excel read/write
- **python-docx** — Word document generation

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

### Dev Container

A `.devcontainer` configuration is included for VS Code / GitHub Codespaces. Opening the project in a dev container will automatically install dependencies and start the app.

## Project Structure

```
├── app.py                     # Main Streamlit application (landing page & status dashboard)
├── pages/
│   ├── 1_Metadata.py          # Step 1: Candidate & interview metadata
│   ├── 2_Questions.py         # Step 2: Question browsing & selection
│   ├── 3_Sections.py          # Step 3: Section organisation
│   ├── 4_Review.py            # Step 4: Document preview
│   └── 5_Generate.py          # Step 5: Validation, generation & download
├── lib/
│   ├── data.py                # Question bank loader & shared constants
│   └── docx_engine.py         # Word document generation engine
├── question-bank.xlsx         # Interview question data source
├── requirements.txt           # Python dependencies
└── .devcontainer/             # Dev container configuration
```

## Project Management

Issues and tasks are tracked on our Jira board:
**[IQS Jira Project](https://keyrusus.atlassian.net/jira/core/projects/IQS/list)**
