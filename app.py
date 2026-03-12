import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path

# --- Config ---
st.set_page_config(page_title="Interview Question Selector", layout="wide")
st.title("Interview Question Selector")

# --- Load data ---
EXCEL_PATH = Path(__file__).parent / "question-bank.xlsx"

TECH_LABELS = {
    "TAB": "Tableau", "QLK": "Qlik", "PBI": "Power BI", "SNO": "Snowflake",
    "FAB": "Fabric", "AWS": "AWS", "AZR": "Azure", "GCP": "GCP",
    "DBR": "Databricks", "DBT": "dbt", "AIR": "Airflow", "SPK": "Spark",
    "KFK": "Kafka", "SQL": "SQL", "PY": "Python", "TFM": "Terraform",
    "GIT": "Git", "LKR": "Looker", "GEN": "General",
}
DIFF_LABELS = {1: "1 — Foundational", 2: "2 — Applied", 3: "3 — Architectural"}


@st.cache_data
def load_questions() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="Questions")
    df = df[df["question_id"].notna()].copy()
    df["tech_list"] = df["technology"].fillna("").str.split(r",\s*")
    df["diff_label"] = df["difficulty"].map(DIFF_LABELS)
    return df


df = load_questions()

# --- Sidebar filters ---
st.sidebar.header("Filters")

all_domains = sorted(df["domain"].dropna().unique())
sel_domains = st.sidebar.multiselect("Domain", all_domains)

if sel_domains:
    sub_opts = sorted(df[df["domain"].isin(sel_domains)]["sub_domain"].dropna().unique())
else:
    sub_opts = sorted(df["sub_domain"].dropna().unique())
sel_subdomains = st.sidebar.multiselect("Sub-domain", sub_opts)

all_techs = sorted({t for techs in df["tech_list"] for t in techs if t})
tech_display = [f"{t} — {TECH_LABELS.get(t, t)}" for t in all_techs]
sel_tech_display = st.sidebar.multiselect("Technology", tech_display)
sel_techs = [t.split(" — ")[0] for t in sel_tech_display]

sel_diffs = []
st.sidebar.markdown("**Difficulty**")
for level, label in DIFF_LABELS.items():
    if st.sidebar.checkbox(label, value=True, key=f"diff_{level}"):
        sel_diffs.append(level)

all_types = sorted(df["question_type"].dropna().unique())
sel_types = st.sidebar.multiselect("Question type", all_types, default=all_types)

max_q = st.sidebar.slider("Max questions", 5, 50, 15)

# --- Apply filters ---
mask = pd.Series(True, index=df.index)

if sel_domains:
    mask &= df["domain"].isin(sel_domains)
if sel_subdomains:
    mask &= df["sub_domain"].isin(sel_subdomains)
if sel_techs:
    mask &= df["tech_list"].apply(lambda ts: any(t in sel_techs for t in ts))
if sel_diffs:
    mask &= df["difficulty"].isin(sel_diffs)
if sel_types:
    mask &= df["question_type"].isin(sel_types)

filtered = df[mask].head(max_q).copy()

st.subheader(f"Matching questions ({len(df[mask])} total, showing {len(filtered)})")

# --- Selection state ---
if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = set()

col1, col2, _ = st.columns([1, 1, 4])
with col1:
    if st.button("Select all visible"):
        st.session_state.selected_ids |= set(filtered["question_id"])
        for qid in filtered["question_id"]:
            st.session_state[f"cb_{qid}"] = True
        st.rerun()
with col2:
    if st.button("Clear selection"):
        for qid in st.session_state.selected_ids:
            st.session_state[f"cb_{qid}"] = False
        st.session_state.selected_ids.clear()
        st.rerun()

# --- Header row ---
hdr_cb, hdr_id, hdr_q, hdr_dom, hdr_tech, hdr_diff, hdr_type = st.columns(
    [0.5, 1, 5, 2, 1.5, 1.5, 1.2]
)
with hdr_id:
    st.markdown("**ID**")
with hdr_q:
    st.markdown("**Question**")
with hdr_dom:
    st.markdown("**Domain**")
with hdr_tech:
    st.markdown("**Tech**")
with hdr_diff:
    st.markdown("**Difficulty**")
with hdr_type:
    st.markdown("**Type**")

# --- Results with checkboxes ---
for _, row in filtered.iterrows():
    qid = row["question_id"]
    checked = qid in st.session_state.selected_ids
    trunc_q = (
        row["question"][:120] + "..."
        if len(str(row["question"])) > 120
        else row["question"]
    )

    col_cb, col_id, col_q, col_dom, col_tech, col_diff, col_type = st.columns(
        [0.5, 1, 5, 2, 1.5, 1.5, 1.2]
    )
    with col_cb:
        new_val = st.checkbox(
            "sel", value=checked, key=f"cb_{qid}", label_visibility="collapsed"
        )
        if new_val and qid not in st.session_state.selected_ids:
            st.session_state.selected_ids.add(qid)
        elif not new_val and qid in st.session_state.selected_ids:
            st.session_state.selected_ids.discard(qid)
    with col_id:
        st.caption(qid)
    with col_q:
        st.write(trunc_q)
    with col_dom:
        st.caption(row["domain"])
    with col_tech:
        st.caption(row["technology"])
    with col_diff:
        st.caption(row["diff_label"])
    with col_type:
        st.caption(row["question_type"])

# --- Selected questions panel ---
st.divider()
selected_df = df[df["question_id"].isin(st.session_state.selected_ids)].copy()
st.subheader(f"Selected questions ({len(selected_df)})")

if selected_df.empty:
    st.info(
        "No questions selected yet. Use the checkboxes above to build your interview set."
    )
else:
    for _, row in selected_df.iterrows():
        with st.expander(f"**{row['question_id']}** — {row['question'][:100]}"):
            st.markdown(f"**Question:** {row['question']}")
            st.markdown(f"**Answer:**\n{row['answer']}")
            st.caption(
                f"Domain: {row['domain']} | Sub-domain: {row['sub_domain']} | "
                f"Tech: {row['technology']} | Difficulty: {row['diff_label']} | "
                f"Type: {row['question_type']} | Tags: {row['tags']}"
            )

    export_cols = [
        "question_id", "question", "answer", "domain", "sub_domain",
        "technology", "difficulty", "question_type", "tags",
    ]
    export_df = selected_df[export_cols].copy()
    export_df["difficulty"] = export_df["difficulty"].map(DIFF_LABELS)

    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="Interview Questions")
        ws = writer.sheets["Interview Questions"]
        ws.column_dimensions["B"].width = 60
        ws.column_dimensions["C"].width = 80
        ws.column_dimensions["D"].width = 20
    buf.seek(0)

    st.download_button(
        label="Download selected questions (.xlsx)",
        data=buf,
        file_name="interview-questions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
