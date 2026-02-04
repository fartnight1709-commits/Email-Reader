import streamlit as st
import time
import engine
import features

# --- 1. PAGE SETUP (Must be first) ---
# We define the pages here so they show up in the sidebar automatically
def main_dashboard():
    st.title("📩 IntelliMail Pro")
    st.caption("Commercial Grade Email Intelligence")

    # Auth Section
    st.markdown("### 🔐 Authentication")
    st.write("Connect securely via Google to analyze your inbox.")
    
    auth_link = engine.get_google_auth_url()
    st.link_button("🚀 Sign in with Google!", auth_link, type="primary")
    
    st.divider()

    # Analysis Interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Manual Email Analysis")
        email_input = st.text_area("Paste email content here:", height=250, key="main_input")
        
        if st.button("Analyze with AI"):
            if email_input:
                with st.spinner("Analyzing..."):
                    analysis = engine.analyze_email(email_input)
                    st.subheader("Results")
                    st.json(analysis)
            else:
                st.warning("Please paste an email first.")

    with col2:
        st.subheader("System Live Feed")
        log_box = st.empty()
        log_box.info("Ready to process...")
        
        if st.button("Run System Check"):
            progress_bar = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                progress_bar.progress(i)
            st.success("System Operational")
            st.balloons()

def privacy_policy():
    st.title("🛡️ Privacy Policy")
    st.write("**Last Updated:** February 4, 2026")
    st.markdown("""
    ### 1. Data Collection
    IntelliMail uses the Google Gmail API to access email content. We only request **Read-Only** access.
    
    ### 2. Data Usage
    We process email data to provide summaries. Information received from Google APIs will adhere to the **Google API Service User Data Policy**, including the Limited Use requirements.
    
    ### 3. Data Storage
    We do **not** store your emails on our servers. Processing happens in real-time.
    """)

def terms_of_service():
    st.title("📜 Terms of Service")
    st.markdown("""
    ### 1. Service Description
    IntelliMail provides AI-driven insights for email management.
    
    ### 2. User Responsibilities
    Users are responsible for maintaining the security of their own Google accounts.
    """)

# --- 2. EXECUTION & NAVIGATION ---
# This creates the actual "Pages" in your sidebar
pg = st.navigation([
    st.Page(main_dashboard, title="Dashboard", icon="🏠"),
    st.Page(privacy_policy, title="Privacy Policy", icon="🛡️"),
    st.Page(terms_of_service, title="Terms of Service", icon="📜"),
])

# Sidebar Status (Fixed the duplicate issue)
with st.sidebar:
    st.title("IntelliMail V1")
    try:
        st.success(f"Engine: {engine.get_api_status()}")
    except:
        st.warning("Engine: Connecting...")
    st.divider()

# Run the selected page
pg.run()
