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
