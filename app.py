import streamlit as st

st.set_page_config(page_title="Interview Question Selector", layout="wide")

st.title("Interview Question Selector")

st.markdown("Use the sidebar to navigate through the workflow.")

st.markdown(
    """
    ### Workflow

    1. **Metadata** — Enter candidate and interview details
    2. **Questions** — Browse and select questions from the bank
    3. **Sections** — Organise selected questions into interview sections
    4. **Review** — Preview the final interview document
    5. **Generate** — Export the interview document
    """
)
