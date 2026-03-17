import streamlit as st

st.set_page_config(page_title="Interview Question Selector", layout="wide")

st.title("Interview Question Selector")

st.markdown("Use the sidebar to navigate through the workflow.")

st.markdown("""\
### Workflow

1. **Metadata** — Enter candidate and interview details
2. **Questions** — Browse and select questions from the bank
3. **Sections** — Organise selected questions into interview sections
4. **Review** — Preview the final interview document
5. **Generate** — Export the interview document
""")

# ---------------------------------------------------------------------------
# Workflow status dashboard
# ---------------------------------------------------------------------------
st.markdown("### Current Status")

col1, col2, col3, col4 = st.columns(4)

# Metadata status
meta = st.session_state.get("metadata", {})
meta_ok = all(
    meta.get(k, "")
    for k in ("candidate", "interviewer", "job_title")
)
with col1:
    if meta_ok:
        st.success("Metadata: Complete")
    else:
        st.error("Metadata: Incomplete")

# Questions status
selected_ids = st.session_state.get("selected_ids", set())
with col2:
    if selected_ids:
        st.success(f"Questions: {len(selected_ids)} selected")
    else:
        st.warning("Questions: None selected")

# Sections status
sections = st.session_state.get("sections", [])
section_q_count = sum(len(s.get("questions", [])) for s in sections)
with col3:
    if sections and section_q_count > 0:
        st.success(f"Sections: {len(sections)} with {section_q_count} questions")
    else:
        st.warning("Sections: Not organised")

# Review status
with col4:
    if st.session_state.get("review_complete", False):
        st.success("Review: Approved")
    else:
        st.warning("Review: Pending")
