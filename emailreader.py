import streamlit as st
import auth
import engine
from gmail_client import fetch_inbox
from urllib.parse import urlencode

st.set_page_config("IntelliMail Pro", "📩", layout="wide")

# ----------------- SESSION INIT -----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if "creds" not in st.session_state:
    st.session_state.creds = None

if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None

# ----------------- AUTH GATEWAY -----------------
def show_gateway():
    st.markdown("<h1 style='text-align:center;'>INTELLIMAIL <span style='color:#38BDF8'>PRO</span></h1>", unsafe_allow_html=True)

    params = st.query_params
    if "code" in params:
        creds = auth.exchange_code(
            params["code"],
            params["state"]
        )
        st.session_state.creds = creds
        st.session_state.auth = True
        st.query_params.clear()
        st.rerun()

    auth_url, state = auth.get_auth_url()
    st.session_state.oauth_state = state

    st.markdown(
        f"""
        <a href="{auth_url}">
        <button style="
            width:100%;
            padding:14px;
            font-size:16px;
            background:#4285F4;
            color:white;
            border:none;
            border-radius:6px;">
            Sign in with Google
        </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# ----------------- DASHBOARD -----------------
def main_dashboard():
    with st.sidebar:
        st.title("INTELLIMAIL")
        st.status(engine.get_api_status())
        if st.button("Terminate Session"):
            st.session_state.clear()
            st.rerun()

    emails = fetch_inbox(st.session_state.creds)

    col_list, col_view = st.columns([1, 2])

    with col_list:
        st.subheader("Intelligence Stream")
        for i, mail in enumerate(emails):
            if st.button(mail["subject"], key=i):
                st.session_state.current_mail = mail

    with col_view:
        if "current_mail" in st.session_state:
            m = st.session_state.current_mail
            ai = engine.IntelliMailEngine()

            with st.spinner("Analyzing email..."):
                res = ai.analyze_email(m["body"], m["sender"])

            st.title(m["subject"])
            st.info(res.summary_executive)
            st.write(res.summary_bullets)
            st.text_area("Suggested Reply", res.suggested_reply, height=200)
            st.button("Approve & Send")

# ----------------- ROUTER -----------------
if not st.session_state.auth:
    show_gateway()
else:
    main_dashboard()
