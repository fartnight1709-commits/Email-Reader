import streamlit as st
from IntelliMail import IntelliMailEngine
import os

# Premium Executive Configuration
st.set_page_config(page_title="IntelliMail Pro", layout="wide", page_icon="📩")

# High-Net-Worth Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #1E293B; border-right: 1px solid #334155; }
    .email-card { 
        background: #1E293B; padding: 20px; border-radius: 12px; 
        border-left: 5px solid #38BDF8; margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .email-card:hover { transform: translateY(-2px); background: #26334d; }
    </style>
""", unsafe_allow_html=True)

engine = IntelliMailEngine()

# --- STEP 1: Handle the Google Auth Callback ---
# This "catches" the code Google sends back to your URL
query_params = st.query_params
if "code" in query_params and 'credentials' not in st.session_state:
    try:
        from google_auth_oauthlib.flow import Flow
        client_config = {
            "web": {
                "client_id": st.secrets["GOOGLE_CLIENT_ID"],
                "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
                "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        flow = Flow.from_client_config(
            client_config,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri="https://intellimail.streamlit.app/"
        )
        flow.fetch_token(code=query_params["code"])
        st.session_state.credentials = flow.credentials
        st.query_params.clear() # Clean the URL
        st.rerun()
    except Exception as e:
        st.error(f"Authentication Failed: {e}")

# --- STEP 2: UI Logic ---
if 'credentials' not in st.session_state:
    # AUTHENTICATION GATEWAY
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>INTELLIMAIL<span style='color:#38BDF8'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8;'>Enterprise Intelligence for Garrison Financial</p>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1, 1])
    with col:
        auth_url = engine.get_google_auth_url()
        st.link_button("🔐 Sign in with Google", auth_url, type="primary", use_container_width=True)
else:
    # MAIN INTELLIGENCE DASHBOARD
    with st.sidebar:
        st.title("Garrison Financial")
        st.status("Intelligence Cluster: Alpha-1")
        if st.button("Secure Logout"):
            del st.session_state.credentials
            st.rerun()

    st.title("Intelligence Stream")
    
    with st.spinner("Accessing Secure Inbox..."):
        emails = engine.fetch_live_emails(st.session_state.credentials)

    col_list, col_view = st.columns([1, 1])

    with col_list:
        for e in emails:
            with st.container():
                st.markdown(f"""
                    <div class='email-card'>
                        <small style='color:#38BDF8'>SENDER: {e['sender']}</small>
                        <h4 style='margin: 5px 0;'>{e['subject']}</h4>
                        <p style='font-size: 14px; color: #94A3B8;'>{e['body'][:100]}...</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Analyze Intelligence", key=e['id']):
                    st.session_state.active_email = e

    with col_view:
        if 'active_email' in st.session_state:
            e = st.session_state.active_email
            st.subheader("AI Executive Analysis")
            with st.spinner("Analyzing with Gemini 1.5 Pro..."):
                analysis = engine.analyze_email(e['body'], e['sender'])
                
                st.metric("Priority Level", analysis.priority)
                st.write(f"**Intent Detected:** {analysis.intent_detected}")
                
                with st.expander("View CEO Draft Reply", expanded=True):
                    st.text_area("Draft", analysis.suggested_reply, height=250)
                    st.button("Approve & Send (Mock)")
        else:
            st.info("Select a high-signal communication from the stream to begin analysis.")
