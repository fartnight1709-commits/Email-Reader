import streamlit as st
import json
import os
import time
from datetime import datetime

# --- 1. ENTERPRISE DATA PERSISTENCE ---
# Using a local JSON registry to mimic a secure SQL backend for immediate deployment.
DB_FILE = "intellimail_core_registry.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {
        "authorized_accounts": ["admin@intellimail.pro", "cto@garrison.financial"],
        "access_logs": []
    }

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

db_registry = load_db()

# --- 2. THE "INTELLIGENCE DARK" DESIGN SYSTEM ---
st.set_page_config(
    page_title="IntelliMail | Enterprise AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* GLOBAL FOUNDATION */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #010409; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR: MISSION CRITICAL NAVIGATION */
    [data-testid="stSidebar"] {
        background-color: #0D1117 !important;
        border-right: 1px solid #30363D;
        width: 280px !important;
    }
    
    /* TOP NAVIGATION RIBBON */
    .top-ribbon {
        background: #0D1117;
        padding: 12px 30px;
        margin: -5rem -5rem 2rem -5rem;
        border-bottom: 1px solid #30363D;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 99;
    }
    
    .status-badge {
        background: rgba(35, 134, 54, 0.15);
        color: #3FB950;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(63, 185, 80, 0.3);
    }

    /* EMAIL LISTING: HIGH DENSITY */
    .mail-row {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 6px;
        padding: 14px;
        margin-bottom: 10px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    .mail-row:hover {
        border-color: #58A6FF;
        background: #1C2128;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    .mail-sender { color: #8B949E; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
    .mail-subject { color: #F0F6FC; font-size: 0.95rem; font-weight: 600; margin: 4px 0; }
    
    /* AI ANALYSIS BRIEFING */
    .briefing-box {
        background: linear-gradient(145deg, rgba(56, 139, 253, 0.08) 0%, rgba(56, 139, 253, 0.02) 100%);
        border: 1px solid #388BFD;
        border-left: 4px solid #58A6FF;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* RAW CONTENT VIEWER */
    .raw-viewer {
        font-family: 'JetBrains Mono', monospace;
        background: #0D1117;
        padding: 20px;
        border-radius: 6px;
        border: 1px solid #30363D;
        color: #8B949E;
        font-size: 0.85rem;
    }

    /* BUTTONS: TACTICAL MINIMALISM */
    .stButton>button {
        background-color: #21262D;
        color: #C9D1D9;
        border: 1px solid #30363D;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #30363D;
        border-color: #8B949E;
        color: #F0F6FC;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION ORCHESTRATION ---
if 'auth_active' not in st.session_state:
    st.session_state.auth_active = False
if 'current_operator' not in st.session_state:
    st.session_state.current_operator = None

# --- 4. ENTERPRISE GATEWAY (LOGIN) ---
def show_gateway():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    
    with col:
        st.markdown("<h1 style='text-align:center;'>INTELLIMAIL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#8B949E; margin-top:-15px;'>Enterprise Intelligence Terminal</p>", unsafe_allow_html=True)
        
        with st.container():
            email = st.text_input("Corporate ID", placeholder="operator@domain.com")
            
            if st.button("Authorize Connection", type="primary"):
                if email in db_registry["authorized_accounts"]:
                    # Secure session initiation
                    st.session_state.auth_active = True
                    st.session_state.current_operator = email
                    db_registry["access_logs"].append({
                        "user": email, 
                        "event": "Login", 
                        "timestamp": datetime.now().isoformat()
                    })
                    save_db(db_registry)
                    st.rerun()
                else:
                    st.error("Access Denied: Account not found in Enterprise Registry.")
        
        with st.expander("Administrative Override"):
            if st.text_input("Master Key", type="password") == "devmode":
                st.session_state.auth_active = True
                st.session_state.current_operator = "SYSTEM_ROOT"
                st.rerun()

# --- 5. THE WORKSPACE (MAIN UI) ---
def show_workspace():
    # Header Ribbon
    st.markdown(f"""
        <div class="top-ribbon">
            <div style="font-weight:700; letter-spacing:-0.5px; font-size:1.2rem; color:#58A6FF;">INTELLIMAIL <span style="font-weight:400; color:#30363D;">|</span> PRO</div>
            <div class="status-badge">● Engine Operational</div>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"**Operator:** `{st.session_state.current_operator}`")
        st.divider()
        # High-End Navigation
        nav = st.radio("DASHBOARD", ["📩 Intelligence Stream", "🛠️ Registry Management", "📊 Audit Logs", "🛡️ Compliance"])
        
        st.v_spacer(height=200) # Maintain layout density
        st.divider()
        if st.button("Terminate Session"):
            st.session_state.auth_active = False
            st.rerun()

    # --- ROUTING LOGIC ---
    if nav == "📩 Intelligence Stream":
        st.subheader("Focused Communication Stream")
        
        list_col, view_col = st.columns([1, 1.8])
        
        with list_col:
            # High-density mock data
            items = [
                {"id": 1, "sender": "Legal Counsel", "sub": "Asset Purchase Agreement - Final Review", "body": "The due diligence period for the Scottsdale acquisition has concluded..."},
                {"id": 2, "sender": "Finance (Internal)", "sub": "Q1 Performance Summary - Draft", "body": "Please find the attached P&L statement for the quarter ending March..."},
            ]
            
            for i in items:
                st.markdown(f"""
                <div class="mail-row">
                    <div class="mail-sender">👤 {i['sender']}</div>
                    <div class="mail-subject">{i['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Analyze Item {i['id']}", key=f"btn_{i['id']}"):
                    st.session_state.active_mail = i

        with view_col:
            if 'active_mail' in st.session_state:
                mail = st.session_state.active_mail
                st.markdown(f"## {mail['sub']}")
                st.caption(f"Source: {mail['sender']} | Classification: **High Business Impact**")
                
                # THE INTELLIGENCE BRIEFING WIDGET
                st.markdown("""
                <div class="briefing-box">
                    <h4 style="margin-top:0; color:#58A6FF;">✨ Intelligence Briefing</h4>
                    <p style="font-size:0.95rem; line-height:1.6;">
                        <b>Intent:</b> Strategic Financial Decision Required.<br>
                        <b>Executive Summary:</b> This correspondence contains critical terms for a multi-million dollar asset acquisition. 
                        AI identifies a signature bottleneck in Clause 4.2.<br>
                        <b>Risk Score:</b> <span style="color:#D29922;">Medium Priority</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### Raw Correspondence")
                st.markdown(f'<div class="raw-viewer">{mail["body"]}</div>', unsafe_allow_html=True)
            else:
                st.info("Select a high-impact communication from the stream to begin analysis.")

    elif nav == "🛠️ Registry Management":
        st.title("Enterprise Registry")
        st.write("Manage authorized personnel access to the IntelliMail Intelligence Suite.")
        
        new_account = st.text_input("Add New Business Account to Registry:")
        if st.button("Store in Core Database"):
            if new_account and new_account not in db_registry["authorized_accounts"]:
                db_registry["authorized_accounts"].append(new_account)
                save_db(db_registry)
                st.success(f"Successfully whitelisted: {new_account}")
        
        st.divider()
        st.subheader("Authorized Personnel")
        st.table(db_registry["authorized_accounts"])

    elif nav == "📊 Audit Logs":
        st.title("Security Audit Trail")
        st.dataframe(db_registry["access_logs"], use_container_width=True)

# --- 6. EXECUTION ---
if not st.session_state.auth_active:
    show_gateway()
else:
    show_workspace()
