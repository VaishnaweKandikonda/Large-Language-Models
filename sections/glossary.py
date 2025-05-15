import streamlit as st
from utils.helpers import display_expand_collapse_controls, expander_section
from fpdf import FPDF

def generate_glossary_pdf(glossary, output_path="LLM_Glossary.pdf"):
    """
    Generates a PDF file for the glossary terms and definitions.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Use a Unicode-compatible font (e.g., DejaVuSans)
    pdf.add_font("DejaVu", "", "/path/to/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Title
    pdf.set_font("DejaVu", style="B", size=16)
    pdf.cell(0, 10, "LLM Glossary", ln=True, align="C")
    pdf.ln(10)

    # Add glossary terms and definitions
    pdf.set_font("DejaVu", size=12)
    for term, definition in glossary.items():
        pdf.set_font("DejaVu", style="B", size=12)
        pdf.cell(0, 10, term, ln=True)
        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 10, definition)
        pdf.ln(5)

    # Save the PDF
    pdf.output(output_path)

def render():
    current_page = "Glossary"
    st.title("Glossary")
    display_expand_collapse_controls(current_page)

    glossary = {
        "LLM (Large Language Model)": "An AI model trained on vast text datasets to generate and understand human-like language. Examples include GPT-3.5 and GPT-4.",
        "Prompt": "The instruction or input you give to the AI model. Clear, specific prompts produce better results.",
        "Prompt Engineering": "The practice of crafting clear and effective inputs to guide large language models and achieve high-quality outputs.",
        "Zero-shot Prompting": "A prompt format that provides no examples — the model relies solely on the instruction.",
        "Few-shot Prompting": "A prompt that includes multiple examples to guide the model’s responses more effectively.",
        "Instructional Prompt": "A direct command, like 'Summarize this email in three bullet points.'",
        "Conversational Prompt": "A friendly, dialogue-based prompt like 'Hi! Can you help me explain this to a 10-year-old?'",
        "Temperature": "A setting that controls how predictable or creative the model’s output is. Lower = more deterministic, Higher = more diverse.",
        "Token": "A unit of text (like a word or subword). AI models process and charge based on tokens.",
        "Sampling": "A method for selecting which word comes next. Includes top-k and top-p (nucleus) sampling to control randomness.",
        "Top-k Sampling": "The model picks from the top k most likely next tokens.",
        "Top-p Sampling (Nucleus Sampling)": "The model selects from the smallest group of tokens whose cumulative probability is above a threshold p.",
        "Hallucination": "When a language model outputs a confident but incorrect or made-up statement.",
        "Bias": "Unintended favoritism or prejudice in model outputs, usually inherited from biased training data.",
        "Human-in-the-Loop": "A method where humans validate or oversee AI-generated outputs, especially for sensitive tasks.",
        "Model Selection": "Choosing the right AI model based on cost, capability, and complexity — e.g., GPT-4 vs FLAN-T5.",
        "Prompt Tuning": "An advanced technique that fine-tunes prompts using gradient-based optimization and training data.",
        "Use Case": "A real-world application of LLMs to solve a specific startup or business need (e.g., customer support, content generation).",
        "API Token Cost": "The pricing structure based on the number of input and output tokens processed by the model.",
        "Cost Optimization": "Strategies to reduce the cost of using AI APIs, such as shortening prompts and using cheaper models.",
        "Hallucination Risk": "The likelihood of a model generating inaccurate or fabricated content.",
        "Ethical AI": "The practice of using AI responsibly by reducing bias, ensuring fairness, and protecting user trust.",
        "Bias Checklist": "A list of considerations for detecting and minimizing bias in AI outputs or prompts.",
        "Prompt Generator": "A tool that suggests high-quality prompts for specific business or startup needs.",
        "Startup Use Case Matcher": "An interactive tool that recommends LLM use cases based on industry, goal, and team size.",
        "Temperature Control": "The process of tuning the model’s output randomness using the temperature parameter.",
        "Try it Yourself": "An interactive section where users can test prompts and view real-time LLM responses.",
        "Toolkit": "A downloadable collection of templates, guides, and resources for implementing LLMs in startups."
    }

    # --- Display Glossary Items ---
    st.markdown("### Key LLM Terms Every Startup Founder Should Know")
    for term, definition in glossary.items():
        with expander_section(term):
            st.markdown(definition)

    # --- Generate and Download PDF ---
    st.markdown("### Download Glossary")
    pdf_path = "LLM_Glossary.pdf"
    generate_glossary_pdf(glossary, pdf_path)  # Generate the PDF dynamically
    try:
        with open(pdf_path, "rb") as f:
            st.download_button("Download Glossary as PDF", f, file_name="LLM_Glossary.pdf", mime="application/pdf")
    except FileNotFoundError:
        st.error("The glossary PDF file is not available. Please contact support.")

    # --- Final Note ---
    st.markdown("Explore, test, and apply these terms as you build with LLMs in your startup.")