import streamlit as st
import pandas as pd
import json
from io import BytesIO
from pathlib import Path

from lib.data import load_questions, TECH_LABELS, DIFF_LABELS

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Question Browser", layout="wide")
st.title("Question Browser")

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
df = load_questions()

# Load job profiles
PROFILES_PATH = Path(__file__).resolve().parent.parent / "config" / "job_profiles.json"
with open(PROFILES_PATH, "r", encoding="utf-8") as f:
    JOB_PROFILES: dict = json.load(f)

# ---------------------------------------------------------------------------
# Session-state defaults
# ---------------------------------------------------------------------------
if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = set()

# ---------------------------------------------------------------------------
# Sidebar — Job Profile Preset (at the TOP)
# ---------------------------------------------------------------------------
profile_options = ["(None)"] + list(JOB_PROFILES.keys())
chosen_profile = st.sidebar.selectbox("Job Profile Preset", profile_options, key="job_profile_preset")

if chosen_profile != "(None)":
    profile = JOB_PROFILES[chosen_profile]
    st.session_state["filter_domains"] = profile["domains"]
    # Build technology display labels for the preset
    preset_tech_labels = [
        f"{code} — {TECH_LABELS.get(code, code)}" for code in profile["technologies"]
    ]
    st.session_state["filter_technologies"] = preset_tech_labels

# ---------------------------------------------------------------------------
# Sidebar — Reset Filters
# ---------------------------------------------------------------------------
if st.sidebar.button("Reset Filters"):
    st.session_state["filter_domains"] = []
    st.session_state["filter_subdomains"] = []
    st.session_state["filter_technologies"] = []
    st.session_state["filter_question_types"] = list(df["question_type"].dropna().unique())
    st.session_state["filter_diff_1"] = True
    st.session_state["filter_diff_2"] = True
    st.session_state["filter_diff_3"] = True
    st.session_state["job_profile_preset"] = "(None)"
    st.rerun()

# ---------------------------------------------------------------------------
# Sidebar — Filters
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

# Domain multiselect
all_domains = sorted(df["domain"].dropna().unique())
selected_domains = st.sidebar.multiselect(
    "Domain", all_domains, key="filter_domains"
)

# Sub-domain multiselect (filtered by selected domains)
if selected_domains:
    available_subdomains = sorted(
        df.loc[df["domain"].isin(selected_domains), "sub_domain"].dropna().unique()
    )
else:
    available_subdomains = sorted(df["sub_domain"].dropna().unique())

selected_subdomains = st.sidebar.multiselect(
    "Sub-domain", available_subdomains, key="filter_subdomains"
)

# Technology multiselect — show "CODE — Label" format
all_tech_codes = set()
for tech_list in df["tech_list"]:
    if isinstance(tech_list, list):
        all_tech_codes.update(tech_list)
all_tech_codes.discard("")

tech_display_options = sorted(
    [f"{code} — {TECH_LABELS.get(code, code)}" for code in all_tech_codes],
    key=lambda x: x.split(" — ")[0],
)

selected_technologies = st.sidebar.multiselect(
    "Technology", tech_display_options, key="filter_technologies"
)

# Difficulty checkboxes (1-3, default True)
st.sidebar.markdown("**Difficulty**")
diff_1 = st.sidebar.checkbox(DIFF_LABELS[1], value=True, key="filter_diff_1")
diff_2 = st.sidebar.checkbox(DIFF_LABELS[2], value=True, key="filter_diff_2")
diff_3 = st.sidebar.checkbox(DIFF_LABELS[3], value=True, key="filter_diff_3")

allowed_difficulties = []
if diff_1:
    allowed_difficulties.append(1)
if diff_2:
    allowed_difficulties.append(2)
if diff_3:
    allowed_difficulties.append(3)

# Question type multiselect (default all)
all_question_types = sorted(df["question_type"].dropna().unique())
selected_question_types = st.sidebar.multiselect(
    "Question Type", all_question_types, default=all_question_types, key="filter_question_types"
)

# Max questions slider
max_questions = st.sidebar.slider(
    "Max questions", min_value=5, max_value=50, value=15, key="filter_max_questions"
)

# ---------------------------------------------------------------------------
# Apply filters — AND between categories, OR within category
# ---------------------------------------------------------------------------
filtered = df.copy()

