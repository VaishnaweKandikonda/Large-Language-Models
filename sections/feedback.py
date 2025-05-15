import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
from utils.helpers import display_expand_collapse_controls, reset_expansion_state, store_feedback, load_feedback,inject_custom_css

def render():
    inject_custom_css()
    current_page = "Feedback"
    st.title("Share Your Experience")
    display_expand_collapse_controls(current_page)

    st.markdown("""
    Your feedback helps us improve the **LLM Guide for Startups**.  
    Let us know what you found useful and what you'd like to see next.
    """)

    st.markdown("### Feedback Form")

    # --- Feedback Form ---
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
        with col2:
            email = st.text_input("Email Address (optional)", placeholder="e.g. alex@startup.ie")

        rating = st.slider("How helpful was this guide?", 1, 5, 3)
        feedback = st.text_area("Your Comments (optional)", placeholder="What worked well? What could be improved?")
        suggestion = st.selectbox("What topics should we cover next?", 
                                  ["None", "LLM APIs", "Customer Support", "Tool Comparisons", "No-code Prototyping"])
        attachment = st.file_uploader("📎 Optional File Upload", type=["png", "jpg", "pdf", "txt", "docx"])

        required_filled = bool(name.strip())
        email_valid = True if not email.strip() else re.match(r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$", email.strip())

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if not required_filled:
                st.warning("Please enter your name to submit the form.")
            elif not email_valid:
                st.error("Invalid email format. Please check and try again.")
            else:
                entry = {
                    "Name": name.strip(),
                    "Email": email.strip(),
                    "Rating": rating,
                    "Feedback": feedback.strip(),
                    "Suggested Topic": None if suggestion == "None" else suggestion,
                    "Attachment Name": attachment.name if attachment else None
                }
                store_feedback(entry)

                # Update session state with the new feedback entry
                if "feedback_entries" not in st.session_state:
                    st.session_state["feedback_entries"] = []
                st.session_state["feedback_entries"].append(entry)

                st.success(f" Thank you, {name.strip()}! We truly appreciate your insights.")

    # --- Load feedback entries on first render ---
    if 'feedback_entries' not in st.session_state:
        st.session_state['feedback_entries'] = load_feedback()

    # --- Feedback Table ---
    if st.session_state['feedback_entries']:
        df = pd.DataFrame(st.session_state['feedback_entries'])
        df = df[df["Name"].str.strip().str.lower() != "admin"]
        df = df[df["Name"].str.strip() != ""]
        df.index += 1
        df.index.name = "No."

        st.markdown("### All Submitted Feedback")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No feedback submitted yet. Be the first to contribute!")

    # --- Admin Controls ---
    with st.expander("Admin Controls: Manage Feedback Records"):
        st.markdown("Export or delete all feedback entries below.")
        admin_key_input = st.text_input("Admin Passphrase", type="password", placeholder="Enter passphrase")
        confirm_clear = st.checkbox("I confirm this action is irreversible.")

        ADMIN_PASSPHRASE = st.secrets["ADMIN_PASSPHRASE"]
        FEEDBACK_PATH = "feedback.csv"

        # Download feedback CSV
        if st.session_state.get("feedback_entries"):
            export_df = pd.DataFrame(st.session_state["feedback_entries"])
            csv_data = export_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Feedback CSV", csv_data, file_name="feedback_backup.csv", mime="text/csv")

        # Clear feedback
        if st.button("Clear All Feedback"):
            if admin_key_input == ADMIN_PASSPHRASE and confirm_clear:
                try:
                    if os.path.exists(FEEDBACK_PATH):
                        os.remove(FEEDBACK_PATH)
                        st.success("feedback.csv file deleted from disk.")
                    else:
                        st.info("feedback.csv file not found.")

                    st.session_state["feedback_entries"] = []
                    st.cache_data.clear()
                    st.success("Feedback data cleared from memory and cache.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error while deleting feedback: {str(e)}")
            else:
                st.error("Invalid passphrase or confirmation checkbox not selected.")

    reset_expansion_state()

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; font-size: 14px; line-height: 1.6;'>
            <strong>LLM Guide for Startups</strong> — Practical insights for using language models responsibly and efficiently in startup settings.<br>
            Built with by:<br>
            • <strong>Vaishnavi Kandikonda - 24216940 </strong> — <a href="mailto:vaishnavi.kandikonda@ucdconnect.com">vaishnavi.kandikonda@ucdconnect.com</a><br>
            • <strong>Shivani Singh - 24234516 </strong> — <a href="mailto:shivani.singh@ucdconnect.ie">shivani.singh@ucdconnect.ie</a><br>
            • <strong>Kushal Pratap Singh - 24205476 </strong> — <a href="mailto:kushal.singh@ucdconnect.ie">kushal.singh@ucdconnect.ie</a><br><br>
            © 2025 LLM Startup Guide • Last updated {last_updated} • Built with Streamlit • Guided by principles of transparency, fairness, and human-centered AI.
        </div>
        """.format(last_updated=datetime.now().strftime("%Y-%m-%d")),
        unsafe_allow_html=True
    )