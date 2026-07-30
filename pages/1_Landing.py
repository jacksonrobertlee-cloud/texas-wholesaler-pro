import streamlit as st
from auth import login_gate
from utils.ui import card

st.set_page_config(
    page_title="Texas Wholesaler Pro — Landing",
    page_icon="🤠",
    layout="wide"
)

login_gate()

st.title("🤠 Texas Wholesaler Pro")
st.caption("AI-powered deal intelligence system for real estate wholesalers")

st.divider()

st.markdown("""
## ⚡ Turn Property Data Into Fast Profit Decisions

Analyze deals, generate content, and stay compliant — all in one place.
""")

col1, col2 = st.columns([2, 1])

with col1:
    card("Instant MAO Calculator", "Know your max offer in seconds.", "🧮")
    card("Content Script Generator", "Turn deals into walkthrough videos.", "🎥")
    card("Compliance Protection", "Stay legally safe with disclosures.", "⚖️")

with col2:
    st.metric("Avg Decision Time", "12 sec")
    st.metric("Deals Modeled", "1,200+")

st.divider()

if st.button("🚀 Start Analyzing Deals", use_container_width=True):
    st.switch_page("pages/2_DealAnalyzer.py")
