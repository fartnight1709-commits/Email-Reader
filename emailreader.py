import streamlit as st
import time
import features
import engine

# --- 1. GLOBAL SETTINGS (Must be first) ---
st.set_page_config(page_title="IntelliMail Pro", page_icon="📩", layout="wide")

# --- 2. SIDEBAR (Your App's Control Center) ---
with st.sidebar:
    st.title("IntelliMail V1")
    # Displays status from your engine.py
    st.success(f"Engine: {engine.get_api_status()}") 
    
    st.divider()
    if st.button("🏠 Home", use_container_width=True):
        st.write("Welcome to your dashboard.")
    if st.button("📋 Activity Logs", use_container_width=True):
        st.info("Log Database: Online")
    
    st.divider()
    theme = st.selectbox("Appearance Mode", ["Dark", "Light"])

# --- 3. MAIN HEADER & AUTH ---
st.title("📩 IntelliMail")
st.caption("Where AI meets the workplace.")

# Google OAuth Section
st.markdown("### 🔐 Secure Connection")
st.write("Connect your account to analyze live inbox data.")
auth_link = engine.get_google_auth_url()
st.link_button("🚀 Sign in with Google!", auth_link, type="primary")

st.divider()

# --- 4. THE CORE FEATURES (Tabs keep the UI clean) ---
tab1, tab2, tab3 = st.tabs(["Manual Analyzer", "Quick Processor", "System Live-View"])

with tab1:
    st.subheader("Analyze Pasted Content")
    email_input = st.text_area("Paste email here:", height=200, key="manual_ta")
    if st.button("Analyze with AI", key="btn_manual"):
        if email_input:
            with st.spinner("Analyzing..."):
                analysis = engine.analyze_email(email_input)
                st.json(analysis)
                if analysis.get("length", 0) > 10:
                    st.success(f"Action: {analysis['suggestion']}")
        else:
            st.warning("Please paste an email first.")

with tab2:
    st.subheader("Fast Snippet Processor")
    user_snippet = st.text_input("Enter Email Content", key="snippet_ti")
    if st.button("Send Email Content!", key="btn_snippet"):
        # Calls your features.py module
        response = features.process_email(user_snippet)
        st.info(response)

with tab3:
    st.subheader("System Processing Feed")
    output_container = st.empty()
    output_container.text_area("AI Output", value="System Ready...", height=200)
    
    if st.button("Start AI Process", key="btn_live"):
        st.write("Processing live data...")
        progress_bar = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.02)
            progress_bar.progress(i)
        st.success("Process Finished!")
        st.balloons()

# --- 5. FOOTER ---
st.divider()
st.caption("© 2026 IntelliMail Corp. Read-Only Permissions Active.")
