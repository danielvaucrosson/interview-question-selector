import streamlit as st
from lib.data import load_questions, DIFF_LABELS

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Sections & Ordering", layout="wide")
st.title("Sections & Question Ordering")

# ---------------------------------------------------------------------------
# Guard clause — no selected questions
# ---------------------------------------------------------------------------
if "selected_ids" not in st.session_state or not st.session_state.selected_ids:
    st.info(
        "No questions selected yet. Go to the **Questions** page to browse and "
        "select questions first."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Load question data for selected IDs
# ---------------------------------------------------------------------------
df = load_questions()
selected_ids = st.session_state.selected_ids
selected_df = df[df["question_id"].isin(selected_ids)].copy()

# Build a lookup dict: question_id -> row dict
question_lookup: dict = {}
for _, row in selected_df.iterrows():
    question_lookup[row["question_id"]] = {
        "id": row["question_id"],
        "question": str(row["question"]),
        "answer": str(row.get("answer", "")),
        "domain": str(row.get("domain", "")),
        "subdomain": str(row.get("sub_domain", "")),
        "technology": str(row.get("technology", "")) or "\u2014",
        "difficulty": int(row["difficulty"]) if row.get("difficulty") is not None else 1,
        "question_type": str(row.get("question_type", "")),
    }

# ---------------------------------------------------------------------------
# Default sections
# ---------------------------------------------------------------------------
DEFAULT_SECTIONS = [
    {
        "title": "INTRODUCTION (5 MIN)",
        "subtitle": "Let the candidate settle in. Listen for narrative clarity, career arc, and what they emphasize.",
        "questions": [],
    },
    {
        "title": "WARM-UP & ROLE FIT",
        "subtitle": "Start conversational. Assess motivation, consulting experience, and communication style.",
        "questions": [],
    },
    {
        "title": "CORE TECHNICAL SKILLS",
        "subtitle": "Primary assessment area. Test depth in the role\u2019s key technologies.",
        "questions": [],
    },
    {
        "title": "ARCHITECTURE & DESIGN",
        "subtitle": "Tests system thinking, migration planning, and platform knowledge.",
        "questions": [],
    },
    {
        "title": "CLOSING \u2014 DEPTH CHECK",
        "subtitle": "One final technical deep-dive to confirm seniority level.",
        "questions": [],
    },
]

if "sections" not in st.session_state:
    st.session_state.sections = [dict(s, questions=list(s["questions"])) for s in DEFAULT_SECTIONS]

# Custom question counter
if "custom_q_counter" not in st.session_state:
    st.session_state.custom_q_counter = 0


# ---------------------------------------------------------------------------
# Helper: collect all question IDs already assigned to sections
# ---------------------------------------------------------------------------
def _assigned_ids() -> set:
    ids = set()
    for sec in st.session_state.sections:
        for q in sec["questions"]:
            ids.add(q["id"])
    return ids


# ---------------------------------------------------------------------------
# Helper: get section titles
# ---------------------------------------------------------------------------
def _section_titles() -> list[str]:
    return [s["title"] for s in st.session_state.sections]


# ---------------------------------------------------------------------------
# Sidebar — Add new section
# ---------------------------------------------------------------------------
st.sidebar.subheader("Add New Section")
new_title = st.sidebar.text_input("Section title", key="new_section_title")
new_subtitle = st.sidebar.text_input("Section subtitle", key="new_section_subtitle")
if st.sidebar.button("Add section"):
    if new_title.strip():
        st.session_state.sections.append(
            {"title": new_title.strip(), "subtitle": new_subtitle.strip(), "questions": []}
        )
        st.rerun()
    else:
        st.sidebar.warning("Section title cannot be empty.")

# ---------------------------------------------------------------------------
# Sidebar — Add custom question
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Add Custom Question")
custom_q_text = st.sidebar.text_area("Question text", key="custom_q_text")
custom_a_text = st.sidebar.text_area("Answer key", key="custom_a_text")
custom_section = st.sidebar.selectbox(
    "Assign to section", _section_titles(), key="custom_q_section"
)
if st.sidebar.button("Add custom question"):
    if custom_q_text.strip():
        st.session_state.custom_q_counter += 1
        cid = f"CUSTOM-{st.session_state.custom_q_counter:03d}"
        custom_q = {
            "id": cid,
            "question": custom_q_text.strip(),
            "answer": custom_a_text.strip(),
            "domain": "Custom",
            "subdomain": "Custom",
            "technology": "\u2014",
            "difficulty": 0,
            "question_type": "scenario",
        }
        # Find the target section and append
        for sec in st.session_state.sections:
            if sec["title"] == custom_section:
                sec["questions"].append(custom_q)
                break
        # Also add to question_lookup so it shows properly
        question_lookup[cid] = custom_q
        st.rerun()
    else:
        st.sidebar.warning("Question text cannot be empty.")

# ---------------------------------------------------------------------------
# Unassigned questions — assign to sections
# ---------------------------------------------------------------------------
assigned = _assigned_ids()
unassigned_ids = [qid for qid in sorted(selected_ids) if qid in question_lookup and qid not in assigned]

if unassigned_ids:
    st.subheader(f"Unassigned Questions ({len(unassigned_ids)})")
    st.caption("Assign each selected question to a section.")

    section_titles = _section_titles()
    for qid in unassigned_ids:
        q = question_lookup[qid]
        col_q, col_sec, col_btn = st.columns([3, 2, 1])
        col_q.write(f"**{qid}** \u2014 {q['question'][:100]}")
        chosen = col_sec.selectbox(
            "Section",
            section_titles,
            key=f"assign_{qid}",
            label_visibility="collapsed",
        )
        if col_btn.button("Assign", key=f"btn_assign_{qid}"):
            for sec in st.session_state.sections:
                if sec["title"] == chosen:
                    sec["questions"].append(dict(q))
                    break
            st.rerun()

    # Bulk assign all visible
    bulk_col1, bulk_col2, _ = st.columns([2, 2, 4])
    bulk_section = bulk_col1.selectbox(
        "Assign all to", section_titles, key="bulk_assign_section"
    )
    if bulk_col2.button("Assign all unassigned"):
        for qid in unassigned_ids:
            q = question_lookup[qid]
            for sec in st.session_state.sections:
                if sec["title"] == bulk_section:
                    sec["questions"].append(dict(q))
                    break
        st.rerun()

    st.markdown("---")

# ---------------------------------------------------------------------------
# Sections display — rename, reorder questions, remove
# ---------------------------------------------------------------------------
st.subheader("Sections")

for sec_idx, section in enumerate(st.session_state.sections):
    with st.expander(f"{section['title']}  ({len(section['questions'])} questions)", expanded=True):
        # Rename title and subtitle
        rename_col1, rename_col2 = st.columns(2)
        new_t = rename_col1.text_input(
            "Title", value=section["title"], key=f"sec_title_{sec_idx}"
        )
        new_s = rename_col2.text_input(
            "Subtitle", value=section["subtitle"], key=f"sec_sub_{sec_idx}"
        )
        if new_t != section["title"]:
            section["title"] = new_t
        if new_s != section["subtitle"]:
            section["subtitle"] = new_s

        # Remove section button (only if empty)
        if not section["questions"]:
            if st.button(f"Remove section", key=f"remove_sec_{sec_idx}"):
                st.session_state.sections.pop(sec_idx)
                st.rerun()
        else:
            st.caption("Remove all questions before deleting this section.")

        # Questions within section
        questions = section["questions"]
        for q_idx, q in enumerate(questions):
            diff_label = DIFF_LABELS.get(q["difficulty"], "Intro") if q["difficulty"] != 0 else "Intro"
            q_col_order, q_col_id, q_col_text, q_col_actions = st.columns([0.8, 1, 4, 1.5])

            # Up / Down reorder buttons
            with q_col_order:
                btn_cols = st.columns(2)
                if q_idx > 0:
                    if btn_cols[0].button("\u25b2", key=f"up_{sec_idx}_{q_idx}"):
                        questions[q_idx], questions[q_idx - 1] = questions[q_idx - 1], questions[q_idx]
                        st.rerun()
                else:
                    btn_cols[0].write("")
                if q_idx < len(questions) - 1:
                    if btn_cols[1].button("\u25bc", key=f"down_{sec_idx}_{q_idx}"):
                        questions[q_idx], questions[q_idx + 1] = questions[q_idx + 1], questions[q_idx]
                        st.rerun()
                else:
                    btn_cols[1].write("")

            q_col_id.write(f"**{q['id']}**")
            q_col_text.write(f"{q['question'][:120]}  \n*{diff_label} | {q['question_type']}*")

            # Remove from section
            if q_col_actions.button("Remove", key=f"rmq_{sec_idx}_{q_idx}"):
                questions.pop(q_idx)
                st.rerun()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
st.markdown("---")
total_assigned = sum(len(s["questions"]) for s in st.session_state.sections)
total_selected = len(selected_ids)
assigned_from_bank = _assigned_ids()
custom_count = sum(1 for qid in assigned_from_bank if qid.startswith("CUSTOM-"))
bank_assigned = total_assigned - custom_count
unassigned_count = len([qid for qid in selected_ids if qid not in assigned_from_bank])

st.caption(
    f"**Summary:** {total_assigned} questions assigned across "
    f"{len(st.session_state.sections)} sections "
    f"({bank_assigned} from bank, {custom_count} custom). "
    f"{unassigned_count} still unassigned."
)
