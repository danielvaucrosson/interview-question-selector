import streamlit as st
from datetime import date

from lib.data import SENIORITY_LEVELS

st.set_page_config(page_title="Interview Metadata", layout="wide")

st.title("Interview Metadata")
st.caption("Fill in candidate and interview details. Fields marked with * are required.")

# ---------------------------------------------------------------------------
# Persistent storage keys — these survive page navigation.
# Widget keys are ephemeral; we copy TO them on load and FROM them on save.
# ---------------------------------------------------------------------------
_FIELDS = {
    "meta_candidate": "",
    "meta_date": date.today(),
    "meta_interviewer": "",
    "meta_job_title": "",
    "meta_company": "Keyrus",
    "meta_seniority": "Mid",
    "meta_duration": "60 min",
}

# Ensure persistent keys exist
for key, default in _FIELDS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------------------------
# Form — groups all inputs, only writes on submit
# ---------------------------------------------------------------------------
with st.form("metadata_form"):
    left, right = st.columns(2)

    with left:
        candidate = st.text_input(
            "Candidate Name *", value=st.session_state.meta_candidate
        )
        interview_date = st.date_input(
            "Interview Date *", value=st.session_state.meta_date
        )
        interviewer = st.text_input(
            "Interviewer Name *", value=st.session_state.meta_interviewer
        )

    with right:
        job_title = st.text_input(
            "Job Title / Role *", value=st.session_state.meta_job_title
        )
        company = st.text_input(
            "Company / Business Unit", value=st.session_state.meta_company
        )
        seniority_idx = (
            SENIORITY_LEVELS.index(st.session_state.meta_seniority)
            if st.session_state.meta_seniority in SENIORITY_LEVELS
            else 1
        )
        seniority = st.selectbox(
            "Seniority Level", SENIORITY_LEVELS, index=seniority_idx
        )
        duration = st.text_input(
            "Estimated Duration", value=st.session_state.meta_duration
        )

    submitted = st.form_submit_button("Save & Continue", type="primary")

if submitted:
    # Persist all values to session state
    st.session_state.meta_candidate = candidate
    st.session_state.meta_date = interview_date
    st.session_state.meta_interviewer = interviewer
    st.session_state.meta_job_title = job_title
    st.session_state.meta_company = company
    st.session_state.meta_seniority = seniority
    st.session_state.meta_duration = duration

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
# Show current status (non-form area)
# ---------------------------------------------------------------------------
st.divider()
required_check = {
    "Candidate Name": st.session_state.meta_candidate,
    "Interviewer Name": st.session_state.meta_interviewer,
    "Job Title / Role": st.session_state.meta_job_title,
}
missing_now = [name for name, val in required_check.items() if not str(val).strip()]

if missing_now:
    st.info(f"Required fields still needed: {', '.join(missing_now)}")
else:
    st.success("All required fields are saved.")
