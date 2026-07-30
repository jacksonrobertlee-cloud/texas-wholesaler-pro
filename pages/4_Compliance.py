import streamlit as st
from auth import login_gate

st.set_page_config(
    page_title="Texas Wholesaler Pro — Compliance",
    page_icon="⚖️",
    layout="wide"
)

login_gate()

st.title("⚖️ Compliance Guide")

st.warning("Always disclose equitable interest in wholesale transactions.")

st.markdown("""
### Allowed:
- Assigning contracts
- Marketing contract rights
- Disclosing equitable interest

### Not Allowed:
- Claiming ownership
- Misrepresentation as buyer
""")
