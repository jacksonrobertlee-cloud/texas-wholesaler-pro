import streamlit as st
from utils.calculations import calculate_mao

st.title("🧮 Deal Analyzer")
st.caption("Run real-time wholesale deal analysis")

st.divider()

col1, col2 = st.columns(2)

with col1:
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