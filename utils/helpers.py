import os
import re
import pandas as pd
import streamlit as st
import json
from contextlib import contextmanager

# File paths for feedback and progress tracking
FEEDBACK_PATH = "feedback.csv"
PROGRESS_FILE = "progress.json"

# -----------------------------------------------------------------------------
# Custom CSS Injection
# -----------------------------------------------------------------------------
def inject_custom_css():
    """Inject custom CSS from the style.css file."""
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Default styles will be applied.")

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
def init_session_state() -> None:
    """Initialize session state defaults."""
    st.session_state.setdefault("read_sections", set())
    st.session_state.setdefault("current_page_index", 0)
    st.session_state.setdefault("global_expansion_state", None)
    st.session_state.setdefault("expand_all_triggered", False)
    st.session_state.setdefault("collapse_all_triggered", False)

# -----------------------------------------------------------------------------
# Validation Utilities
# -----------------------------------------------------------------------------
def is_valid_email(email: str) -> bool:
    """Basic email validation (RFC 5322-lite)."""
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

# -----------------------------------------------------------------------------
# Expand / Collapse Controls
# -----------------------------------------------------------------------------
def display_expand_collapse_controls(current_page: str):
    """Display expand/collapse buttons for sections."""
    visible_on_pages = [
        "Home", "Prompt Engineering", "Temperature & Sampling", "Hallucinations",
        "API Cost Optimization", "Ethics & Bias", "FAQs", "Glossary"
    ]

    if current_page not in visible_on_pages:
        return

    # Handle button clicks using Streamlit
    col1, col2, col3 = st.columns([6, 0.3, 0.5])
    with col2:
        if st.button("➕", key="expand-all"):
            st.session_state["expand_all_triggered"] = True
            st.session_state["collapse_all_triggered"] = False
    with col3:
        if st.button("➖", key="collapse-all"):
            st.session_state["expand_all_triggered"] = False
            st.session_state["collapse_all_triggered"] = True

# -----------------------------------------------------------------------------
# Expander Sections
# -----------------------------------------------------------------------------
@contextmanager
def expander_section(title: str):
    """Creates a Streamlit expander that respects global or per-section expansion state."""
    expander_key = f"expander_{title}"

    # Set default to collapsed
    if expander_key not in st.session_state:
        st.session_state[expander_key] = False

    # Override with global state if set
    if st.session_state.get("expand_all_triggered"):
        st.session_state[expander_key] = True
    elif st.session_state.get("collapse_all_triggered"):
        st.session_state[expander_key] = False

    # Return the expander
    with st.expander(title, expanded=st.session_state[expander_key]):
        yield

# -----------------------------------------------------------------------------
# Reset Controls
# -----------------------------------------------------------------------------
def reset_expansion_state() -> None:
    """Reset all expander-related states to collapsed and clear global state."""
    for key in list(st.session_state.keys()):
        if key.startswith("expander_"):
            st.session_state[key] = False
    st.session_state.pop("global_expansion_state", None)

def reset_expand_collapse_triggers():
    """Reset expand/collapse triggers in session state."""
    st.session_state["expand_all_triggered"] = False
    st.session_state["collapse_all_triggered"] = False

# -----------------------------------------------------------------------------
# Feedback Persistence
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def store_feedback(entry):
    """Store feedback entry into a CSV file."""
    try:
        if os.path.exists(FEEDBACK_PATH):
            # Load existing feedback data
            df = pd.read_csv(FEEDBACK_PATH)
            # Append the new entry using pd.concat
            new_entry_df = pd.DataFrame([entry])
            df = pd.concat([df, new_entry_df], ignore_index=True)
        else:
            # Create a new DataFrame for the entry
            df = pd.DataFrame([entry])
        # Save the updated DataFrame to the CSV file
        df.to_csv(FEEDBACK_PATH, index=False)
    except Exception as e:
        st.error(f"Error storing feedback: {e}")

def load_feedback():
    """Load feedback entries from the CSV file."""
    try:
        if os.path.exists(FEEDBACK_PATH):
            return pd.read_csv(FEEDBACK_PATH).to_dict(orient="records")
        return []
    except Exception as e:
        st.error(f"Error loading feedback: {e}")
        return []

# -----------------------------------------------------------------------------
# Progress Persistence
# -----------------------------------------------------------------------------
def load_progress():
    """Load progress from a JSON file."""
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        return {"read_sections": []}
    except Exception as e:
        st.error(f"Error loading progress: {e}")
        return {"read_sections": []}

def save_progress(page_key):
    """Save progress for a specific page to a JSON file."""
    try:
        progress_data = load_progress()
        progress_data[page_key] = list(st.session_state.get(page_key, []))
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress_data, f)
    except Exception as e:
        st.error(f"Error saving progress: {e}")

def reset_progress(sections, page_key):
    """Reset all progress and clear checkboxes for the given sections."""
    reset_expansion_state()
    st.session_state.pop("Sub-topic", None)  # Clear the sub-topic selector state

    # Clear all checkboxes and read sections
    for title in sections.keys():
        checkbox_key = f"read_checkbox_{title}"
        if checkbox_key in st.session_state:
            del st.session_state[checkbox_key]  # Remove the key entirely

    # Reset the read sections set for the current page
    st.session_state[page_key] = set()

    # Set a flag to indicate that reset was triggered
    st.session_state["reset_triggered"] = True

    # Save progress to file
    save_progress(page_key)