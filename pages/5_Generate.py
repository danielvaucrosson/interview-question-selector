import streamlit as st
import re
from lib.docx_engine import generate_interview_docx

st.set_page_config(page_title="Generate Document", layout="wide")

st.title("Generate Interview Document")

# ---------------------------------------------------------------------------
# Validation gate
# ---------------------------------------------------------------------------
warnings = []

meta_candidate = st.session_state.get("meta_candidate", "")
meta_interviewer = st.session_state.get("meta_interviewer", "")
meta_job_title = st.session_state.get("meta_job_title", "")

if not meta_candidate or not meta_interviewer or not meta_job_title:
    warnings.append("Metadata incomplete — visit **1 - Metadata** to fill in required fields.")

sections = st.session_state.get("sections", [])
total_questions = sum(len(s.get("questions", [])) for s in sections)

if not sections or total_questions == 0:
    warnings.append("No questions organised — visit **3 - Sections** to organise questions into sections.")

review_complete = st.session_state.get("review_complete", False)
if not review_complete:
    warnings.append("Review not yet approved — visit **4 - Review** to finalise (optional).")

# Show warnings
blocking = [w for w in warnings if "optional" not in w.lower()]
optional = [w for w in warnings if "optional" in w.lower()]

for w in blocking:
    st.error(w)
for w in optional:
    st.warning(w)

# ---------------------------------------------------------------------------
# Document outline preview
# ---------------------------------------------------------------------------
if sections and total_questions > 0:
    st.subheader("Document Outline")

    st.markdown(f"**Candidate:** {meta_candidate}")
    st.markdown(f"**Job Title:** {meta_job_title}")

    for sec in sections:
        q_count = len(sec.get("questions", []))
        st.markdown(f"- **{sec.get('title', 'Untitled')}** — {q_count} question{'s' if q_count != 1 else ''}")

    duration = st.session_state.get("meta_duration", "")
    st.markdown(f"**Total questions:** {total_questions}")
    if duration:
        st.markdown(f"**Estimated duration:** {duration}")

    st.divider()

# ---------------------------------------------------------------------------
# Generate button
# ---------------------------------------------------------------------------
can_generate = len(blocking) == 0

if can_generate:
    if st.button("Generate Interview Document", type="primary"):
        metadata = {
            "candidate_name": meta_candidate,
            "interview_date": str(st.session_state.get("meta_date", "")),
            "interviewer": meta_interviewer,
            "job_title": meta_job_title,
            "company": st.session_state.get("meta_company", ""),
            "seniority": st.session_state.get("meta_seniority", ""),
            "duration": st.session_state.get("meta_duration", ""),
            "question_count": str(total_questions),
        }

        with st.spinner("Generating document..."):
            buf = generate_interview_docx(metadata, sections)

        # Sanitize candidate name for filename
        safe_name = re.sub(r"[^a-zA-Z0-9_\- ]", "", meta_candidate).strip().replace(" ", "_")
        date_str = str(st.session_state.get("meta_date", "today"))
        file_name = f"Interview_{safe_name}_{date_str}.docx"

        st.success("Document generated successfully!")

        st.download_button(
            label="Download Interview Document",
            data=buf,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        st.divider()

        if st.button("Start New Interview"):
            for key in [
                "meta_candidate", "meta_date", "meta_interviewer",
                "meta_job_title", "meta_company", "meta_seniority",
                "meta_duration", "selected_ids", "sections",
                "review_complete", "custom_q_counter",
            ]:
                st.session_state.pop(key, None)
            # Clear all checkbox keys (chk_*)
            chk_keys = [k for k in st.session_state if k.startswith("chk_")]
            for k in chk_keys:
                del st.session_state[k]
            st.rerun()
else:
    st.info("Resolve the errors above before generating the document.")
