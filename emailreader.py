import streamlit as st
import engine
import time

# --- 1. SLIM OUTLOOK CONFIG ---
st.set_page_config(
    page_title="IntelliMail | Secure Business",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE "OLED" DARK THEME ---
st.markdown("""
    <style>
    /* Ultra Dark Background */
    .stApp { background-color: #0b0b0b; color: #e1e1e1; }
    
    /* Slim Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
        min-width: 200px !important;
        max-width: 200px !important;
    }

    /* Outlook-Style Email Row (Slim) */
    .email-row {
        padding: 10px 15px;
        border-bottom: 1px solid #222;
        background-color: #111;
        cursor: pointer;
    }
    .email-row:hover { background-color: #1a1a1a; border-left: 3px solid #0078d4; }
    .sender { color: #0078d4; font-weight: 700; font-size: 0.85rem; }
    .subject { color: #ffffff; font-weight: 600; font-size: 0.95rem; display: block; }
    .preview { color: #888; font-size: 0.8rem; }

    /* Custom Header */
    .header-ribbon {
        background-color: #111;
        border-bottom: 1px solid #333;
        padding: 10px 25px;
        margin: -5rem -5rem 1rem -5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & AUTH ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user_db' not in st.session_state:
    st.session_state.user_db = ["admin@intellimail.ai"]

# --- 4. THE GATEWAY (SIGN IN) ---
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔒 Secure Workspace</h2>", unsafe_allow_html=True)
        st.info("Authorized Personnel Only")
        
        # Proper OAuth Link
        auth_url = engine.get_google_auth_url()
        st.link_button("🔗 Link Authorized Account", auth_url, use_container_width=True)
        
        st.divider()
        # Admin Bypass for Testing
        bypass = st.text_input("Portal Key", type="password", placeholder="devmode")
        if bypass == "devmode":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 5. THE WORKSPACE (AFTER LOGIN) ---

# Sidebar Navigation (Slim)
with st.sidebar:
    st.markdown("### IntelliMail")
    st.caption("Active Session")
    st.divider()
    nav = st.radio("MENU", ["Inbox", "Admin Console", "Compliance"], label_visibility="collapsed")
    st.divider()
    if st.button("Logout", use_container_width=True):
        st.session_state.auth = False
        st.rerun()

# --- PAGE: ADMIN CONSOLE ---
if nav == "Admin Console":
    st.title("🛠️ Administration")
    st.write("Grant access to new business entities.")
    
    new_user = st.text_input("Account Email:")
    if st.button("Add Account"):
        if new_user and new_user not in st.session_state.user_db:
            st.session_state.user_db.append(new_user)
            st.success(f"Granted: {new_user}")
            
    st.divider()
    st.write("### Whitelist")
    for u in st.session_state.user_db:
        st.code(u)

# --- PAGE: COMPLIANCE ---
elif nav == "Compliance":
    st.title("🛡️ Legal & Privacy")
    st.markdown("""
    **Privacy Policy**
    IntelliMail uses Google's `gmail.readonly` scope. No data is shared or stored long-term.
    
    **Limited Use**
    Our app complies with Google's Limited Use requirements.
    """)

# --- PAGE: INBOX (OUTLOOK DESIGN) ---
else:
    st.markdown('<div class="header-ribbon"><h4>Focused Inbox</h4></div>', unsafe_allow_html=True)
    
    col_list, col_view = st.columns([1, 2.5])
    
    with col_list:
        # Business Filtered Data
        emails = [
            {"id": 1, "sender": "Mark Stevens", "subject": "Project Phoenix Update", "body": "The due diligence is complete. We are ready to move forward..."},
            {"id": 2, "sender": "Legal Team", "subject": "Urgent: Signature Required", "body": "Please review the attached contract for the Scottsdale property..."},
        ]
        
        for e in emails:
            with st.container():
                st.markdown(f"""
                <div class="email-row">
                    <div class="sender">👤 {e['sender']}</div>
                    <div class="subject">{e['subject']}</div>
                    <div class="preview">{e['body'][:50]}...</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open: {e['id']}", key=f"e_{e['id']}", use_container_width=True):
                    st.session_state.active_mail = e

    with col_view:
        if 'active_mail' in st.session_state:
            mail = st.session_state.active_mail
            st.markdown(f"## {mail['subject']}")
            st.caption(f"From: {mail['sender']} | Business Intelligence: **High Priority**")
            
            with st.expander("✨ AI SMART SUMMARY", expanded=True):
                st.write("This email requires immediate attention regarding the **Project Phoenix** contract signatures.")
            
            st.text_area("Content", value=mail['body'], height=500, disabled=True)
        else:
            st.info("Select a message to view analytics.")
