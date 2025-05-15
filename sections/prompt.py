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
    current_page = "Prompt Engineering"
    st.title("Prompt Like a Pro")
    display_expand_collapse_controls(current_page)

    # --- Load progress from file ---
    if "prompt_read_sections" not in st.session_state:
        progress_data = load_progress()
        st.session_state["prompt_read_sections"] = set(progress_data.get("prompt_read_sections", []))

    # --- Define sections for progress tracking ---
    prompt_sections = {
        "Introduction to Prompt Engineering": (
            "A **prompt** is the instruction you give to an AI model. Think of it like a creative brief — "
            "the clearer you are, the better the output.\n\n"
            "**Prompt Engineering** is the practice of crafting clear and effective inputs (prompts) to guide large language models (LLMs) like GPT-4. "
            "Think of it like writing instructions to a very smart assistant — the better your instructions, the better the output.\n\n"
            "#### Why It Matters for Startups\n"
            "- Speeds up content generation and prototyping\n"
            "- Powers customer support chatbots and assistants\n"
            "- Helps in idea generation, naming, and brainstorming\n"
            "- Reduces reliance on manual copywriting, support, or even coding"
        ),
        "Types of Prompts": (
            "Different types of prompts serve different needs. Here are the most common:\n\n"
            "#### Zero-shot Prompting\n"
            "No examples are provided. The model relies entirely on the instruction.\n"
            "- *Example:* \"Write a one-line product description for a fitness tracker.\"\n\n"
            "#### One-shot Prompting\n"
            "A single example is included.\n"
            "- *Example:*  \n"
            "  Q: What’s 2 + 2? A: 4  \n"
            "  Q: What’s 7 + 5?\n\n"
            "#### Few-shot Prompting\n"
            "Multiple examples help guide the model.\n"
            "- *Example:*  \n"
            "  \"Translate: EN: Hello → ES: Hola. EN: Thank you → ES: Gracias.\"\n\n"
            "#### Instructional vs Conversational\n"
            "- **Instructional:** Direct commands like “Summarize this email in 3 lines.”\n"
            "- **Conversational:** Framed as a dialogue, e.g., “Hi! Can you help me explain this concept to a 10-year-old?”"
        ),
        "Vague vs. Clear Examples": (
            "#### Vague Prompt\n"
            "- Describe our app\n"
            "- Write something about our new feature\n\n"
            "#### Clear Prompt\n"
            "- Write a 3-sentence product description...\n"
            "- Write a 2-sentence announcement..."
        ),
        "Prompt Best Practices": (
            "Great prompts are clear, structured, and targeted.\n\n"
            "#### Key Techniques\n"
            "- **Be Clear & Specific:** Avoid vague instructions.\n"
            "- **Use Delimiters:** Separate instructions from content with `\"\"\"` or `---`.\n"
            "- **Step-by-Step Instructions:** Ask the model to \"explain step-by-step\" when needed.\n"
            "- **Set a Role:** E.g., \"You are a technical recruiter.\"\n"
            "- **Define Output Format:** Specify number of bullets, length, tone, etc.\n"
            "- **Iterate:** Rerun and refine based on what works.\n\n"
            "_Example Prompt:_  \n"
            "> \"You are a SaaS marketer. Write a 2-sentence announcement for our AI onboarding tool, in a friendly tone.\""
        ),
        "Common Pitfalls": (
            "Even simple prompts can fail if they're poorly structured. Here are key mistakes to avoid:\n\n"
            "- **Ambiguity:** “Tell me about our product” — too vague.\n"
            "- **Overloading Instructions:** Don't cram 5 tasks into 1 prompt.\n"
            "- **Missing Context:** Always provide enough background for the model to understand the task."
        ),
        "Prompt Engineering vs Prompt Tuning": (
            "While both involve improving how AI generates output, they differ significantly:\n\n"
            "- **Prompt Engineering**  \n"
            "  Uses well-crafted text prompts to control output. No training required. Fast and flexible.\n\n"
            "- **Prompt Tuning (Advanced)**  \n"
            "  Involves fine-tuning the model on a custom dataset. Requires ML knowledge, compute resources, and time.\n\n"
            "_Prompt Engineering is ideal for startups needing quick results without deep ML expertise._"
        ),
        "Startup Use Cases": (
            "Prompt engineering can unlock huge value across startup functions:\n\n"
            "- **Marketing:** Social media posts, taglines, blog intros\n"
            "- **Customer Support:** Smart autoresponders, refund replies\n"
            "- **Product & Dev:** Auto-generate feature descriptions, bug summaries\n"
            "- **Branding:** Name generation, slogan ideas, elevator pitches"
        ),
        "Prompt Learning Resources": (
            "Dive deeper into the art and science of prompting with these free resources:\n\n"
            "- [OpenAI Cookbook – Prompting Guide](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb)\n"
            "- [PromptHero (Community Examples)](https://prompthero.com/)\n"
            "- [FlowGPT – Community Prompt Library](https://flowgpt.com/)\n"
            "- [Full Guide to Prompt Engineering](https://www.promptingguide.ai/)"
        ),
        "Quiz": (
            "Test your knowledge of prompt engineering with this interactive quiz!"
        )
    }

    # --- Sub-topic selector ---
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown("### Explore Prompt Engineering Concepts")
    with col_right:
        subtopic = st.selectbox("Sub-topic", ["All"] + list(prompt_sections.keys()), key="prompt_subtopic")

    # --- Display sections with expanders ---
    for title, content in prompt_sections.items():
        if subtopic == "All" or subtopic == title:
            with expander_section(title):
                # Header with checkbox on the right
                top_col_left, top_col_right = st.columns([5, 1])
                with top_col_right:
                    checkbox_key = f"read_checkbox_{title}"

                    # Initialize checkbox state if not already set
                    if checkbox_key not in st.session_state:
                        st.session_state[checkbox_key] = title in st.session_state["prompt_read_sections"]

                    # Render the checkbox
                    completed = st.checkbox("Mark as complete", key=checkbox_key, value=st.session_state[checkbox_key])

                    # Sync read_sections with checkbox state
                    if completed:
                        st.session_state["prompt_read_sections"].add(title)
                    else:
                        st.session_state["prompt_read_sections"].discard(title)

                if title == "Quiz":
                    # Interactive Quiz
                    q1 = st.radio("1. What makes a good prompt?", [
                        "-- Select an answer --",
                        "Something short like 'Write something'",
                        "Clear instructions with role, format, and topic",
                        "Anything, the AI will figure it out"
                    ])
                    if q1 != "-- Select an answer --":
                        if q1 == "Clear instructions with role, format, and topic":
                            st.success("Correct!")
                        else:
                            st.error("Try again.")

                    q2 = st.radio("2. Which is a strong ad prompt?", [
                        "-- Select an answer --",
                        "Write an ad",
                        "Write a 2-line ad copy for a wearable fitness tracker targeting new moms in a friendly tone",
                        "Make something catchy"
                    ])
                    if q2 != "-- Select an answer --":
                        if "fitness tracker" in q2:
                            st.success("Spot on!")
                        else:
                            st.error("Try again.")

                    q3 = st.radio("3. True or False: AI always knows your intent.", [
                        "-- Select an answer --",
                        "True",
                        "False"
                    ])
                    if q3 != "-- Select an answer --":
                        if q3 == "False":
                            st.success("Correct!")
                        else:
                            st.error("Incorrect.")
                else:
                    st.markdown(content)

    # --- Progress tracking ---
    total_sections = len(prompt_sections)
    read_sections = len(st.session_state["prompt_read_sections"])
    progress = int((read_sections / total_sections) * 100)

    st.markdown("### Your Reading Progress")
    st.progress(progress)
    st.caption(f"You’ve completed **{read_sections} of {total_sections}** sections ({progress}%)")
    
    if st.button("Reset Progress"):
        reset_progress(prompt_sections, "prompt_read_sections")
        st.rerun()

    # Save progress to file whenever it changes
    save_progress("prompt_read_sections")
    
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