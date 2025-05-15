import streamlit as st
from datetime import datetime  # Import datetime for the footer
from utils.helpers import (
    display_expand_collapse_controls,
    expander_section,
    reset_expansion_state,
    reset_expand_collapse_triggers,
    reset_progress,
    save_progress,
    load_progress,inject_custom_css
)

PROGRESS_FILE = "progress.json"

def render():
    inject_custom_css()
    current_page = "Ethics & Bias"
    st.title("Ethics and Bias in Language Models")
    display_expand_collapse_controls(current_page)

    # --- Load progress from file ---
    if "read_sections" not in st.session_state:
        progress_data = load_progress()
        st.session_state["read_sections"] = set(progress_data.get("read_sections", []))
        
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
        "Bias Reflection Quiz": (
            "#### Try This\n\n"
            "Which of these might reflect bias?\n\n"
            "- Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'\n"
            "- Summarize a product spec for a software tool\n"
            "- Generate a welcome message for a task management app\n\n"
            "**Answer:** The first option assumes gender and age, which may reflect bias."
        ),
        "Ethical Review Template": (
            "Use this ethical review form when designing any AI-powered feature.\n\n"
            "### Ethical Review Form\n\n"
            "- **Feature Name:**\n"
            "- **Bias Testing Completed?** Yes/No\n"
            "- **Human Review Process in Place?** Yes/No\n"
            "- **Final Risk Assessment:** Low/Medium/High\n"
            "- **Disclosure to Users?** Yes/No\n"
            "- **Purpose of AI Usage:**\n"
            "- **Potential Ethical Risks:**"
        )
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

    # --- Display sections with expanders ---
    for title, content in ethics_sections.items():
        if ethics_subtopic == "All" or ethics_subtopic == title:
            with expander_section(title):
                # Header with checkbox on the right
                top_col_left, top_col_right = st.columns([5, 1])
                with top_col_left:
                    st.markdown(f"#### {title}")
                with top_col_right:
                    checkbox_key = f"read_checkbox_{title}"

                    # Initialize checkbox state if not already set
                    if checkbox_key not in st.session_state:
                        st.session_state[checkbox_key] = title in st.session_state["ethics_read_sections"]

                    # Render the checkbox
                    completed = st.checkbox("Mark as complete", key=checkbox_key, value=st.session_state[checkbox_key])

                    # Sync read_sections with checkbox state
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
        reset_progress(ethics_sections)

    # Save progress to file whenever it changes
    save_progress()
    reset_expand_collapse_triggers()

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; font-size: 14px; line-height: 1.6;'>
            <strong>LLM Guide for Startups</strong> — Practical insights for using language models responsibly and efficiently in startup settings.<br>
            Built with ❤️ by:<br>
            • <strong>Vaishnavi Kandikonda</strong> — <a href="mailto:vaishnavi.kandikonda@ucdconnect.com">vaishnavi.kandikonda@ucdconnect.com</a><br>
            • <strong>Shivani Singh</strong> — <a href="mailto:shivani.singh@ucdconnect.ie">shivani.singh@ucdconnect.ie</a><br>
            • <strong>Kushal Pratap Singh</strong> — <a href="mailto:kushal.singh@ucdconnect.ie">kushal.singh@ucdconnect.ie</a><br><br>
            © 2025 LLM Startup Guide • Last updated {last_updated} • Built with Streamlit • Guided by principles of transparency, fairness, and human-centered AI.
        </div>
        """.format(last_updated=datetime.now().strftime("%Y-%m-%d")),
        unsafe_allow_html=True
    )