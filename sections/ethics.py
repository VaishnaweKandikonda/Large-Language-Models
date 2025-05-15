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
        "Bias Reflection Quiz": (
            "#### Try This\n\n"
            "Which of these might reflect bias?\n\n"
            "- Write a bio for a doctor: 'Dr. Smith is a brilliant young man...'\n"
            "- Summarize a product spec for a software tool\n"
            "- Generate a welcome message for a task management app\n\n"
            "**Answer:** The first option assumes gender and age, which may reflect bias."
        ),
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

    # --- Display sections with expanders ---
    for title, content in ethics_sections.items():
        if ethics_subtopic == "All" or ethics_subtopic == title:
            with expander_section(title):
                if title == "Ethical Review Template":
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

                    with st.form("embedded_ethical_review_form"):
                        st.subheader("🔍 Ethical Review Form")

                        col1, col2 = st.columns(2)
                        with col1:
                            feature_name = st.text_input("Feature Name")
                            bias_tested = st.radio("Bias Testing Completed?", ["Yes", "No"])
                            human_review = st.radio("Human Review Process in Place?", ["Yes", "No"])
                        with col2:
                            risk_level = st.selectbox("Final Risk Assessment", ["Low", "Medium", "High"])
                            disclosure = st.radio("Disclosure to Users?", ["Yes", "No"])

                        purpose = st.text_area("Purpose of AI Usage")
                        risks = st.text_area("Potential Ethical Risks (e.g., bias, exclusion, hallucination)")

                        submitted = st.form_submit_button("Submit Review")

                        if submitted:
                            st.success("Review submitted. Please copy or document your answers for records.")
                            st.markdown("### 📄 Review Summary")
                            st.write(f"**Feature Name:** {feature_name}")
                            st.write(f"**Purpose:** {purpose}")
                            st.write(f"**Potential Risks:** {risks}")
                            st.write(f"**Bias Testing Completed:** {bias_tested}")
                            st.write(f"**Human Review In Place:** {human_review}")
                            st.write(f"**Disclosure to Users:** {disclosure}")
                            st.write(f"**Final Risk Assessment:** {risk_level}")

                            # Create a downloadable file
                            if feature_name.strip():  # Ensure the feature name is not empty
                                review_data = f"""
                                Feature Name: {feature_name}
                                Purpose: {purpose}
                                Potential Risks: {risks}
                                Bias Testing Completed: {bias_tested}
                                Human Review In Place: {human_review}
                                Disclosure to Users: {disclosure}
                                Final Risk Assessment: {risk_level}
                                """
                                review_file = io.StringIO(review_data)
                                st.download_button(
                                    label="📥 Download Review",
                                    data=review_file.getvalue(),
                                    file_name=f"{feature_name}_ethical_review.txt",
                                    mime="text/plain"
                                )
                            else:
                                st.warning("Please provide a valid feature name to enable the download.")
                else:
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

    # Save progress to file whenever it changes
    save_progress("ethics_read_sections")
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