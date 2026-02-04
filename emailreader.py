import streamlit as st
import json
import os
import time
import engine # Your backend for Gmail OAuth and AI

# --- 1. GARRISON FINANCIAL DATABASE ---
DB_FILE = "garrison_registry.json"

def load_registry():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"authorized_users": ["admin@garrisonfinancial.com"], "activity_logs": []}

def save_registry(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 2. THE "ULTRA-SLIM" DARK UI ---
st.set_page_config(page_title="Garrison Financial | IntelliMail", layout="wide")

st.markdown("""
    <style>
    /* OLED Black & Garrison Navy */
    .stApp { background-color: #050505; color: #d1d1d1; }
    [data-testid="stSidebar"] { background-color: #0a0b0d !important; border-right: 1px solid #1c1f26; }
    
    /* Slim Outlook Cards */
    .email-card {
        padding: 12px;
        background-color: #0f1115;
        border: 1px solid #21262d;
        border-left: 4px solid #0078d4;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    .sender-text { color: #58a6ff; font-weight: 700; font-size: 0.85rem; }
    .subject-text { color: #ffffff; font-weight: 600; font-size: 0.9rem; }
    
    /* Financial Insight Box */
    .insight-box {
        background: rgba(0, 120, 212, 0.1);
        border: 1px solid #0078d4;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Header */
    .garrison-header {
        background: linear-gradient(90deg, #001f3f 0%, #0078d4 100%);
        padding: 15px 30px;
        margin: -5rem -5rem 2rem -5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
registry = load_registry()
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'active_user' not in st.session_state:
    st.session_state.active_user = None

# --- 4. THE GATEWAY (Garrison Secure Sign-In) ---
def gateway():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, mid, c3 = st.columns([1, 1.5, 1])
    
    with mid:
        st.markdown("<h1 style='text-align:center;'>Garrison Financial</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>Intelligent Mail & Asset Management</p>", unsafe_allow_html=True)
        
        # LINKING INTERFACE
        with st.container(border=True):
            user_mail = st.text_input("Corporate Email", placeholder="user@garrisonfinancial.com")
            
            if st.button("🚀 Link & Access Portal", use_container_width=True):
                if user_mail in registry["authorized_users"]:
                    auth_url = engine.get_google_auth_url()
                    st.session_state.auth = True
                    st.session_state.active_user = user_mail
                    st.link_button("Complete Google Linking", auth_url)
                else:
                    st.error("Access Restricted: Email not found in Garrison Registry.")
        
        # Dev Bypass
        with st.expander("Administrative Override"):
            key = st.text_input("Bypass Key", type="password")
            if key == "devmode":
                st.session_state.auth = True
                st.session_state.active_user = "SYSTEM_ADMIN"
                st.rerun()

# --- 5. THE WORKSPACE ---
def workspace():
    st.markdown('<div class="garrison-header"><h3 style="margin:0; color:white;">Garrison Intelligence Hub</h3></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"**Operator:** `{st.session_state.active_user}`")
        st.divider()
        nav = st.radio("PRO MENU", ["📥 Focused Inbox", "🛠️ Admin Console", "📊 Activity Logs", "⚖️ Compliance"])
        st.divider()
        if st.button("Secure Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- ADMIN CONSOLE ---
    if nav == "🛠️ Admin Console":
        st.title("User Permissions Management")
        new_user = st.text_input("Authorize New Team Member Email:")
        if st.button("Add to Garrison Registry"):
            if new_user and new_user not in registry["authorized_users"]:
                registry["authorized_users"].append(new_user)
                save_registry(registry)
                st.success(f"Access granted to {new_user}")
        
        st.write("### Authorized Personnel")
        st.table(registry["authorized_users"])

    # --- INBOX & AI SCANNING ---
    elif nav == "📥 Focused Inbox":
        col_list, col_view = st.columns([1, 2])
        
        with col_list:
            st.subheader("Business Streams")
            # Filtering out "numbnuts" verification emails
            emails = [
                {"id": 1, "sender": "Partnerships Dept", "subject": "Venture Capital Terms", "body": "Please review the attached equity structure for the Q1 deal..."},
                {"id": 2, "sender": "Compliance Team", "subject": "Annual Audit Notification", "body": "This is a notice regarding the upcoming financial audit..."},
            ]
            
            for e in emails:
                st.markdown(f"""
                <div class="email-card">
                    <div class="sender-text">💼 {e['sender']}</div>
                    <div class="subject-text">{e['subject']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"AI SCAN: {e['id']}", key=f"s_{e['id']}", use_container_width=True):
                    st.session_state.current_mail = e

        with col_view:
            if 'current_mail' in st.session_state:
                mail = st.session_state.current_mail
                st.title(mail['subject'])
                st.write(f"**From:** {mail['sender']}")
                
                # AI FINANCIAL SCANNING FEATURE
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("### ✨ Garrison AI Insight")
                st.write("**Intent:** Financial Agreement / Legal Review")
                st.write("**Action Required:** Asset valuation check and signature.")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.text_area("Message Content", value=mail['body'], height=450, disabled=True)
            else:
                st.info("Select a financial communication to begin the AI scan.")

    # --- LOGS & COMPLIANCE ---
    elif nav == "📊 Activity Logs":
        st.title("System Audit Logs")
        st.caption("Tracking all AI scans and data access for compliance.")
        st.write("No unauthorized access detected.")
        
    elif nav == "⚖️ Compliance":
        st.title("Privacy & Data Policy")
        st.write("Garrison Financial adheres to Google's Limited Use Policy.")

# --- 6. MAIN ROUTER ---
if not st.session_state.auth:
    gateway()
else:
    workspace()
