import streamlit as st
import json
import os
import engine # Your logic for Google/AI

# --- 1. DATABASE LOGIC (Persistence) ---
DB_FILE = "user_registry.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"assigned_emails": ["dev@intellimail.ai"]}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- 2. THE ULTIMATE DARK UI ---
st.set_page_config(page_title="IntelliMail Pro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* OLED Background */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Slim Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #1a1a1a;
        width: 220px !important;
    }

    /* Outlook Header Ribbon */
    .outlook-ribbon {
        background-color: #0078d4;
        padding: 8px 20px;
        margin: -5rem -5rem 1rem -5rem;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Slim Email Cards */
    .email-item {
        padding: 12px;
        background-color: #0f0f0f;
        border: 1px solid #1a1a1a;
        border-left: 4px solid transparent;
        margin-bottom: 5px;
        border-radius: 4px;
    }
    .email-item:hover { border-left: 4px solid #0078d4; background-color: #161616; }
    .sender-name { color: #0078d4; font-weight: 700; font-size: 0.85rem; }
    .email-subject { font-weight: 600; color: #eee; font-size: 0.9rem; margin-top: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION & REGISTRY ---
db = load_db()
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- 4. SIGN-IN / ACCOUNT CREATION PAGE ---
def login_page():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1])
    
    with c2:
        st.markdown("<h2 style='text-align:center;'>📩 Create / Access Account</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔒 Secure Login", "✨ New Registration"])
        
        with tab1:
            st.write("Sign in with your assigned business email.")
            auth_email = st.text_input("Business Email")
            if st.button("Link Gmail Account"):
                if auth_email in db["assigned_emails"]:
                    # Redirect to your actual Google OAuth flow
                    auth_url = engine.get_google_auth_url()
                    st.link_button("Confirm Google Linking", auth_url)
                    st.session_state.auth = True # Bypass for your testing
                    st.rerun()
                else:
                    st.error("Account not assigned. Contact administrator.")

        with tab2:
            st.write("Enter your admin bypass key to register a new user.")
            admin_key = st.text_input("Portal Key", type="password")
            if admin_key == "devmode":
                st.session_state.auth = True
                st.session_state.is_admin = True
                st.rerun()

# --- 5. THE MAIN OUTLOOK WORKSPACE ---
def main_workspace():
    # Top Outlook Ribbon
    st.markdown('<div class="outlook-ribbon"><b>IntelliMail</b> | Focused Inbox</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.button("➕ New Message", use_container_width=True)
        st.divider()
        nav = ["📥 Inbox", "🛠️ Admin Console", "⚖️ Legal"]
        if not st.session_state.is_admin:
            nav.remove("🛠️ Admin Console")
        choice = st.radio("Navigation", nav, label_visibility="collapsed")
        
        st.divider()
        if st.button("Log Out"):
            st.session_state.auth = False
            st.rerun()

    if choice == "🛠️ Admin Console":
        st.title("Admin Administration")
        new_mail = st.text_input("Whitelisted Email:")
        if st.button("Register Account"):
            if new_mail and new_mail not in db["assigned_emails"]:
                db["assigned_emails"].append(new_mail)
                save_db(db)
                st.success(f"Added {new_mail} to database.")
        
        st.write("### Currently Assigned")
        st.table(db["assigned_emails"])

    elif choice == "⚖️ Legal":
        st.title("Compliance & Security")
        st.info("We adhere to Google's Limited Use Policy. Your data is never stored.")

    else: # INBOX VIEW
        col_list, col_view = st.columns([1, 2])
        
        with col_list:
            st.subheader("Focused")
            # Example Emails
            mails = [
                {"id": 1, "from": "John (Legal)", "sub": "Service Agreement", "body": "Please review the signature line..."},
                {"id": 2, "from": "Sarah (HR)", "sub": "Q1 Performance", "body": "The metrics for the quarter are in..."},
            ]
            for m in mails:
                with st.container():
                    st.markdown(f"""
                    <div class="email-item">
                        <div class="sender-name">{m['from']}</div>
                        <div class="email-subject">{m['sub']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"View {m['id']}", key=f"v_{m['id']}", use_container_width=True):
                        st.session_state.view_mail = m

        with col_view:
            if 'view_mail' in st.session_state:
                m = st.session_state.view_mail
                st.markdown(f"### {m['sub']}")
                st.caption(f"From: {m['from']}")
                st.divider()
                st.info("✨ **AI Summary:** Signature required on page 4 of document.")
                st.text_area("Content", value=m['body'], height=400, disabled=True)
            else:
                st.info("Select a business communication to start.")

# --- 6. ROUTING ---
if not st.session_state.auth:
    login_page()
else:
    main_workspace()
