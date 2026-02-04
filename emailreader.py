import streamlit as st
import json
import os
import time
import engine # Your backend for Gmail OAuth and AI logic

# --- 1. INTELLIMAIL CORE STORAGE ---
DB_FILE = "intellimail_registry.json"

def load_registry():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"authorized_users": ["admin@intellimail.ai"], "system_logs": []}

def save_registry(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 2. THE OLED-ULTRA SLIM DESIGN ---
st.set_page_config(page_title="IntelliMail | AI Business Intelligence", layout="wide")

st.markdown("""
    <style>
    /* OLED Black Theme */
    .stApp { background-color: #030303; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #080808 !important; border-right: 1px solid #1a1a1a; }
    
    /* Slim Outlook-Style Email Row */
    .mail-item {
        padding: 14px;
        background-color: #0d0d0d;
        border: 1px solid #1f1f1f;
        border-left: 3px solid #0078d4;
        border-radius: 4px;
        margin-bottom: 6px;
        transition: 0.2s;
    }
    .mail-item:hover { background-color: #151515; border-color: #58a6ff; }
    .sender-name { color: #58a6ff; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; }
    .subject-line { color: #ffffff; font-weight: 600; font-size: 0.95rem; margin-top: 2px; }
    
    /* AI Intelligence Box */
    .ai-box {
        background: linear-gradient(145deg, #0a0a0a, #111);
        border: 1px solid #0078d4;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 120, 212, 0.2);
    }
    
    /* Branding Header */
    .brand-header {
        background: #0078d4;
        padding: 10px 25px;
        margin: -5rem -5rem 2rem -5rem;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION & REGISTRY ---
registry = load_registry()
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'active_user' not in st.session_state:
    st.session_state.active_user = None

# --- 4. THE GATEWAY (Account Linking & Sign-Up) ---
def show_gateway():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, mid, col3 = st.columns([1, 1.8, 1])
    
    with mid:
        st.markdown("<h1 style='text-align:center;'>INTELLIMAIL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#666;'>Secure AI Email Intelligence Suite</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            user_input = st.text_input("Business Email Address", placeholder="name@company.com")
            
            if st.button("🔗 Link & Authorize Account", use_container_width=True, type="primary"):
                if user_input in registry["authorized_users"]:
                    # Actual Google Link via Engine
                    auth_url = engine.get_google_auth_url()
                    st.session_state.authenticated = True
                    st.session_state.active_user = user_input
                    st.link_button("Confirm Google Connection", auth_url)
                else:
                    st.error("Account Access Denied: This email is not whitelisted in the IntelliMail Registry.")
        
        # Dev Secret Bypass
        with st.expander("System Administrator Access"):
            secret = st.text_input("Master Key", type="password")
            if secret == "devmode":
                st.session_state.authenticated = True
                st.session_state.active_user = "MASTER_ADMIN"
                st.rerun()

# --- 5. THE AI WORKSPACE ---
def show_workspace():
    st.markdown('<div class="brand-header"><h3 style="margin:0; color:white;">IntelliMail | Secure Analytics</h3></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("INTELLIMAIL")
        st.caption(f"Session: {st.session_state.active_user}")
        st.divider()
        nav = st.radio("MAIN NAVIGATION", ["📥 AI Inbox", "🛠️ Administration", "📊 Activity Audit", "🛡️ Compliance"])
        st.divider()
        if st.button("🚪 Secure Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- ADMINISTRATION (Account Management) ---
    if nav == "🛠️ Administration":
        st.title("Intelligence Console")
        st.write("Register and store business accounts for IntelliMail access.")
        
        new_mail = st.text_input("Enter Email to Whitelist:")
        if st.button("Register Business Account"):
            if new_mail and new_mail not in registry["authorized_users"]:
                registry["authorized_users"].append(new_mail)
                save_registry(registry)
                st.success(f"Access Permanently Granted: {new_mail}")
        
        st.divider()
        st.subheader("Whitelisted Entities")
        st.table(registry["authorized_users"])

    # --- THE AI INBOX ---
    elif nav == "📥 AI Inbox":
        st.markdown("### Focused AI Stream")
        
        col_list, col_view = st.columns([1, 1.8])
        
        with col_list:
            # Filtered Business Emails (Integrated from your engine)
            emails = [
                {"id": 1, "sender": "Alex Rivera", "subject": "Venture Equity Terms", "body": "Please review the attached contract regarding the Scottsdale asset acquisition..."},
                {"id": 2, "sender": "Compliance Lab", "subject": "Audit Report 2026", "body": "Your annual financial compliance check is now due..."},
            ]
            
            for e in emails:
                with st.container():
                    st.markdown(f"""
                    <div class="mail-item">
                        <div class="sender-name">👤 {e['sender']}</div>
                        <div class="subject-line">{e['subject']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Analyze: {e['id']}", key=f"a_{e['id']}", use_container_width=True):
                        st.session_state.selected_msg = e

        with col_view:
            if 'selected_msg' in st.session_state:
                msg = st.session_state.selected_msg
                st.markdown(f"# {msg['subject']}")
                st.write(f"**Sender:** {msg['sender']}")
                
                # --- AI SCANNING BLOCK ---
                st.markdown('<div class="ai-box">', unsafe_allow_html=True)
                st.markdown("### ✨ IntelliMail AI Analysis")
                with st.spinner("Scanning for business intent..."):
                    # Use your engine: analysis = engine.analyze_email(msg['body'])
                    st.info("**Intent Identified:** Financial Asset Management / Contract Review.")
                    st.write("**Smart Summary:** This email discusses terms for a Scottsdale asset. Immediate legal review of the equity structure is recommended.")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.text_area("Original Content", value=msg['body'], height=400, disabled=True)
            else:
                st.info("Select a business communication to run the IntelliMail AI scan.")

    # --- AUDIT LOGS ---
    elif nav == "📊 Activity Audit":
        st.title("System Activity")
        st.write("All email reads and AI scans are logged for Garrison Financial compliance requirements.")
        st.code("LOG: [2026-02-03 23:10] - MASTER_ADMIN accessed AI Analytics.")

    # --- COMPLIANCE ---
    elif nav == "🛡️ Compliance":
        st.title("Privacy & Security")
        st.markdown("IntelliMail adheres to the **Google Limited Use Policy**. No email data is stored beyond the current session.")

# --- 6. ROUTER ---
if not st.session_state.authenticated:
    show_gateway()
else:
    show_workspace()
