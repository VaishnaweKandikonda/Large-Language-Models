import streamlit as st
from streamlit_option_menu import option_menu
from config import PAGE_TITLES
from utils.helpers import init_session_state
from sections import (
    home, prompt, temperature, hallucinations,
    api_cost, ethics, faq, glossary, feedback
)

# Page setup
st.set_page_config(page_title="LLM Guide for Startups", layout="wide")
init_session_state()

# Sidebar navigation with icons
with st.sidebar:
    selected_page = option_menu(
        "Sections",
        options=[
            "Home", "Prompt Engineering", "Temperature & Sampling",
            "Hallucinations", "API Cost Optimization", "Ethics & Bias",
            "FAQs", "Glossary", "Feedback"
        ],
        icons=[
            "house", "pencil", "thermometer-half", "exclamation-circle",
            "wallet", "shield-exclamation", "question-circle", "book", "envelope"
        ],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#ffffff"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#FF4B4B", "color": "white"},
        }
    )

# Route to correct page
PAGE_RENDERERS = {
    "Home": home,
    "Prompt Engineering": prompt,
    "Temperature & Sampling": temperature,
    "Hallucinations": hallucinations,
    "API Cost Optimization": api_cost,
    "Ethics & Bias": ethics,
    "FAQs": faq,
    "Glossary": glossary,
    "Feedback": feedback,
}

if selected_page in PAGE_RENDERERS:
    PAGE_RENDERERS[selected_page].render()
else:
    st.error("⚠️ Page not found.")