if selected_domains:
    filtered = filtered[filtered["domain"].isin(selected_domains)]

if selected_subdomains:
    filtered = filtered[filtered["sub_domain"].isin(selected_subdomains)]

if selected_technologies:
    # Extract codes from "CODE — Label" format
    selected_tech_codes = [t.split(" — ")[0] for t in selected_technologies]
    # Multi-tech: "QLK, PBI" matches if user selects either
    mask = filtered["tech_list"].apply(
        lambda tl: any(code in tl for code in selected_tech_codes) if isinstance(tl, list) else False
    )
    filtered = filtered[mask]

if allowed_difficulties:
    filtered = filtered[filtered["difficulty"].isin(allowed_difficulties)]
else:
    filtered = filtered.iloc[0:0]  # no difficulties selected → empty

if selected_question_types:
    filtered = filtered[filtered["question_type"].isin(selected_question_types)]
else:
    filtered = filtered.iloc[0:0]

# Limit to max questions
filtered = filtered.head(max_questions)

# ---------------------------------------------------------------------------
# Results table
# ---------------------------------------------------------------------------
st.subheader(f"Matching Questions ({len(filtered)})")

# Select all visible / Clear selection buttons
col_sel, col_clr, _ = st.columns([1, 1, 4])
with col_sel:
    if st.button("Select all visible"):
        st.session_state.selected_ids.update(filtered["question_id"].tolist())
        st.rerun()
with col_clr:
    if st.button("Clear selection"):
        st.session_state.selected_ids.clear()
        st.rerun()

# Header row
header_cols = st.columns([0.3, 0.8, 3, 1.2, 0.8, 0.8, 0.8])
headers = ["", "ID", "Question", "Domain", "Tech", "Diff.", "Type"]
for col, header in zip(header_cols, headers):
    col.markdown(f"**{header}**")

# Results rows
for _, row in filtered.iterrows():
    cols = st.columns([0.3, 0.8, 3, 1.2, 0.8, 0.8, 0.8])
    qid = row["question_id"]

    # Checkbox
    is_selected = qid in st.session_state.selected_ids
    if cols[0].checkbox("sel", value=is_selected, key=f"chk_{qid}", label_visibility="collapsed"):
        st.session_state.selected_ids.add(qid)
    else:
        st.session_state.selected_ids.discard(qid)

    # ID
    cols[1].write(qid)
    # Question (truncated)
    question_text = str(row["question"])
    truncated = question_text[:120] + "..." if len(question_text) > 120 else question_text
    cols[2].write(truncated)
    # Domain
    cols[3].write(row.get("domain", ""))
    # Technology
    cols[4].write(row.get("technology", ""))
    # Difficulty
    cols[5].write(row.get("diff_label", ""))
    # Type
    cols[6].write(row.get("question_type", ""))

# ---------------------------------------------------------------------------
# Selected questions panel
# ---------------------------------------------------------------------------
st.markdown("---")
selected_ids = st.session_state.selected_ids
selected_df = df[df["question_id"].isin(selected_ids)]

st.subheader(f"Selected Questions ({len(selected_df)})")

if not selected_df.empty:
    for _, row in selected_df.iterrows():
        with st.expander(f"{row['question_id']} — {str(row['question'])[:80]}"):
            st.markdown(f"**Question:** {row['question']}")
            st.markdown(f"**Answer:** {row.get('answer', 'N/A')}")
            st.markdown(
                f"**Domain:** {row.get('domain', '')} | "
                f"**Sub-domain:** {row.get('sub_domain', '')} | "
                f"**Technology:** {row.get('technology', '')} | "
                f"**Difficulty:** {row.get('diff_label', '')} | "
                f"**Type:** {row.get('question_type', '')}"
            )

    # Excel export button
    export_df = selected_df[["question_id", "question", "answer", "domain", "sub_domain", "technology", "difficulty", "question_type"]].copy()
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="Interview Questions")
        ws = writer.sheets["Interview Questions"]
        ws.column_dimensions["B"].width = 60
        ws.column_dimensions["C"].width = 80
        ws.column_dimensions["D"].width = 20

    st.download_button(
        label="Export Selected to Excel",
        data=buf.getvalue(),
        file_name="selected_questions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.info("No questions selected. Use the checkboxes above to select questions.")
