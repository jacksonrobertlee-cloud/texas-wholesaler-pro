import streamlit as st

def login_gate():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        st.title("🔐 Login to Texas Wholesaler Pro")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            valid_email = st.secrets.get("AUTH_EMAIL", None)
            valid_password = st.secrets.get("AUTH_PASSWORD", None)

            if not valid_email or not valid_password:
                st.error(
                    "Login isn't configured yet. Add AUTH_EMAIL and AUTH_PASSWORD "
                    "to this app's Secrets (see Streamlit Cloud → your app → Settings → Secrets)."
                )
            elif email.strip().lower() == valid_email.strip().lower() and password == valid_password:
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Incorrect email or password.")

        st.stop()

