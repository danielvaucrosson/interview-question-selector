import streamlit as st
from datetime import date

from lib.data import SENIORITY_LEVELS

st.set_page_config(page_title="Interview Metadata", layout="wide")

st.title("Interview Metadata")
st.caption("Fill in candidate and interview details. Fields marked with * are required.")

# ---------------------------------------------------------------------------
# Persistent storage — a single dict that is NOT widget-bound, so it
# survives page navigation reliably.
# ---------------------------------------------------------------------------
_DEFAULTS = {
    "candidate": "",
    "date": date.today(),
    "interviewer": "",
    "job_title": "",
    "company": "Keyrus",
    "seniority": "Mid",
    "duration": "60 min",
}

if "metadata" not in st.session_state:
    st.session_state.metadata = dict(_DEFAULTS)

meta = st.session_state.metadata

# ---------------------------------------------------------------------------
# Form — all inputs are batched; values captured on submit only.
# No need to press Enter after each field.
# ---------------------------------------------------------------------------
with st.form("metadata_form"):
    left, right = st.columns(2)

    with left:
        candidate = st.text_input("Candidate Name *", value=meta["candidate"])
        interview_date = st.date_input("Interview Date *", value=meta["date"])
        interviewer = st.text_input("Interviewer Name *", value=meta["interviewer"])

    with right:
        job_title = st.text_input("Job Title / Role *", value=meta["job_title"])
        company = st.text_input("Company / Business Unit", value=meta["company"])
        seniority_idx = (
            SENIORITY_LEVELS.index(meta["seniority"])
            if meta["seniority"] in SENIORITY_LEVELS
            else 1
        )
        seniority = st.selectbox(
            "Seniority Level", SENIORITY_LEVELS, index=seniority_idx
        )
        duration = st.text_input("Estimated Duration", value=meta["duration"])

    submitted = st.form_submit_button("Save & Continue", type="primary")

if submitted:
    # Persist all values into the dict (not individual keys)
    st.session_state.metadata = {
        "candidate": candidate,
        "date": interview_date,
        "interviewer": interviewer,
        "job_title": job_title,
        "company": company,
        "seniority": seniority,
        "duration": duration,
    }

    # Validate required fields
    missing = []
    if not candidate.strip():
        missing.append("Candidate Name")
    if not interviewer.strip():
        missing.append("Interviewer Name")
    if not job_title.strip():
        missing.append("Job Title / Role")

    if missing:
        st.warning(f"Missing required fields: {', '.join(missing)}")
    else:
        st.success("Metadata saved! Navigating to Questions...")
        st.switch_page("pages/2_Questions.py")

# ---------------------------------------------------------------------------
# Show current saved status
# ---------------------------------------------------------------------------
st.divider()
meta = st.session_state.metadata
required_check = {
    "Candidate Name": meta["candidate"],
    "Interviewer Name": meta["interviewer"],
    "Job Title / Role": meta["job_title"],
}
missing_now = [name for name, val in required_check.items() if not str(val).strip()]

if missing_now:
    st.info(f"Required fields still needed: {', '.join(missing_now)}")
else:
    st.success("All required fields are saved.")
