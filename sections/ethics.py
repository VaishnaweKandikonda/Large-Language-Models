import streamlit as st
from datetime import datetime  # Import datetime for the footer
import io  # For creating downloadable files
from utils.helpers import (
    display_expand_collapse_controls,
    expander_section,
    reset_expansion_state,
    reset_expand_collapse_triggers,
    reset_progress,
    save_progress,
    load_progress, inject_custom_css
)

PROGRESS_FILE = "progress.json"

def render():
    inject_custom_css()
    current_page = "Ethics & Bias"
    st.title("Ethics and Bias in Language Models")
    display_expand_collapse_controls(current_page)

    # --- Load progress from file ---
    if "ethics_read_sections" not in st.session_state:
        progress_data = load_progress()
        st.session_state["ethics_read_sections"] = set(progress_data.get("ethics_read_sections", []))
        
    # --- Define sections for progress tracking ---
    ethics_sections = {
        "Why Ethics and Fairness Matter": (
            "Language models are powerful but not perfect. Trained on internet-scale data, they may reflect or amplify social biases.\n\n"
            "As a founder, you're responsible for building inclusive, safe, and trustworthy AI-powered products."
        ),
        "Types of Bias": (
            "### Common Biases Language Models May Exhibit\n\n"
            "- **Gender Bias** — Assigning roles by stereotypes. _E.g., 'engineer = man'._\n"
            "- **Racial Bias** — Unequal treatment or assumptions by race.\n"
            "- **Cultural Bias** — Overrepresenting dominant values, underrepresenting others.\n"
            "- **Age Bias** — Assuming lack of tech literacy by age.\n"
            "- **Language Bias** — Penalizing informal, regional, or non-native language use.\n\n"
            "Bias can be subtle. Always test across diverse user personas."
        ),
        "Examples of Bias": (
            "- A resume screener that favors male names\n"
            "- A chatbot that assumes engineers are male\n"
            "- Product copy omitting diverse customer personas"
        ),
        "Why Bias Happens": (
            "Language models reflect patterns in the data they’re trained on:\n\n"
            "- Repetition of dominant cultural narratives\n"
            "- Lack of understanding of fairness\n"
            "- Imbalanced or toxic web content influencing outputs"
        ),
        "What Founders Can Do": (
            "Test outputs across diverse identities\n"
            "Avoid AI in high-risk use cases without oversight\n"
            "Add human review to sensitive content\n"
            "Communicate transparently about AI use\n"
            "Share responsibility across product, design, and legal teams"
        ),
        "Bias Detection Example": (
            "#### Live Example: Can You Detect the Bias?\n\n"
            "**Prompt:** Write a job ad for a software engineer\n\n"
            "**Model Output:** “We're looking for a strong, young male developer to join our elite dev team.”\n\n"
            "**Reflection:** Are assumptions being made? Who is stereotyped or excluded?"
        ),
        "Bias Reflection Quiz": None,  # Placeholder for the interactive quiz
        "Ethical Review Template": None  # Placeholder for the Ethical Review Template
    }

    # --- Sub-topic selector ---
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown("### Building Responsible AI for Startups")
    with col_right:
        ethics_subtopic = st.selectbox(
            "Sub-topic",
            ["All"] + list(ethics_sections.keys()),
            key="ethics_subtopic"
        )

    # --- Display sections with checkboxes ---
    for title, content in ethics_sections.items():
        if ethics_subtopic == "All" or ethics_subtopic == title:
            with expander_section(title):
                if title == "Ethical Review Template":
                    # Logic for the Ethical Review Template
                    st.markdown("### What Is This Template?")
                    st.write("""
                    This is a structured form to help startup teams evaluate whether an AI-powered feature is being designed and used ethically and responsibly.
                    It’s useful for catching potential risks early — like bias, misinformation, or lack of transparency.
                    """)

                    st.markdown("### When Should You Use It?")
                    st.markdown("""
                    - When building any new feature that involves LLMs or AI-generated content  
                    - Before launching customer-facing AI functionality  
                    - During internal QA or product review meetings  
                    """)

                    st.markdown("### How to Use It")
                    st.write("""
                    Complete the form below as a team (product, design, engineering).  
                    Save or export the answers as part of your product documentation or AI governance records.
                    """)

                    st.markdown("### Why It’s Useful for Startups")
                    st.write("""
                        - Helps meet ethical and legal expectations early in your product lifecycle
                        - Builds trust with your users and investors
                        - Prevents future reputational or legal risk
                        - Encourages intentional, responsible design decisions
                        """)
                elif title == "Bias Reflection Quiz":
                    # Interactive Bias Reflection Quiz
                    st.markdown("#### Try This Quiz")
                    st.write("Which of these might reflect bias?")

                    # Define quiz options
                    options = [
                        "-- Select an answer --",
                        "Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'",
                        "Summarize a product spec for a software tool",
                        "Generate a welcome message for a task management app"
                    ]

                    # Add a radio button for the quiz
                    selected_option = st.radio("Select the option you think reflects bias:", options, key="bias_quiz")

                    # Provide feedback based on the user's selection
                    if selected_option == options[1]:
                        st.success("Correct! The first option assumes gender and age, which may reflect bias.")
                    elif selected_option in options[2:]:
                        st.error("Not quite. The first option reflects bias due to assumptions about gender and age.")
                else:
                    # Display content for other sections
                    col1, col2 = st.columns([5, 1])
                    with col2:
                        checkbox_key = f"read_checkbox_{title}"
                        if checkbox_key not in st.session_state:
                            st.session_state[checkbox_key] = title in st.session_state["ethics_read_sections"]

                        completed = st.checkbox("Mark as complete", key=checkbox_key, value=st.session_state[checkbox_key])
                        if completed:
                            st.session_state["ethics_read_sections"].add(title)
                        else:
                            st.session_state["ethics_read_sections"].discard(title)

                    st.markdown(content)

    # --- Progress tracking ---
    total_sections = len(ethics_sections)
    read_sections = len(st.session_state["ethics_read_sections"])
    progress = int((read_sections / total_sections) * 100)

    st.markdown("### Your Reading Progress")
    st.progress(progress)
    st.caption(f"You’ve completed **{read_sections} of {total_sections}** sections ({progress}%)")
    
    if st.button("Reset Progress"):
        reset_progress(ethics_sections, "ethics_read_sections")
        st.rerun()

    # Save progress to file whenever it changes
    save_progress("ethics_read_sections")
      # Display success message if reset was triggered
    if st.session_state.get("reset_triggered", False):
        st.success("Progress reset! All checkboxes have been cleared.")
        # Clear the flag after displaying the message
        st.session_state["reset_triggered"] = False
    reset_expand_collapse_triggers()

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; font-size: 14px; line-height: 1.6;'>
            <strong>LLM Guide for Startups</strong> — Practical insights for using language models responsibly and efficiently in startup settings.<br>
            Built with  by:<br>
            • <strong>Vaishnavi Kandikonda - 24216940 </strong> — <a href="mailto:vaishnavi.kandikonda@ucdconnect.com">vaishnavi.kandikonda@ucdconnect.com</a><br>
            • <strong>Shivani Singh - 24234516 </strong> — <a href="mailto:shivani.singh@ucdconnect.ie">shivani.singh@ucdconnect.ie</a><br>
            • <strong>Kushal Pratap Singh - 24205476 </strong> — <a href="mailto:kushal.singh@ucdconnect.ie">kushal.singh@ucdconnect.ie</a><br><br>
            © 2025 LLM Startup Guide • Last updated {last_updated} • Built with Streamlit • Guided by principles of transparency, fairness, and human-centered AI.
        </div>
        """.format(last_updated=datetime.now().strftime("%Y-%m-%d")),
        unsafe_allow_html=True
    )