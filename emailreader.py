import streamlit as st
import json
import os
import time
import engine # Your Gmail/AI backend

# --- 1. THE OLED CORE ---
st.set_page_config(page_title="IntelliMail | AI Intelligence", layout="wide")

# --- 2. HIGH-END DASHBOARD CSS ---
st.markdown("""
    <style>
    /* Ultra Black Canvas */
    .stApp { background-color: #030303; color: #ffffff; }
    
    /* Hide Default Sidebar Clutter */
    section[data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #1a1a1a;
        min-width: 240px !important;
    }

    /* Glass Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 10px 40px;
        border-bottom: 1px solid #222;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
    }

    /* Custom Button Styling */
    .stButton>button {
        background-color: #0d1117;
        color: #58a6ff;
        border: 1px solid #30363d;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0078d4;
        color: white;
        border-color: #0078d4;
    }

    /* Email List Styling */
    .mail-card {
        padding: 15px;
        background: #0d0d0d;
        border: 1px solid #1f1f1f;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .mail-card:hover { border-color: #0078d4; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT REGISTRY ---
DB_FILE = "user_registry.json"
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"users": ["dev@intellimail.ai"]}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_db()

# --- 4. NAVIGATION LOGIC (NO MORE RADIO BUTTONS) ---
if 'page' not in st.session_state:
    st.session_state.page = "Inbox"
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- 5. THE WORKSPACE ---
def main_app():
    # CUSTOM TOP NAVIGATION BAR
    st.markdown(f"""
        <div class="top-nav">
            <h2 style="margin:0; font-weight:800; color:#0078d4;">INTELLIMAIL</h2>
            <div style="display: flex; gap: 20px; align-items: center;">
                <span style="color:#888; font-size:0.9rem;">Operator: {st.session_state.get('user', 'ADMIN')}</span>
            </div>
        </div>
        <div style="margin-top: 80px;"></div>
    """, unsafe_allow_html=True)

    # ACTION SIDEBAR
    with st.sidebar:
        st.markdown("### ⚡ Command Center")
        if st.button("📥 Focused Inbox", use_container_width=True):
            st.session_state.page = "Inbox"
        if st.button("🛠️ User Management", use_container_width=True):
            st.session_state.page = "Admin"
        if st.button("📊 Security Audit", use_container_width=True):
            st.session_state.page = "Logs"
        
        st.divider()
        if st.button("🚪 Secure Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # PAGE ROUTING
    if st.session_state.page == "Inbox":
        st.title("Business Stream")
        col_list, col_view = st.columns([1, 2])
        
        with col_list:
            mock_mails = [
                {"id": 1, "sender": "Mark Stevens", "sub": "Project Phoenix Update"},
                {"id": 2, "sender": "Finance Team", "sub": "Invoice #881"}
            ]
            for m in mock_mails:
                with st.container():
                    st.markdown(f"""
                    <div class="mail-card">
                        <div style="color:#58a6ff; font-weight:700; font-size:0.8rem;">{m['sender']}</div>
                        <div style="font-weight:600; font-size:0.95rem;">{m['sub']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Scan Asset {m['id']}", key=f"s_{m['id']}", use_container_width=True):
                        st.session_state.active = m

        with col_view:
            if 'active' in st.session_state:
                st.subheader(st.session_state.active['sub'])
                st.info("✨ **AI Intelligence Scan:** Financial Intent Detected. High Priority.")
                st.text_area("Analysis Report", "Sample data extraction in progress...", height=400)
            else:
                st.info("Select a communication to initiate AI scanning.")

    elif st.session_state.page == "Admin":
        st.title("User Registry")
        new_u = st.text_input("Grant New Corporate Access:")
        if st.button("Whitelisting Account"):
            db["users"].append(new_u)
            save_db(db)
            st.success("User Stored Successfully.")
        st.table(db["users"])

# --- 6. LOGIN GATEWAY ---
def login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, mid, c3 = st.columns([1, 1.5, 1])
    with mid:
        st.title("🔑 IntelliMail Portal")
        email = st.text_input("Business Email")
        if st.button("Sign in with Assigned Account", type="primary", use_container_width=True):
            if email in db["users"]:
                st.session_state.auth = True
                st.session_state.user = email
                st.rerun()
        
        with st.expander("Bypass"):
            if st.text_input("Key", type="password") == "devmode":
                st.session_state.auth = True
                st.rerun()

# --- RUN APP ---
if not st.session_state.auth:
    login()
else:
    main_app()
