import streamlit as st
import json
import os
import time
from datetime import datetime

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(page_title="IntelliMail | AI Autopilot", layout="wide", page_icon="🪄")

# --- 2. THE $1M DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #020408; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    
    /* Global Command Ribbon */
    .command-ribbon {
        background: rgba(13, 17, 23, 0.9);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #30363D;
        padding: 12px 40px;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Strategic Card Design */
    .strategic-card {
        background: linear-gradient(145deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #388BFD;
        border-left: 6px solid #58A6FF;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    /* AI Draft Component */
    .ai-draft-container {
        background: rgba(35, 134, 54, 0.05);
        border: 1px dashed #238636;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
    }

    .status-active { color: #3FB950; font-size: 0.75rem; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE AI LOGIC ENGINE ---
def simulate_ai_analysis(email_body):
    """
    In Production: This function sends 'email_body' to the Gemini API.
    It returns a structured JSON for routing.
    """
    # High-value simulation logic
    is_strategic = "contract" in email_body.lower() or "approve" in email_body.lower() or "budget" in email_body.lower()
    
    return {
        "strategic": is_strategic,
        "summary": "Urgent: Signature required for Project Phoenix budget reallocation.",
        "reply": "I have reviewed the reallocation request. This aligns with our Q1 strategy. Please proceed.",
        "confidence": 0.98
    }

# --- 4. SESSION STATE & ROUTING ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 5. THE GATEWAY (GOOGLE SIGN-IN) ---
def show_gateway():
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center;'>INTELLIMAIL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#8B949E;'>AI-Driven Communication Intelligence</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.write("### Enterprise Access")
            # To fix ERROR 400: Ensure the redirect URI in Google Console is exactly your app's URL.
            if st.button("🔵 Sign in with Google Workspaces", use_container_width=True, type="primary"):
                st.session_state.authenticated = True
                st.rerun()
            
            st.caption("Identity management handled via Google OAuth 2.0 Secure Protocols.")

# --- 6. THE AI WORKSPACE ---
def show_workspace():
    # Top Branding Ribbon
    st.markdown(f"""
        <div class="command-ribbon">
            <div style="font-weight:800; color:#58A6FF; font-size:1.2rem;">INTELLIMAIL <span style="font-weight:200; color:#30363D;">|</span> AI</div>
            <div class="status-active">● AGENT SCANNING ACTIVE</div>
        </div>
        <div style="margin-top: 100px;"></div>
    """, unsafe_allow_html=True)

    # Action Sidebar
    with st.sidebar:
        st.markdown("### Control Center")
        st.toggle("Auto-Drafting", value=True)
        st.toggle("Priority Notifications", value=True)
        st.divider()
        if st.button("Terminate Session"):
            st.session_state.authenticated = False
            st.rerun()

    # Strategic Inbox Logic
    tab_strat, tab_gen = st.tabs(["🔥 STRATEGIC VAULT", "📥 GENERAL FEED"])

    # Sample Emails to be read by AI
    incoming_mails = [
        {"from": "Legal Dept", "subj": "Contract: Phoenix Asset", "body": "Please approve the budget for the Phoenix property contract..."},
        {"from": "Marketing", "subj": "Weekly Newsletter", "body": "Here is the update on our social media performance..."},
    ]

    with tab_strat:
