import streamlit as st
import time
import engine 

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(
    page_title="IntelliMail | Secure Business",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HIGH-VISIBILITY DARK CSS ---
st.markdown("""
    <style>
    /* Dark Slate Background */
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Neon Blue Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #161b22 !important; 
        border-right: 2px solid #58a6ff; 
    }
    
    /* High-Contrast Email Cards */
    .email-card {
        padding: 20px;
        background-color: #1c2128;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        border-left: 6px solid #58a6ff;
    }
    .sender-text { color: #58a6ff; font-weight: 800; font-size: 1.2em; }
    .subject-text { color: #f0f6fc; font-weight: 700; font-size: 1.1em; margin: 8px 0; }
    .snippet-text { color: #8b949e; font-size: 0.95em; }

    /* Giant Title Bar */
    .hero-header {
        background: #161b22;
        padding: 30px;
        border-bottom: 2px solid #58a6ff;
        margin: -5rem -5rem 2rem -5rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'admin' not in st.session_state:
    st.session_state.admin = False
if 'whitelist' not in st.session_state:
    st.session_state.whitelist = ["dev@intellimail.ai"]

# --- 4. THE SIGN-IN GATEWAY ---
def sign_in_page():
    st.markdown('<div class="hero-header"><h1>🛡️ INTELLIMAIL SECURE ACCESS</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.error("### RESTRICTED AREA")
        st.write("Please authenticate with your assigned business credentials.")
        
        # Real Google Login
        auth_url = engine.get_google_auth_url()
        st.link_button("🚀 LOGIN WITH GOOGLE", auth_url, use_container_width=True, type="primary")
        
        st.divider()
        
        # Hidden Dev Override
        with st.expander("Unlock Console (Dev Only)"):
            key = st.text_input("Portal Key:", type="password")
            if key == "devmode":
                st.session_state.auth = True
                st.session_state.admin = True
                st.rerun()

# --- 5. THE WORKSPACE ---
def workspace():
    st.markdown('<div class="hero-header"><h2 style="margin:0;">WORKSPACE: FOCUSED INBOX</h2></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("INTELLIMAIL")
        st.divider()
        nav = ["📥 Inbox", "🛡️ Compliance"]
        if st.session_state.admin:
            nav.append("🛠️ Admin Console")
        
        choice = st.radio("GO TO:", nav)
        
        st.divider()
        if st.button("🔴 SECURE LOGOUT"):
            st.session_state.auth = False
            st.rerun()

    # PAGE: ADMIN CONSOLE
    if choice == "🛠️ Admin Console":
        st.title("Account Adder Console")
        new_acc = st.text_input("Enter Email to Assign:")
        if st.button("GRANT ACCESS"):
            if new_acc and new_acc not in st.session_state.whitelist:
                st.session_state.whitelist.append(new_acc)
                st.success(f"Access granted to {new_acc}")
        
        st.write("### Assigned Accounts")
        for acc in st.session_state.whitelist:
            st.code(acc)

    # PAGE: COMPLIANCE
    elif choice == "🛡️ Compliance":
        st.title("Legal & Privacy")
        st.markdown("### Privacy Policy\nWe adhere to Google's Limited Use Policy. No data is stored.")

    # PAGE: INBOX
    else:
        col_list, col_view = st.columns([1, 1.5])
        
        with col_list:
            st.subheader("Business Streams")
            
            # Dummy Business Data
            emails = [
                {"id": 1, "sender": "Mark Stevens", "subject": "Project Phoenix Update", "body": "The due diligence is complete for the Scottsdale assets..."},
                {"id": 2, "sender": "Legal Team", "subject": "Contract Revision", "body": "Please review the signature line on the service agreement..."},
            ]
            
            for m in emails:
                st.markdown(f"""
                <div class="email-card">
                    <div class="sender-text">👤 {m['sender']}</div>
                    <div class="subject-text">{m['subject']}</div>
                    <div class="snippet-text">{m['body'][:80]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Fixed Button (No more TypeError)
                if st.button(f"OPEN ANALYTICS: {m['sender']}", key=f"mail_{m['id']}", use_container_width=True):
                    st.session_state.current_mail = m

        with col_view:
            if 'current_mail' in st.session_state:
                mail = st.session_state.current_mail
                st.title(mail['subject'])
                st.write(f"**From:** {mail['sender']}")
                
                st.info("✨ **AI SMART SUMMARY:** This email requires a signature on the Phoenix project contract.")
                
                st.text_area("Original Content", value=mail['body'], height=450, disabled=True)
            else:
                st.info("Select a business communication to begin.")

# --- 6. ROUTER ---
if not st.session_state.auth:
    sign_in_page()
else:
    workspace()
