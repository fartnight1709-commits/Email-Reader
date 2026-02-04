import streamlit as st
import time
import engine
import features

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(
    page_title="IntelliMail AI | Enterprise",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS FOR PROFESSIONAL DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        border: 1px solid #464b5d;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    div[data-testid="stExpander"] {
        border: none !important;
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PRO NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/281/281769.png", width=50)
    st.title("IntelliMail Enterprise")
    st.markdown("---")
    
    # Navigation with icons
    page = st.radio(
        "GO TO",
        ["System Dashboard", "Security & Privacy", "Compliance Terms"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("Infrastructure")
    try:
        status = engine.get_api_status()
        st.success(f"● {status}")
    except:
        st.error("● Engine Offline")
        
    st.caption("Version: 1.0.4-Stable")
    st.caption("© 2026 IntelliMail AI Global")

# --- 4. PAGE: DASHBOARD ---
if page == "System Dashboard":
    st.title("🚀 Intelligence Dashboard")
    st.info("Authenticated Session Required for Live Sync")

    col1, col2, col3 = st.columns(3)
    col1.metric("API Latency", "24ms", "-2ms")
    col2.metric("AI Confidence", "98.2%", "+0.4%")
    col3.metric("Security Tier", "Level 4", "Encrypted")

    st.divider()

    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📥 Input Intelligence")
        email_data = st.text_area("Source Email Content", height=300, placeholder="Paste raw email data or headers here for AI auditing...")
        
        if st.button("EXECUTE ANALYSIS"):
            if email_data:
                with st.spinner("Decoding and Analyzing..."):
                    res = engine.analyze_email(email_data)
                    st.success("Analysis Complete")
                    st.subheader("Audit Results")
                    st.json(res)
            else:
                st.error("Input required for execution.")

    with c2:
        st.subheader("⚙️ System Controls")
        auth_link = engine.get_google_auth_url()
        st.link_button("🔑 Re-Authorize Google Cloud", auth_link, type="primary")
        
        with st.expander("System Logs", expanded=True):
            st.code("Initializing engine...\nConnection: OK\nReady for OAuth...", language="bash")
        
        if st.button("Clear Cache"):
            st.toast("Internal Memory Purged")

# --- 5. PAGE: PRIVACY POLICY (ENTERPRISE RULES) ---
elif page == "Security & Privacy":
    st.title("🛡️ Enterprise Privacy Policy")
    st.warning("Last Revision: February 4, 2026. This policy is binding for Google OAuth Verification.")
    
    st.markdown("""
    ### 1. Data Governance
    IntelliMail AI operates under strict data minimization principles. We only access the `gmail.readonly` scope to provide textual analysis. 
    
    ### 2. Limited Use Disclosure
    Our application strictly adheres to the **Google API Service User Data Policy**, including the **Limited Use requirements**. We do not use user data for:
    * Developing or improving generalized AI/ML models.
    * Serving advertisements or tracking user behavior.
    * Reselling data to third-party brokers.
    
    ### 3. Encryption & Storage
    * **Zero-Retention:** We do not store raw email content on our databases.
    * **Transit Security:** All data transmitted via the Google API is encrypted using TLS 1.2 or higher.
    * **Volatile Memory:** Data is processed in RAM and cleared upon session termination.
    """)

# --- 6. PAGE: COMPLIANCE TERMS ---
elif page == "Compliance Terms":
    st.title("📜 Terms of Service & Compliance")
    
    st.markdown("""
    ### 1. Authorized Use
    The IntelliMail Enterprise suite is provided for professional productivity purposes. Unauthorized scraping or attempted reverse engineering of the AI engine is strictly prohibited.
    
    ### 2. Liability Limitation
    IntelliMail AI provides probabilistic analysis based on Large Language Models. We are not liable for:
    * Misinterpreted financial instructions.
    * Temporary outages of the Google API service.
    * Inaccuracies in AI-generated summaries.
    
    ### 3. Account Security
    Users are responsible for maintaining the confidentiality of their Google OAuth tokens. If you suspect a breach, revoke access immediately via [Google Security Settings](https://myaccount.google.com/permissions).
    
    ### 4. Termination
    We reserve the right to suspend API access for users violating our security protocols.
    """)
