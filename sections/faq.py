import streamlit as st
from datetime import datetime
from utils.helpers import display_expand_collapse_controls, expander_section,inject_custom_css

def render():
    inject_custom_css()
    current_page = "FAQs"
    st.title("Frequently Asked Questions")
    display_expand_collapse_controls(current_page)

    faq_sections = {
        "What is a large language model (LLM)?": (
            "A large language model (LLM) is an AI system trained to generate and understand human-like text. "
            "It can help you write, summarize, explain, and automate content in your startup workflows."
        ),
        "Is ChatGPT the same as a search engine?": (
            "No. ChatGPT doesn’t search the internet live. It generates responses based on patterns learned from training data. "
            "It doesn’t verify facts, so double-check anything important."
        ),
        "Why does it sometimes say things that are wrong?": (
            "This is called a hallucination. The model doesn’t know what’s true — it just predicts what sounds right. "
            "Always review AI-generated content before using it externally."
        ),
        "How can I control the tone or creativity of the AI's response?": (
            "Use the temperature setting. Lower values (e.g., 0.2) generate more factual, safe content. "
            "Higher values (e.g., 0.8) create more creative or varied outputs."
        ),
        "Will using LLMs increase my startup’s costs?": (
            "It can. LLMs charge based on token usage. Use prompt optimization, shorter outputs, model tiering (e.g., GPT-3.5 over GPT-4), "
            "and batch processing to control costs."
        ),
        "Can I use LLMs for decisions like hiring or pricing?": (
            "Only with caution. LLMs can reflect social bias and make mistakes. Never automate high-stakes decisions without human review."
        ),
        "How do I avoid biased or exclusionary outputs?": (
            "Test prompts using diverse scenarios. Be mindful of wording that assumes gender, age, or culture. "
            "Use a review process before publishing AI-generated content."
        )
    }

    # --- FAQ Sections ---
    for title, content in faq_sections.items():
        with expander_section(title):
            st.write(content)

    # --- Final Note ---
    st.markdown("Have more questions? Use the **feedback form** in the sidebar to help us expand this section.")

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