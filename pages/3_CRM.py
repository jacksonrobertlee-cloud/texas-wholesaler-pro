import streamlit as st
import pandas as pd
from auth import login_gate

st.set_page_config(
    page_title="Texas Wholesaler Pro — CRM",
    page_icon="📦",
    layout="wide"
)

login_gate()

st.title("📦 CRM Pipeline")

if "leads" not in st.session_state:
    st.session_state.leads = []

if st.session_state.leads:
    df = pd.DataFrame(st.session_state.leads)

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Export CSV",
        df.to_csv(index=False),
        file_name="pipeline.csv"
    )
else:
    st.info("No deals saved yet. Save one from the Deal Analyzer page.")
