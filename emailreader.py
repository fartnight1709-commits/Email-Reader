import streamlit as st
import os
import time
from engine import IntelliMailEngine

# --- 1. SESSION STATE SAFETY (Fixes KeyErrors) ---
if 'auth_active' not in st.session_state:
    st.session_state.auth_active = False
if 'user_list' not in st.session_state:
    st.session_state.user_list = []
if 'logged_in_history' not in st.session_state:
    st.session_state.logged_in_history = []
if 'users' not in st.session_state:
    st.session_state.users = {}

# --- 2. LAYOUT HELPER (Fixes v_spacer error) ---
def v_spacer(height):
    for _ in range(height // 20):
        st.write("")

# --- 3. THE WORKSPACE ---
def show_workspace():
    st.title("📩 Intelligence Stream")
    
    # Corrected Sidebar
    with st.sidebar:
        st.header("DASHBOARD")
        nav = st.radio("Navigation", ["Intelligence Stream", "Regulatory Settings"])
        
        v_spacer(100) # Manual spacer instead of st.v_spacer
        st.divider()
        if st.button("Terminate Session"):
            st.session_state.auth_active = False
            st.rerun()

    # Main Area Logic
    col_list, col_view = st.columns([1, 2])
    
    business_emails = [
        {"sender": "John Doe", "subject": "Quarterly Review", "body": "Please find the review attached..."},
        {"sender": "Sarah Miller", "subject": "Onboarding", "body": "Welcome to the team!"}
    ]

    with col_list:
        for i, mail in enumerate(business_emails):
            with st.container(border=True):
                st.markdown(f"**{mail['sender']}**")
                st.caption(mail['subject'])
                # Removed 'label_visibility' to fix TypeError
                if st.button(f"Analyze", key=f"btn_{i}"):
                    st.session_state.current_mail = mail

def show_gateway():
    st.title("🔐 IntelliMail Gateway")
    if st.button("Sign in with Garrison Financial SSO", type="primary"):
        st.session_state.auth_active = True
        st.rerun()

# --- 4. ROUTER ---
if not st.session_state.auth_active:
    show_gateway()
else:
    show_workspace()
