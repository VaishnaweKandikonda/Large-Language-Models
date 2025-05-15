import streamlit as st
from datetime import datetime  # Import datetime for the footer
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
    current_page = "Temperature & Sampling"
    st.title("Temperature & Sampling")
    display_expand_collapse_controls(current_page)

    # --- Load progress from file ---
    if "temperature_read_sections" not in st.session_state:
        progress_data = load_progress()
        st.session_state["temperature_read_sections"] = set(progress_data.get("temperature_read_sections", []))
        
    # --- Define sections for progress tracking ---
    temperature_sections = {
        "What is Temperature?": (
            "**Temperature** controls how creative or consistent a language model’s responses are. "
            "It ranges from **0.0 (very safe)** to **1.0 (very random)**.\n\n"
            "- **Low (0.1–0.3)** → Factual, predictable, robotic\n"
            "- **Medium (0.4–0.6)** → Natural balance\n"
            "- **High (0.7–1.0)** → Creative, surprising\n\n"
            "Think of temperature as the AI’s **risk-taking slider**."
        ),
        "What is Sampling?": (
            "**Sampling** is how the model decides **which word to say next**. "
            "It picks from a range of likely options — not just the top one.\n\n"
            "- **Top-k sampling**: Picks from top *k* most likely next words\n"
            "- **Top-p sampling (nucleus)**: Picks from smallest set of words whose probability adds to *p*\n\n"
            "Sampling prevents boring, repetitive outputs — great for product copy, social posts, and blogs."
        ),
        "Adjust the Temperature": (
            "Use the slider below to adjust the temperature and see how it affects the tone and creativity of the output.\n\n"
        ),
        "Match Temp to Task": (
            "| Task                             | Best Temperature | Why                              |\n"
            "|----------------------------------|------------------|----------------------------------|\n"
            "| Legal docs or product specs      | 0.1 – 0.2        | Needs precision and consistency  |\n"
            "| Customer service replies         | 0.3 – 0.5        | Polite, friendly, on-brand       |\n"
            "| Blog intros or product stories   | 0.5 – 0.7        | Natural, slightly creative       |\n"
            "| Instagram ad or slogan ideas     | 0.8 – 1.0        | Bold, punchy, unexpected         |"
        ),
        "Summary Table": (
            "| Temperature | Output Style         | Best For                            |\n"
            "|-------------|----------------------|-------------------------------------|\n"
            "| 0.1 – 0.3   | Safe, focused         | Legal disclaimers, investor reports |\n"
            "| 0.4 – 0.7   | Balanced, natural     | Product copy, customer FAQs         |\n"
            "| 0.8 – 1.0   | Creative, surprising  | Marketing, brainstorming, social    |"
        ),
        "Common Misconceptions": (
            "| Myth                                  | Truth                                               |\n"
            "|---------------------------------------|----------------------------------------------------|\n"
            "| High temperature = more accurate      | No — it means more *variety*, not accuracy.        |\n"
            "| Low temperature is always best        | It’s best only when you want very safe output.     |\n"
            "| Sampling doesn’t matter               | It’s crucial for avoiding repetition.             |"
        ),
        "Final Takeaway": (
            "**Quick Guide:**\n"
            "- Use **low temperature** for consistent, formal content.\n"
            "- Use **high temperature** to ideate, entertain, and experiment.\n"
            "- Use **sampling** to keep outputs fresh and natural.\n\n"
            "Your AI is like a co-creator. Adjust temperature and sampling to guide tone and creativity."
        )
    }

    # --- Sub-topic selector ---
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown("### Explore Temperature & Sampling Concepts")
    with col_right:
        temp_subtopic = st.selectbox(
            "Sub-topic",
            ["All"] + list(temperature_sections.keys()),
            key="temperature_subtopic"
        )

    # --- Display sections with expanders ---
    for title, content in temperature_sections.items():
        if temp_subtopic == "All" or temp_subtopic == title:
            with expander_section(title):
                # Header with checkbox on the right
                top_col_left, top_col_right = st.columns([5, 1])
                with top_col_right:
                    checkbox_key = f"read_checkbox_{title}"

                    # Initialize checkbox state if not already set
                    if checkbox_key not in st.session_state:
                        st.session_state[checkbox_key] = title in st.session_state["temperature_read_sections"]

                    # Render the checkbox
                    completed = st.checkbox("Mark as complete", key=checkbox_key, value=st.session_state[checkbox_key])

                    # Sync read_sections with checkbox state
                    if completed:
                        st.session_state["temperature_read_sections"].add(title)
                    else:
                        st.session_state["temperature_read_sections"].discard(title)

                if title == "Adjust the Temperature":
                    st.markdown(content)
                    temp = st.slider("Choose a temperature value", 0.1, 1.0, step=0.1, value=0.7)
                    user_prompt = st.text_input("Enter a prompt to test:", "Describe our app in one sentence.")

                    if temp < 0.3:
                        st.success("Low Temperature (Factual & Consistent)")
                        st.markdown(f"> **Prompt:** {user_prompt}\n\n> **Output:** Our app helps freelancers manage budgets. It's secure and simple.")
                    elif temp < 0.7:
                        st.info("Medium Temperature (Balanced & Natural)")
                        st.markdown(f"> **Prompt:** {user_prompt}\n\n> **Output:** Meet your financial sidekick — smart, helpful, and always on call.")
                    else:
                        st.warning("High Temperature (Creative & Risky)")
                        st.markdown(f"> **Prompt:** {user_prompt}\n\n> **Output:** Money? Managed. Chaos? Cancelled. Our app is your freedom button.")
                else:
                    st.markdown(content)

    # --- Progress tracking ---
    total_sections = len(temperature_sections)
    read_sections = len(st.session_state["temperature_read_sections"])
    progress = int((read_sections / total_sections) * 100)

    st.markdown("### Your Reading Progress")
    st.progress(progress)
    st.caption(f"You’ve completed **{read_sections} of {total_sections}** sections ({progress}%)")
    
    if st.button("Reset Progress"):
        reset_progress(temperature_sections, "temperature_read_sections")
        st.rerun()

    # Save progress to file whenever it changes
    save_progress("temperature_read_sections")
    
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
            Built with by:<br>
            • <strong>Vaishnavi Kandikonda - 24216940 </strong> — <a href="mailto:vaishnavi.kandikonda@ucdconnect.com">vaishnavi.kandikonda@ucdconnect.com</a><br>
            • <strong>Shivani Singh - 24234516 </strong> — <a href="mailto:shivani.singh@ucdconnect.ie">shivani.singh@ucdconnect.ie</a><br>
            • <strong>Kushal Pratap Singh - 24205476 </strong> — <a href="mailto:kushal.singh@ucdconnect.ie">kushal.singh@ucdconnect.ie</a><br><br>
            © 2025 LLM Startup Guide • Last updated {last_updated} • Built with Streamlit • Guided by principles of transparency, fairness, and human-centered AI.
        </div>
        """.format(last_updated=datetime.now().strftime("%Y-%m-%d")),
        unsafe_allow_html=True
    )