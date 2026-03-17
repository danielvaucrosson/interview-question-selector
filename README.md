# Interview Question Selector

A Streamlit-based web application for filtering, selecting, and exporting interview questions from a curated question bank. Designed for interviewers preparing technical assessments across data and analytics domains.

**Live app:** [interview-question-selector.streamlit.app](https://interview-question-selector-ftivfsozkvakxgd9dl2rzk.streamlit.app/)

## Features

- **Multi-dimensional filtering** — Filter by domain, sub-domain, technology, difficulty level, and question type
- **Bulk selection** — Select all visible questions or clear selections with one click
- **Detailed review** — Expand any question to see the full text, expected answer, and metadata
- **Excel export** — Download selected questions as a formatted `.xlsx` file
- **Reset filters** — Quickly clear all filters to start a fresh search

## Tech Stack

- **Python 3.11+**
- **Streamlit** — Interactive web UI
- **pandas** — Data processing
- **openpyxl** — Excel read/write

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
├── app.py                 # Main Streamlit application
├── question-bank.xlsx     # Interview question data source
├── requirements.txt       # Python dependencies
└── .devcontainer/         # Dev container configuration
```

## Project Management

Issues and tasks are tracked on our Jira board:
**[IQS Jira Project](https://keyrusus.atlassian.net/jira/core/projects/IQS/list)**
