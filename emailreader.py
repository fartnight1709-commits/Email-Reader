import streamlit as st
import json
import os
import engine # Ensure engine.py handles your Google OAuth and AI calls

# --- 1. PERSISTENCE & STYLING ---
DB_FILE = "user_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"users": ["dev@intellimail.ai"]}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

st.set_page_config(page_title="IntelliMail Pro", layout="wide")

# --- 2. HIGH-END OLED CSS ---
st.markdown("""
    <style>
    /* Ultra Dark Background */
    .stApp { background-color: #050608; color: #e1e1e1; }
    
    /* Slim Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #0b0d11 !important; 
        border-right: 1px solid #1f232a; 
    }

    /* Outlook Blue Ribbon */
    .outlook-header {
        background: #0078d4;
        padding: 12px 24px;
        margin: -5rem -5rem 1rem -5rem;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* Glassmorphism Cards */
    .email-card {
        background: #111418;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #21262d;
        margin-bottom: 10px;
        transition: 0.2s;
    }
    .email-card:hover { border-color: #58a6ff; background: #161b22; }
    .sender-tag { color: #58a6ff; font-weight: 700; font-size: 0.85rem; }
    .subject-tag { color: #f0f6fc; font-weight: 600; font-size: 0.95rem; margin: 4px 0; }
    
    /* Login Card */
    .login-box {
        background: #0d1117;
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & ROUTING ---
db = load_db()
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# --- 4. THE HOME SCREEN (Login & Linking) ---
def show_home():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, mid, c3 = st.columns([1, 1.8, 1])
    
    with mid:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.title("🛡️ IntelliMail Secure")
        st.write("Link your business account to enable AI insights.")
        
        # LINKING INPUT
        email_input = st.text_input("Enter Authorized Email", placeholder="yourname@business.com")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔗 Link & Sign In", use_container_width=True, type="primary"):
                if email_input in db["users"]:
                    # Trigger Google OAuth from your engine
                    auth_url = engine.get_google_auth_url()
                    st.session_state.auth_state = True
                    st.session_state.user_email = email_input
                    st.link_button("Confirm with Google", auth_url)
                else:
                    st.error("Account not whitelisted.")
        
        with col_btn2:
            # Dev Override for you
            with st.popover("Dev Access"):
                key = st.text_input("Bypass Key", type="password")
                if key == "devmode":
                    st.session_state.auth_state = True
                    st.session_state.user_email = "Admin_User"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. THE WORKSPACE (AI Inbox) ---
def show_workspace():
    st.markdown('<div class="outlook-header"><h3 style="margin:0;color:white;">IntelliMail | Workspace</h3></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.user_email}**")
        st.divider()
        menu = st.radio("Navigation", ["📩 Focused Inbox", "🛠️ Admin Tools", "⚖️ Compliance"], label_visibility="collapsed")
        st.divider()
        if st.button("🔴 Logout", use_container_width=True):
            st.session_state.auth_state = False
            st.rerun()

    if menu == "🛠️ Admin Tools":
        st.header("Administration Console")
        new_acc = st.text_input("Whitelisted Email:")
        if st.button("Add to Database"):
            if new_acc and new_acc not in db["users"]:
                db["users"].append(new_acc)
                save_db(db)
                st.success(f"Registered {new_acc}")
        st.table(db["users"])

    elif menu == "📩 Focused Inbox":
        col_list, col_view = st.columns([1, 2])
        
        with col_list:
            st.subheader("Business Stream")
            # --- AI FILTERING LOGIC ---
            # Replace with engine.get_business_emails()
            mails = [
                {"id": 1, "sender": "Mark Stevens", "subject": "Project Phoenix Update", "body": "Due diligence is complete..."},
                {"id": 2, "sender": "Finance Dept", "subject": "Invoice #881", "body": "Please approve the AI suite payment..."},
            ]
            
            for m in mails:
                st.markdown(f"""
                <div class="email-card">
                    <div class="sender-tag">👤 {m['sender']}</div>
                    <div class="subject-tag">{m['subject']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Scan Email {m['id']}", key=f"scan_{m['id']}", use_container_width=True):
                    st.session_state.active_mail = m

        with col_view:
            if 'active_mail' in st.session_state:
                mail = st.session_state.active_mail
                st.title(mail['subject'])
                st.caption(f"From: {mail['sender']} | Status: **AI Scanned**")
                
                # --- AI SCANNING OUTPUT ---
                with st.expander("✨ AI SMART ANALYSIS", expanded=True):
                    with st.spinner("AI is reading..."):
                        # analysis = engine.get_ai_summary(mail['body'])
                        st.info("**Key Takeaway:** Urgent request for document signature. **Action:** Review the PDF and reply by 5 PM.")
                
                st.text_area("Original Content", value=mail['body'], height=400, disabled=True)
            else:
                st.info("Select a message to run the AI scan.")

# --- 6. ROUTER ---
if not st.session_state.auth_state:
    show_home()
else:
    show_workspace()
