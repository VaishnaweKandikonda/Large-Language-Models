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

def render(): 
    inject_custom_css() 
    current_page = "Home"
    st.markdown("<h1 style='text-align:center; margin: 0;'>Smart Startups. Smart AI.</h1>", unsafe_allow_html=True)
    display_expand_collapse_controls(current_page)

    # --- Load progress from file ---
    if "home_read_sections" not in st.session_state:
        progress_data = load_progress()
        st.session_state["home_read_sections"] = set(progress_data.get("home_read_sections", []))
        
    # --- Define Home page sections ---
    home_sections = {
        "Introduction to Large Language Models": (
            "Large Language Models (LLMs) are smart computer programs that can read, understand, and write text like a human. "
            "They are trained by reading huge amounts of information from books, websites, and articles. "
            "This helps them learn how people use language, so they can help in many useful ways:\n\n"
            "- Answer questions and explain things clearly\n"
            "- Write emails, blog posts, or summaries\n"
            "- Assist with code generation and debugging\n"
            "- Translate between different languages\n"
            "- Support tasks in education, business, and creative work\n\n"
            "**In Simple Terms:**\n"
            "- LLMs power chatbots like ChatGPT, Claude, and Google Gemini.\n"
            "- They’re trained on billions of words from the internet.\n"
            "- Widely used in customer service, education, content creation, and tools."
        ),
        "How Language Models Work": (
            "LLMs are trained using large amounts of text to learn patterns in language. "
            "They don’t understand meaning like humans do — instead, they predict the most likely next word or phrase based on what you type.\n\n"
            "**How LLMs generate text:**\n"
            "- You provide a prompt or question.\n"
            "- The model predicts the next word, again and again, to form a full response.\n"
            "- It uses probabilities learned during training to decide what comes next.\n\n"
            "**What's a token?**\n"
            "- A token is a small piece of text — like a word or part of a word.\n"
            "- For example, “Startup” might become “Start” and “up.”\n"
            "- Most AI tools charge based on the number of tokens processed.\n\n"
            "**Key takeaway:**\n"
            "- LLMs aren’t search engines — they don’t know facts.\n"
            "- They generate likely-sounding responses. Always verify important info!"
        ),
        "Why LLMs Matter for Startups": (
            "Startups often need to move fast with limited resources. LLMs help teams work more efficiently, build smarter tools, and scale faster without needing big teams.\n\n"
            "- Automate customer support and answer FAQs\n"
            "- Write product descriptions, blog posts, and marketing emails\n"
            "- Build chatbots and interactive assistants quickly\n"
            "- Speed up MVP development with code generation and idea testing\n"
            "- Save time on repetitive tasks and research"
        ),
        "Best Practices & Ethics": (
            "Using LLMs wisely ensures safe, fair, and productive outcomes. Here are some key best practices to follow:\n\n"
            "- Write clear, specific prompts for better results\n"
            "- Learn how model temperature affects creativity and accuracy\n"
            "- Don’t rely on AI for factual truth — always double-check\n"
            "- Monitor and manage API usage to control costs\n"
            "- Be aware of potential bias, fairness issues, and ethical concerns"
        ),
        "Who Should Use This Guide": (
            "This guide is built for anyone curious about applying LLMs in a startup or business setting — no technical background required.\n\n"
            "- Startup founders exploring how AI can boost their business\n"
            "- Product managers and developers building AI features\n"
            "- Marketing and content teams looking to scale output\n"
            "- Investors or advisors evaluating AI strategies\n"
            "- Curious learners who want to understand AI in practical terms"
        ),
        "Let's Get Started!": (
            "Use the left menu to explore helpful topics, real use cases, and interactive tools. "
            "You’ll find step-by-step guidance to help you start using AI effectively — whether for writing, coding, customer support, or product development.\n\n"
            "- Browse each section to learn more\n"
            "- Try interactive examples and tools\n"
            "- Get inspired by practical applications for startups\n"
            "- Start small and scale smart with LLMs"
        )
    }
    # Sub-topic selector
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown("### Explore Large Language Models Concepts")
    with col_right:
        default_index = 0  # "All" is the first item
        subtopic = st.selectbox("Sub-topic", ["All"] + list(home_sections.keys()), key="Sub-topic", index=default_index)

    # Display sections with expanders
    for title, content in home_sections.items():
        if subtopic == "All" or subtopic == title:
            with expander_section(title):
                top_col_left, top_col_right = st.columns([5, 1])
                with top_col_right:
                    checkbox_key = f"read_checkbox_{title}"
                    if checkbox_key not in st.session_state:
                        st.session_state[checkbox_key] = title in st.session_state["home_read_sections"]

                    completed = st.checkbox("Mark as complete", key=checkbox_key, value=st.session_state[checkbox_key])
                    if completed:
                        st.session_state["home_read_sections"].add(title)
                    else:
                        st.session_state["home_read_sections"].discard(title)
                st.markdown(content)

    # --- Progress tracking ---
    total_sections = len(home_sections)
    read_sections = len(st.session_state["home_read_sections"])
    progress = int((read_sections / total_sections) * 100)

    st.markdown("### Your Reading Progress",unsafe_allow_html=True)
    st.progress(progress)
    st.caption(f"You’ve completed **{read_sections} of {total_sections}** sections ({progress}%)")
    
    if st.button("Reset Progress"):
        reset_progress(home_sections, "home_read_sections")
        st.rerun()

    # Display success message if reset was triggered
    if st.session_state.get("reset_triggered", False):
        st.success("Progress reset! All checkboxes have been cleared.")
        # Clear the flag after displaying the message
        st.session_state["reset_triggered"] = False
    
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