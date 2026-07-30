import streamlit as st
from auth import login_gate

st.set_page_config(
    page_title="Texas Wholesaler Pro",
    page_icon="🤠",
    layout="wide"
)

login_gate()

st.title("🤠 Texas Wholesaler Pro")
st.caption("AI-powered deal intelligence system for wholesalers")

st.markdown("""
### Use the sidebar to navigate:
- 🧮 Deal Analyzer
- 📦 CRM Pipeline
- ⚖️ Compliance Guide
""")
