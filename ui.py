import streamlit as st

def card(title, text, emoji="📦"):
    st.markdown(f"""
    <div style="
        padding:16px;
        border-radius:12px;
        background-color:#151C2C;
        border:1px solid #26324A;
        margin-bottom:12px;
    ">
        <h3>{emoji} {title}</h3>
        <p style="color:#B8C0CC;">{text}</p>
    </div>
    """, unsafe_allow_html=True)