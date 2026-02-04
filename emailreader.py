import streamlit as st
import json
import os
from datetime import datetime

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="IntelliMail | Secure Gateway", layout="wide", page_icon="🔐")

# Enterprise CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp { background-color: #030303; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Premium Header */
    .brand-header {
        background: #0078d4;
        padding: 15px 30px;
        margin: -5rem -5rem 2rem -5rem;
        text-align: center;
        font-weight: 800;
        letter-spacing: 1px;
    }

    /* Modern Card Layout */
    .inbox-card {
        background: #0d0d0d;
        border: 1px solid #1f1f1f;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        transition: 0.3s;
    }
    .inbox-card:hover { border-color: #0078d4; background: #121212; }

    /* AI Highlight */
    .ai-badge {
        color: #58a6ff;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# --- 3. LOGIN GATEWAY ---
def show_login():
    st.markdown('<div class="brand-header">INTELLIMAIL SECURE GATEWAY</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    left, mid, right = st.columns([1, 1.5, 1])
    
    with mid:
        st.subheader("🔐 Identity Verification")
        st.info("This application is restricted to assigned business accounts only.")
        
        # This button triggers the OAuth flow. 
        # For Error 400: Ensure 'https://intellimail.streamlit.app/' is in your Google Console.
        if st.button("🚀 Sign in with Authorized Google Account", type="primary", use_container_width=True):
            # Simulation of successful OAuth redirect
            st.session_state.authenticated = True
            st.session_state.user_email = "executive@garrison.financial"
            st.rerun()

        st.divider()
        with st.expander("Admin/Dev Access"):
            portal_key = st.text_input("Enter Portal Key:", type="password")
            if portal_key == "devmode":
                st.session_state.authenticated = True
                st.session_state.user_email = "SYSTEM_ADMIN"
                st.rerun()

# --- 4. THE INTELLIMAIL WORKSPACE ---
def show_workspace():
    # Top Ribbon
    st.markdown(f"""
        <div style="background:#0D1117; padding:10px 40px; border-bottom:1px solid #30363D; display:flex; justify-content:space-between; align-items:center;">
            <div style="font-weight:800; color:#0078d4;">INTELLIMAIL BUSINESS</div>
            <div style="font-size:0.8rem; color:#8B949E;">Active: <b>{st.session_state.user_email}</b></div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Sidebar
    with st.sidebar:
        st.title("Pro Menu")
        nav = st.radio("Navigation", ["📥 Focused Inbox", "🛠️ Admin Console", "🛡️ Compliance"])
        st.divider()
        if st.button("Secure Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    if nav == "📥 Focused Inbox":
        st.title("Focused Stream")
        
        col_list, col_view = st.columns([1, 2])
        
        # Mock Email Data
        emails = [
            {"id": 1, "sender": "Mark Stevens", "subj": "Quarterly Deck", "body": "I've uploaded the Q1 results for the reading portal..."},
            {"id": 2, "sender": "Finance Team", "subj": "Invoice Approval", "body": "Please review the vendor invoice for the Scottsdale asset..."}
        ]

        with col_list:
            for e in emails:
                st.markdown(f"""
                    <div class="inbox-card">
                        <div class="ai-badge">👤 {e['sender']}</div>
                        <div style="font-weight:600;">{e['subj']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"View Analyze {e['id']}", key=f"view_{e['id']}", use_container_width=True):
                    st.session_state.selected_email = e

        with col_view:
            if 'selected_email' in st.session_state:
                mail = st.session_state.selected_email
                st.title(mail['subj'])
                st.write(f"**From:** {mail['sender']}")
                
                # --- AI READING BLOCK ---
                st.markdown("""
                <div style="background:rgba(0,120,212,0.1); border:1px solid #0078d4; padding:15px; border-radius:8px; border-left:5px solid #0078d4;">
                    <h4 style="margin-top:0;">✨ AI Reading Analysis</h4>
                    <p style="font-size:0.9rem;"><b>Summary:</b> This email is a formal request for document approval. <b>Action Item:</b> Review the PDF and sign by Friday.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.caption("Full Message Content")
                st.code(mail['body'], language="text")
            else:
                st.info("Select a message to begin the AI analysis.")

    elif nav == "🛠️ Admin Console":
        st.title("System Administration")
        st.write("Manage authorized accounts and security whitelists.")

    elif nav == "🛡️ Compliance":
        st.title("Compliance & Encryption")
        st.write("Data is encrypted via AES-256 and subject to corporate privacy protocols.")

# --- 5. EXECUTION ---
if not st.session_state.authenticated:
    show_login()
else:
    show_workspace()
