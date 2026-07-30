import streamlit as st

def login_gate():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        st.title("🔐 Login to Texas Wholesaler Pro")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email and password:
                st.session_state.user = email
                st.rerun()

        st.stop()
