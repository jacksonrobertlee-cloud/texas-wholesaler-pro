import streamlit as st
from datetime import date
from auth import login_gate
from utils.calculations import calculate_mao

st.set_page_config(
    page_title="Texas Wholesaler Pro — Deal Analyzer",
    page_icon="🧮",
    layout="wide"
)

login_gate()

if "leads" not in st.session_state:
    st.session_state.leads = []

st.title("🧮 Deal Analyzer")
st.caption("Run real-time wholesale deal analysis")

st.divider()

col1, col2 = st.columns(2)

with col1:
    address = st.text_input("Property Address", "")
    arv = st.number_input("ARV", 250000)
    repairs = st.number_input("Repairs", 30000)
    fee = st.number_input("Assignment Fee", 10000)
    rule = st.slider("Investment Rule %", 60, 80, 70) / 100

mao = calculate_mao(arv, repairs, fee, rule)

with col2:
    st.metric("Max Allowable Offer", f"${mao:,.0f}")

    if mao > 0:
        st.success("🔥 DEAL LOOKS STRONG")
    else:
        st.warning("⚠️ Weak Deal")

st.divider()

with st.spinner("Analyzing deal..."):
    import time
    time.sleep(1)

st.info("Analysis complete.")

st.divider()

if st.button("💾 Save Deal to Pipeline", use_container_width=True):
    st.session_state.leads.append({
        "address": address if address else "(no address entered)",
        "arv": arv,
        "repairs": repairs,
        "assignment_fee": fee,
        "rule_pct": rule,
        "mao": mao,
        "status": "New Lead",
        "date_added": date.today().isoformat(),
    })
    st.success(f"Saved to pipeline — {len(st.session_state.leads)} deal(s) total. Check the CRM Pipeline page.")
