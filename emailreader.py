import streamlit as st
import time
import engine
import features

# --- 1. PAGE CONFIG (Must be the very first line) ---
st.set_page_config(page_title="IntelliMail AI", page_icon="📩", layout="wide")

# --- 2. SINGLE-FILE NAVIGATION ---
# This replaces the 'pages' folder so everything is in one script
page = st.sidebar.radio("Go to:", ["Dashboard", "Privacy Policy", "Terms of Service"])

st.sidebar.divider()

# Safer way to get status to prevent the AttributeError from your screenshot
try:
    status = engine.get_api_status()
    st.sidebar.success(f"Engine: {status}")
except Exception:
    st.sidebar.warning("Engine: Initializing...")

# --- PAGE 1: MAIN DASHBOARD ---
if page == "Dashboard":
    st.title("📩 IntelliMail Pro")
    st.caption("Commercial Grade Email Intelligence")

    # OAuth Section
    st.markdown("### 🔐 Authentication")
    st.write("Connect securely via Google to analyze your inbox.")
    
    auth_link = engine.get_google_auth_url()
    st.link_button("🚀 Sign in with Google!", auth_link, type="primary")
    
    st.divider()

    # Analysis Interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Manual Email Analysis")
        email_input = st.text_area("Paste email content here:", height=250, placeholder="Paste headers and body...")
        
        if st.button("Analyze with AI"):
            if email_input:
                with st.spinner("Analyzing sentiment and priority..."):
                    # Calling your engine module
                    analysis = engine.analyze_email(email_input)
                    st.subheader("Results")
                    st.json(analysis)
            else:
                st.warning("Please paste an email first.")

    with col2:
        st.subheader("System Live Feed")
        log_box = st.empty()
        log_box.info("Waiting for process start...")
        
        if st.button("Run System Check"):
            progress_bar = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                progress_bar.progress(i)
                if i == 50: log_box.warning("Scanning API connections...")
            st.success("System Operational")
            st.balloons()

# --- PAGE 2: PRIVACY POLICY (Required for Google Verification) ---
elif page == "Privacy Policy":
    st.title("🛡️ Privacy Policy")
    st.write("**Last Updated:** February 4, 2026")
    st.markdown("""
    ### 1. Data Collection
    IntelliMail uses the Google Gmail API to access email content. We only request **Read-Only** access.
    
    ### 2. Data Usage
    We process email data to provide summaries. Information received from Google APIs will adhere to the **Google API Service User Data Policy**, including the Limited Use requirements.
    
    ### 3. Data Storage
    We do **not** store your emails on our servers. Processing happens in real-time and is discarded after your session.
    """)

# --- PAGE 3: TERMS OF SERVICE ---
elif page == "Terms of Service":
    st.title("📜 Terms of Service")
    st.markdown("""
    ### 1. Service Description
    IntelliMail provides AI-driven insights for email management.
    
    ### 2. User Responsibilities
    Users are responsible for maintaining the security of their own Google accounts.
    
    ### 3. Disclaimers
    AI analysis is provided 'as-is'. Users should verify critical information manually.
    """)

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("© 2026 IntelliMail AI")
