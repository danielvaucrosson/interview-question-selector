import streamlit as st
from datetime import date

from lib.data import SENIORITY_LEVELS

st.set_page_config(page_title="Interview Metadata", layout="wide")

st.title("Interview Metadata")
st.caption("Fill in candidate and interview details. Fields marked with * are required.")

# ---------------------------------------------------------------------------
# Session-state defaults
# ---------------------------------------------------------------------------
_defaults = {
    "meta_candidate": "",
    "meta_date": date.today(),
    "meta_interviewer": "",
    "meta_job_title": "",
    "meta_company": "Keyrus",
    "meta_seniority": "Mid",
    "meta_duration": "60 min",
}

for key, value in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------------------------------
# Two-column layout
# ---------------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.text_input("Candidate Name *", key="meta_candidate")
    st.date_input("Interview Date *", key="meta_date")
    st.text_input("Interviewer Name *", key="meta_interviewer")

with right:
    st.text_input("Job Title / Role *", key="meta_job_title")
    st.text_input("Company / Business Unit", key="meta_company")
    st.selectbox("Seniority Level", SENIORITY_LEVELS, key="meta_seniority")
    st.text_input("Estimated Duration", key="meta_duration")

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
required = {
    "Candidate Name": st.session_state.meta_candidate,
    "Interviewer Name": st.session_state.meta_interviewer,
    "Job Title / Role": st.session_state.meta_job_title,
}

missing = [name for name, val in required.items() if not val.strip()]

if missing:
    st.warning(f"Missing required fields: {', '.join(missing)}")
else:
    st.success("All required fields are complete.")
