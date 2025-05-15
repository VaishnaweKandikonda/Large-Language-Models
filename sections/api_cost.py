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
    current_page = "API Cost Optimization"
    st.title("API Cost Optimization")
    display_expand_collapse_controls(current_page)

    # --- Load progress from file ---
    if "api_cost_read_sections" not in st.session_state:
        progress_data = load_progress()
        st.session_state["api_cost_read_sections"] = set(progress_data.get("api_cost_read_sections", []))

    # --- Define sections for progress tracking ---
    api_sections = {
        "What Is API Cost?",
        "Why API Costs Matter",
        "What Drives Cost",
        "Optimization Strategies",
        "Estimate Token Cost",
        "Final Note"
    }

    # --- Sub-topic selector ---
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown("### Build Smart, Spend Smarter")
    with col_right:
        cost_subtopic = st.selectbox(
            "Sub-topic",
            ["All"] + list(api_sections),
            key="api_cost_subtopic"
        )

    # --- Display sections with expanders ---

    for title in api_sections:
        if cost_subtopic == "All" or cost_subtopic == title:
            with expander_section(title):
                # Define two columns for layout
                top_col_left, top_col_right = st.columns([5, 1])

                with top_col_right:
                    checkbox_key = f"read_checkbox_{title}"

                    # Initialize checkbox state if not already set
                    if checkbox_key not in st.session_state:
                        st.session_state[checkbox_key] = title in st.session_state["api_cost_read_sections"]

                    # Render the checkbox
                    completed = st.checkbox("Mark as complete", key=checkbox_key, value=st.session_state[checkbox_key])

                    # Sync read_sections with checkbox state
                    if completed:
                        st.session_state["api_cost_read_sections"].add(title)
                    else:
                        st.session_state["api_cost_read_sections"].discard(title)

                # Render content for each section
                if title == "What Is API Cost?":
                    st.write("""
                    When you use a language model like GPT-3.5 or GPT-4 through an API, you’re charged based on how many tokens you send and receive.

                    A **token** is typically 3–4 characters or about 1 word. You are billed for both the prompt you send and the response the model generates.

                    Different models have different pricing structures:
                    """)
                    st.markdown("""
                    | Model         | Input (per 1K tokens) | Output (per 1K tokens) |
                    |---------------|-----------------------|------------------------|
                    | GPT-3.5 Turbo | $0.0015               | $0.002                 |
                    | GPT-4 Turbo   | $0.01                 | $0.03                  |
                    | GPT-4 (8K)    | $0.03                 | $0.06                  |
                    """)

                elif title == "Why API Costs Matter":
                    st.write("""
                    Using large language models can get expensive quickly — especially if your product sends long prompts or handles frequent requests.

                    For example:
                    - Daily chat summaries for users
                    - Auto-generating blog content
                    - AI customer support

                    Managing cost ensures your startup scales **sustainably**.
                    """)

                elif title == "What Drives Cost":
                    st.markdown("""
                    - **Token usage** – You pay per word/token (input + output combined).  
                    - **Model selection** – GPT-4 is significantly more expensive than GPT-3.5.  
                    - **Request frequency** – High-volume traffic means higher cost.  
                    - **Prompt design** – Long prompts or unnecessary verbosity waste tokens.  
                    """)

                elif title == "Optimization Strategies":
                    st.markdown("""
                    1. **Shorten prompts**: Cut boilerplate or redundant phrasing.  
                    2. **Use cheaper models**: GPT-3.5 for summaries, formatting, etc.  
                    3. **Cache outputs**: Reuse LLM responses for repeated queries.  
                    4. **Batch processing**: Combine inputs in a single request.  
                    5. **Analyze usage logs**: Monitor which calls are most expensive.  
                    """)

                elif title == "Estimate Token Cost":
                    st.markdown("Estimate how much your startup might spend based on usage.")

                    model_choice = st.selectbox(
                        "Choose your model",
                        ["GPT-3.5 Turbo", "GPT-4 Turbo", "GPT-4 (8K)"]
                    )

                    tokens_in = st.slider("Prompt tokens per request", 100, 4000, step=100, value=500)
                    tokens_out = st.slider("Response tokens per request", 100, 4000, step=100, value=500)
                    requests_per_day = st.slider("Number of requests per day", 10, 5000, step=50, value=1000)

                    # Define cost rates per model
                    rates = {
                        "GPT-3.5 Turbo": {"in": 0.0015, "out": 0.002},
                        "GPT-4 Turbo": {"in": 0.01, "out": 0.03},
                        "GPT-4 (8K)": {"in": 0.03, "out": 0.06}
                    }

                    rate = rates[model_choice]
                    daily_cost = ((tokens_in * rate["in"] + tokens_out * rate["out"]) / 1000) * requests_per_day
                    monthly_cost = daily_cost * 30

                    st.info(f"**Estimated Daily Cost:** ${daily_cost:,.2f}")
                    st.success(f"**Estimated Monthly Cost:** ${monthly_cost:,.2f}")

                elif title == "Final Note":
                    st.markdown("""
                    API costs are invisible until they scale — and then they scale fast.

                    Be proactive:  
                    ✅ Track usage  
                    ✅ Test models before deploying  
                    ✅ Fine-tune or retrieve where appropriate

                    Optimizing cost = longer runway + happier investors.
                    """)


    # --- Reading Progress ---
    total = len(api_sections)
    completed = len(st.session_state["api_cost_read_sections"])
    percent = int((completed / total) * 100)

    st.markdown("### Your Reading Progress")
    st.progress(percent)
    st.caption(f"You’ve completed **{completed} of {total}** sections ({percent}%)")

    # --- Reset Progress Button ---
    if st.button("Reset Progress"):
        reset_progress(api_sections)

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