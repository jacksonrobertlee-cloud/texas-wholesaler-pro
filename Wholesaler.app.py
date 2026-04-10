import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import datetime
import io

# ========================================
# TEXAS WHOLESALER PRO v2.0
# Compliance + Deal Analysis + Content Engine
# ========================================

st.set_page_config(
    page_title="Texas Wholesaler Pro",
    page_icon="🤠",
    layout="wide"
)

# -----------------------------
# SAFE UTILS
# -----------------------------
def safe_text(value, fallback="N/A"):
    return value if value else fallback

def text_to_audio_html(text):
    """Audio generator with safe fallback"""
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        return f'<audio controls src="data:audio/mp3;base64,{b64}">'
    except:
        return "🔇 Audio unavailable (hosted environment restriction)"

# -----------------------------
# DEAL ENGINE
# -----------------------------
def calculate_mao(arv, repairs, fee, rule_percent):
    arv = float(arv or 0)
    repairs = float(repairs or 0)
    fee = float(fee or 0)

    mao = (arv * rule_percent) - repairs - fee
    return mao

# -----------------------------
# STATE INIT (CRM STYLE)
# -----------------------------
if "leads" not in st.session_state:
    st.session_state.leads = []

if "deal_log" not in st.session_state:
    st.session_state.deal_log = []

# -----------------------------
# HEADER
# -----------------------------
st.title("🤠 Texas Wholesaler Pro v2.0")
st.caption("Deal Analyzer | Content Engine | Compliance-Aware Workflow Tool")

# -----------------------------
# SIDEBAR (PIPELINE TRACKING)
# -----------------------------
with st.sidebar:
    st.header("📊 Deal Pipeline")

    st.write(f"Total Deals Reviewed: **{len(st.session_state.deal_log)}**")
    st.write(f"Saved Leads: **{len(st.session_state.leads)}**")

    st.divider()
    st.subheader("Recent Activity")

    for lead in st.session_state.leads[-5:]:
        st.caption(f"📍 {lead['address']} | MAO ${lead['mao']:,.0f}")

    st.divider()
    rule_selector = st.slider("Investment Rule (%)", 60, 80, 70) / 100
    st.info("Standard Houston wholesale range: 65–75%")

# -----------------------------
# TABS
# -----------------------------
tab_calc, tab_script, tab_compliance, tab_pipeline = st.tabs([
    "🧮 Deal Analyzer",
    "🎥 Content Script Tool",
    "⚖️ Compliance Guide",
    "📦 Pipeline / Skiptrace Tracker"
])

# -----------------------------
# TAB 1 — DEAL ANALYZER
# -----------------------------
with tab_calc:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Property Inputs")

        address = st.text_input("Property Address")
        arv = st.number_input("ARV (After Repair Value)", value=250000, step=5000)
        repairs = st.number_input("Repair Estimate", value=35000, step=1000)
        fee = st.number_input("Assignment Fee Target", value=10000, step=1000)

        mao = calculate_mao(arv, repairs, fee, rule_selector)

    with col2:
        st.subheader("Deal Output")

        st.metric("Max Allowable Offer (MAO)", f"${mao:,.2f}")

        st.write("### ✔ Deal Checklist")
        c1 = st.checkbox("ARV verified (comps checked)")
        c2 = st.checkbox("Repairs estimated realistically")
        c3 = st.checkbox("Deal reviewed on video (content captured)")

        if mao > 0 and c1 and c2:
            st.success("🔥 DEAL LOOKS VIABLE")

            if st.button("💾 Save to Pipeline"):
                st.session_state.leads.append({
                    "address": address,
                    "mao": mao,
                    "date": str(datetime.date.today()),
                    "status": "analyzing"
                })

                st.session_state.deal_log.append(address)

                st.balloons()

        elif mao <= 0:
            st.warning("⚠️ Deal not strong at current numbers")

# -----------------------------
# TAB 2 — CONTENT SCRIPT ENGINE
# -----------------------------
with tab_script:
    st.subheader("🎥 On-Site Recording Script Generator")

    safe_address = safe_text(address, "this property")

    pitch_text = f"""
I'm standing in front of {safe_address}.

Based on my analysis:
- ARV: ${arv:,.0f}
- Estimated repairs: ${repairs:,.0f}
- My maximum allowable offer is approximately ${mao:,.0f}

This tells me whether this is a deal worth pursuing or skipping.

I use data—not emotion—to make real estate decisions.
"""

    st.info(pitch_text)

    st.write("### 🔊 Practice Your Script")

    audio_html = text_to_audio_html(pitch_text)
    st.markdown(audio_html, unsafe_allow_html=True)

    st.caption("Use this while recording on-site walkthrough videos.")

# -----------------------------
# TAB 3 — COMPLIANCE GUIDE
# -----------------------------
with tab_compliance:
    st.subheader("⚖️ Texas Wholesaling Compliance (Plain English)")

    st.warning("You must clearly disclose equitable interest when assigning contracts.")

    with st.expander("What you CAN say"):
        st.write("""
- "I have equitable interest in this property"
- "I am assigning my contract rights"
- "This is a wholesale transaction"
- "I am marketing a contract, not the real estate itself"
""")

    with st.expander("What you CANNOT say"):
        st.write("""
- "I own this property"
- "I am the buyer"
- "I can guarantee purchase"
- Any misleading representation of ownership
""")

    st.write("### Required Assignment Language")

    compliance_text = f"""
Buyer acknowledges that Seller (Wholesaler) has an equitable interest in {safe_address} and is assigning contractual rights for consideration.
"""

    st.code(compliance_text, language="text")

# -----------------------------
# TAB 4 — PIPELINE / SKIPTRACE TRACKER
# -----------------------------
with tab_pipeline:
    st.subheader("📦 Deal Pipeline Tracker (CRM Lite)")

    if st.session_state.leads:
        df = pd.DataFrame(st.session_state.leads)
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "⬇ Export Pipeline CSV",
            df.to_csv(index=False),
            file_name="wholesale_pipeline.csv"
        )
    else:
        st.info("No deals saved yet.")

    st.divider()

    st.subheader("📮 Next Actions Workflow")

    st.write("""
1. Analyze deal in app  
2. Record on-site video (use script tab)  
3. Save lead if viable  
4. Skip trace owner  
5. Send mailer / outreach  
6. Follow up and negotiate  
""")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("Texas Wholesaler Pro v2.0 | Built for Deal Flow + Content Creation + Compliance Awareness")