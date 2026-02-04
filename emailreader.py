import streamlit as st
import json
import os
import engine # Your AI/Google Logic
from datetime import datetime

# --- 1. PERSISTENT STORAGE ENGINE ---
DB_FILE = "user_registry.json"

def load_registry():
    """Loads the whitelist and registered users from disk."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    # Default admin if no file exists
    return {"assigned_emails": ["dev@intellimail.ai"], "logged_in_history": []}

def save_registry(data):
    """Saves the whitelist to disk."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load data at start
registry = load_registry()

# --- 2. ULTRA-SLIM DARK UI ---
st.set_page_config(page_title="IntelliMail AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #1f1f1f; }
    
    /* Slim Outlook Cards */
    .email-row {
        padding: 12px;
        background-color: #0d1117;
        border: 1px solid #21262d;
        border-left: 4px solid transparent;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    .email-row:hover { border-left: 4px solid #58a6ff; background-color: #161b22; }
    .sender-label { color: #58a6ff; font-weight: 800; font-size: 0.85rem; }
    .subject-label { font-weight: 600; color: #f0f6fc; font-size: 0.95rem; }
    
    /* Top Navigation Bar */
    .outlook-bar {
        background-color: #0078d4;
        padding: 10px 25px;
        margin: -5rem -5rem 1rem -5rem;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- 4. SIGN-IN & REGISTRATION (The Gateway) ---
def show_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, col, c3 = st.columns([1, 1.8, 1])
    
    with col:
        st.markdown("<h2 style='text-align:center;'>🔐 IntelliMail Gateway</h2>", unsafe_allow_html=True)
        
        tab_login, tab_reg = st.tabs(["Sign In", "Admin Bypass"])
        
        with tab_login:
            user_email = st.text_input("Enter your Assigned Business Email", placeholder="name@company.com")
            if st.button("Link & Authorize Gmail", use_container_width=True):
                if user_email in registry["assigned_emails"]:
                    # Proceed to actual Google OAuth
                    auth_url = engine.get_google_auth_url()
                    st.session_state.authenticated = True
                    st.session_state.current_user = user_email
                    
                    # Store login event in DB
                    registry["logged_in_history"].append({
                        "email": user_email, 
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    save_registry(registry)
                    
                    st.link_button("Confirm Google Connection", auth_url)
                    st.rerun()
                else:
                    st.error("This email is not on the authorized list. Please contact your administrator.")

        with tab_reg:
            st.info("Direct Administration Access")
            master_key = st.text_input("Portal Master Key", type="password")
            if master_key == "devmode":
                st.session_state.authenticated = True
                st.session_state.current_user = "MASTER_ADMIN"
                st.rerun()

# --- 5. THE AI WORKSPACE ---
def show_workspace():
    st.markdown('<div class="outlook-bar">IntelliMail Business | Workplace</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"**Active:** `{st.session_state.current_user}`")
        st.divider()
        nav = st.radio("Navigate", ["📩 Inbox", "🛠️ Admin Console", "🛡️ Compliance"], label_visibility="collapsed")
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- ADMIN CONSOLE FEATURE ---
    if nav == "🛠️ Admin Console":
        st.title("User Administration")
        st.write("Authorize new emails to use the AI Reading service.")
        
        new_acc = st.text_input("New Business Email to Assign:")
        if st.button("Save to Database"):
            if new_acc and new_acc not in registry["assigned_emails"]:
                registry["assigned_emails"].append(new_acc)
                save_registry(registry)
                st.success(f"Permitted: {new_acc}")
        
        st.divider()
        st.subheader("Stored User Database")
        st.table(registry["assigned_emails"])

    # --- INBOX & AI READING FEATURE ---
    elif nav == "📩 Inbox":
        col_list, col_view = st.columns([1, 2])
        
        with col_list:
            st.subheader("Focused Stream")
            # This is where your filtered engine.get_business_emails() would go
            mock_emails = [
                {"id": 1, "sender": "Mark Stevens", "subject": "Quarterly Deck", "body": "I've uploaded the Q1 results for the reading portal..."},
                {"id": 2, "sender": "Finance Team", "subject": "Invoice Approval", "body": "Please approve the vendor invoice for the AI suite..."},
            ]
            
            for m in mock_emails:
                with st.container():
                    st.markdown(f"""
                    <div class="email-row">
                        <div class="sender-label">👤 {m['sender']}</div>
                        <div class="subject-label">{m['subject']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"View Analyze {m['id']}", key=f"btn_{m['id']}", use_container_width=True):
                        st.session_state.active_mail = m

        with col_view:
            if 'active_mail' in st.session_state:
                mail = st.session_state.active_mail
                st.title(mail['subject'])
                st.write(f"**From:** {mail['sender']}")
                
                # --- AI READING COMPONENT ---
                with st.container():
                    st.markdown("### ✨ AI Reading Analysis")
                    with st.spinner("Analyzing intent..."):
                        # In production, replace with: analysis = engine.analyze(mail['body'])
                        st.info("**Summary:** This email is a formal request for document approval. **Action Item:** Review the PDF and sign by Friday.")
                
                st.text_area("Full Message Content", value=mail['body'], height=450, disabled=True)
            else:
                st.info("Select a business communication to begin AI analysis.")

# --- 6. ROUTER ---
if not st.session_state.authenticated:
    show_login()
else:
    show_workspace()
