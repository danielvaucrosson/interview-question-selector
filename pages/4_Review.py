import streamlit as st
from lib.data import DIFF_COLORS

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Review & Validate", layout="wide")
st.title("Review & Validate")

# ---------------------------------------------------------------------------
# Guard clause
# ---------------------------------------------------------------------------
sections = st.session_state.get("sections", [])
has_questions = any(len(sec.get("questions", [])) > 0 for sec in sections)

if not sections or not has_questions:
    st.info(
        "No sections with questions found. Go to the **Sections** page to "
        "organise your questions first."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Gather all questions and compute difficulty counts
# ---------------------------------------------------------------------------
all_questions = []
for sec in sections:
    all_questions.extend(sec.get("questions", []))

diff_counts: dict[int, int] = {0: 0, 1: 0, 2: 0, 3: 0}
for q in all_questions:
    d = q.get("difficulty", 1)
    diff_counts[d] = diff_counts.get(d, 0) + 1

total_questions = len(all_questions)
estimated_duration = total_questions * 5  # ~5 min per question

# ---------------------------------------------------------------------------
# Difficulty distribution badges
# ---------------------------------------------------------------------------
st.subheader("Difficulty Distribution")

badge_parts = []
for level in (0, 1, 2, 3):
    info = DIFF_COLORS[level]
    count = diff_counts.get(level, 0)
    badge_parts.append(
        f'<span style="background-color:{info["hex"]};color:#fff;'
        f'padding:4px 12px;border-radius:12px;font-weight:600;'
        f'font-size:0.9em;">{count} {info["label"]}</span>'
    )

st.markdown("&nbsp; &middot; &nbsp;".join(badge_parts), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Metrics: total count and estimated duration
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)
col1.metric("Total Questions", total_questions)
col2.metric("Estimated Duration", f"{estimated_duration} min")

# ---------------------------------------------------------------------------
# Seniority warning
# ---------------------------------------------------------------------------
seniority = st.session_state.get("meta_seniority", "")

if seniority and total_questions > 0:
    foundational_pct = diff_counts.get(1, 0) / total_questions
    architectural_pct = diff_counts.get(3, 0) / total_questions

    senior_keywords = {"senior", "expert", "lead", "director", "manager"}
    junior_keywords = {"junior"}

    seniority_lower = seniority.lower()

    if any(kw in seniority_lower for kw in senior_keywords) and foundational_pct > 0.5:
        st.warning(
            f"Over 50% of questions are **Foundational** for a "
            f"**{seniority}** role. Consider adding more Applied or "
            f"Architectural questions to match seniority expectations."
        )

    if any(kw in seniority_lower for kw in junior_keywords) and architectural_pct > 0.5:
        st.warning(
            f"Over 50% of questions are **Architectural** for a "
            f"**{seniority}** role. Consider replacing some with "
            f"Foundational or Applied questions."
        )

# ---------------------------------------------------------------------------
# Section-by-section breakdown
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Section Breakdown")

for sec in sections:
    questions = sec.get("questions", [])
    st.markdown(f"### {sec['title']}  ({len(questions)} questions)")
    if sec.get("subtitle"):
        st.caption(sec["subtitle"])

    if not questions:
        st.write("*No questions in this section.*")
        continue

    for q in questions:
        diff_info = DIFF_COLORS.get(q.get("difficulty", 1), DIFF_COLORS[1])
        with st.expander(f"{q['id']} — {q['question'][:120]}"):
            st.markdown(f"**Question:** {q['question']}")
            if q.get("answer"):
                st.markdown(f"**Answer:** {q['answer']}")
            meta_cols = st.columns(4)
            meta_cols[0].write(f"**Domain:** {q.get('domain', '—')}")
            meta_cols[1].write(f"**Subdomain:** {q.get('subdomain', '—')}")
            meta_cols[2].write(f"**Technology:** {q.get('technology', '—')}")
            meta_cols[3].markdown(
                f'**Difficulty:** <span style="background-color:{diff_info["hex"]};'
                f'color:#fff;padding:2px 8px;border-radius:8px;">'
                f'{diff_info["label"]}</span>',
                unsafe_allow_html=True,
            )
            st.write(f"**Type:** {q.get('question_type', '—')}")

# ---------------------------------------------------------------------------
# Proceed button
# ---------------------------------------------------------------------------
st.markdown("---")
if st.button("Looks good — proceed to generate", type="primary"):
    st.session_state.review_complete = True
    st.switch_page("pages/5_Generate.py")
