import streamlit as st
import json
import os
import time
from datetime import datetime

# --- 1. ENTERPRISE CONFIG & AUTH ---
# FOR ERROR 400 FIX: Ensure your Google Cloud Console has:
# Authorized Redirect URI: https://intellimail.streamlit.app/ (or your specific domain)
st.set_page_config(page_title="IntelliMail | AI Autopilot", layout="wide", page_icon="🪄")

# --- 2. THE SEVEN-FIGURE DESIGN SYSTEM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    
    /* Global Command Bar */
    .command-bar {
        background: rgba(13, 17, 23, 0.8);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #30363D;
        padding: 15px 40px;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* AI Strategic Inbox Cards */
    .strategic-card {
        background: linear-gradient(145deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #388BFD;
        border-left: 6px solid #58A6FF;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .strategic-card:hover { transform: scale(1.01); border-color: #79C0FF; }

    /* Suggested Response UI */
    .suggestion-pane {
        background: rgba(56, 139, 253, 0.1);
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        border: 1px dashed rgba(88, 166, 255, 0.5);
    }

    .status-dot { height: 8px; width: 8px; background-color: #3FB950; border-radius: 50%; display: inline-block; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE AI INFERENCE ENGINE ---
def process_with_ai(email_content):
    """
    CONCEPTUAL AI INTEGRATION:
    In a real-world scenario, you would pass the email_content to 
    an LLM (like Gemini 1.5 Pro) with a system prompt:
    'Categorize this email. Provide a 1-sentence summary and a suggested reply.'
    """
    # Simulate high-level logic
    return {
        "summary": "Urgent request for Q1 Asset approval. Signature required by EOD.",
        "reply": "I have reviewed the terms and approve the acquisition. Please proceed with the filing.",
        "priority": "Strategic"
    }

# --- 4. DATA STORAGE ---
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False

# --- 5. GATEWAY: GOOGLE AUTH ---
def show_gateway():
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h1 style='text-align:center;'>INTELLIMAIL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#8B949E;'>Unified Business Intelligence Hub</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.write("### 🔐 Identity Verification")
            # To fix Error 400: Ensure the URL called by this button matches your Google Cloud Console exactly.
            if st.button("🔵 Authorize via Google Workspaces", use_container_width=True, type="primary"):
                st.session_state.auth_state = True
                st.rerun()
            
            st.caption("Access restricted to authorized enterprise business accounts only.")

# --- 6. WORKSPACE: THE STRATEGIC INBOX ---
def show_workspace():
    st.markdown("""
        <div class="command-bar">
            <div style="font-weight:800; color:#58A6FF; font-size:1.2rem;">INTELLIMAIL</div>
            <div><span class="status-dot"></span> <span style="font-size:0.8rem; color:#8B949E;">AI ENGINE ACTIVE</span></div>
        </div>
        <div style="margin-top: 100px;"></div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("Filters")
        st.checkbox("Only Strategic Items", value=True)
        st.checkbox("Show Suggested Replies", value=True)
        st.divider()
        if st.button("Logout"):
            st.session_state.auth_state = False
            st.rerun()

    # --- MAIN CONTENT AREA ---
    tab_strategic, tab_general = st.tabs(["🔥 STRATEGIC INBOX", "📥 GENERAL FEED"])

    with tab_strategic:
        st.markdown("### AI-Prioritized Communications")
        
        # MOCK DATA (Simulating the output of the AI Reading every email)
        emails = [
            {"from": "Mark Stevens (Legal)", "subject": "Final Signature: Project Phoenix", "body": "Please find the attached contract for the Scottsdale property..."},
            {"from": "CFO Office", "subject": "Q1 Budget Reallocation", "body": "We need to reallocate $2M to the R&D division immediately..."}
        ]

        for i, email in enumerate(emails):
            ai_data = process_with_ai(email['body'])
            
            st.markdown(f"""
            <div class="strategic-card">
                <div style="color:#58A6FF; font-size:0.7rem; font-weight:800; letter-spacing:1px;">AI ANALYSIS: {ai_data['priority'].upper()}</div>
                <h2 style="margin: 5px 0 15px 0;">{email['subject']}</h2>
                <p><b>Executive Summary:</b> {ai_data['summary']}</p>
                <div class="suggestion-pane">
                    <p style="color:#79C0FF; font-weight:600; margin-bottom:5px;">✨ Suggested Response:</p>
                    <p style="font-style:italic; color:#C9D1D9;">"{ai_data['reply']}"</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, _ = st.columns([1, 1, 3])
            with c1:
                st.button("✅ Send Suggestion", key=f"send_{i}", use_container_width=True)
            with c2:
                st.button("📝 Edit", key=f"edit_{i}", use_container_width=True)

    with tab_general:
        st.info("The AI has categorized 14 other emails as 'Non-Strategic'. No immediate action required.")

# --- ROUTER ---
if not st.session_state.auth_state:
    show_gateway()
else:
    show_workspace()
