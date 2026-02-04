import streamlit as st
import time
import engine 

# --- 1. ENTERPRISE UI CONFIG ---
st.set_page_config(
    page_title="IntelliMail | Secure Business Workspace",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HIGH-CONTRAST CSS (EASY TO SEE) ---
st.markdown("""
    <style>
    /* High Contrast Backgrounds */
    .stApp { background-color: #f0f2f5; color: #1a1a1b; }
    [data-testid="stSidebar"] { 
        background-color: #ffffff !important; 
        border-right: 2px solid #0078d4; 
    }
    
    /* Bigger, Bolder Email List */
    .email-card {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #0078d4;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .sender-name { font-size: 1.1em; font-weight: 800; color: #0078d4; }
    .subject-line { font-size: 1em; font-weight: 700; color: #201f1e; margin: 5px 0; }
    .snippet { color: #444; font-size: 0.9em; line-height: 1.4; }
    
    /* Header Bar */
    .top-bar {
        background: linear-gradient(90deg, #0078d4 0%, #005a9e 100%);
        padding: 20px;
        color: white;
        margin: -5rem -5rem 2rem -5rem;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'assigned_accounts' not in st.session_state:
    st.session_state.assigned_accounts = ["dev@intellimail.app"]

# --- 4. THE SIGN-IN PAGE ---
def show_login_page():
    st.markdown('<div class="top-bar"><h1>IntelliMail Secure Gateway</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 🔐 Identity Verification")
        st.info("This application is restricted to assigned business accounts only.")
        
        # Main Sign In
        auth_url = engine.get_google_auth_url()
        st.link_button("🚀 Sign in with Authorized Google Account", auth_url, use_container_width=True, type="primary")
        
        st.divider()
        
        # Dev Secret Key Bypass
        with st.expander("Admin/Dev Access"):
            secret_key = st.text_input("Enter Portal Key:", type="password")
            if secret_key == "devmode":
                st.session_state.authenticated = True
                st.session_state.is_admin = True
                st.rerun()

# --- 5. THE ADMIN CONSOLE ---
def show_admin_console():
    st.title("🛠️ Account Adder Console")
    st.subheader("Manage Authorized Business Access")
    
    new_acc = st.text_input("Enter Email to Assign:")
    if st.button("Add to Whitelist"):
        if new_acc and new_acc not in st.session_state.assigned_accounts:
            st.session_state.assigned_accounts.append(new_acc)
            st.success(f"Access granted to {new_acc}")
            
    st.divider()
    st.write("### Currently Assigned Accounts")
    for acc in st.session_state.assigned_accounts:
        st.code(acc)

# --- 6. THE OUTLOOK WORKSPACE ---
def show_outlook_workspace():
    st.markdown('<div class="top-bar"><h2 style="margin:0;">Business Workspace</h2></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("IntelliMail")
        st.divider()
        nav = ["📥 Focused Inbox", "📜 Terms & Privacy"]
        if st.session_state.is_admin:
            nav.append("🛠️ Admin Console")
        
        choice = st.radio("Navigation", nav)
        
        st.divider()
        if st.button("Sign Out"):
            st.session_state.authenticated = False
            st.session_state.is_admin = False
            st.rerun()

    if choice == "🛠️ Admin Console":
        show_admin_console()
        
    elif choice == "📜 Terms & Privacy":
        st.title("Compliance & Security")
        st.markdown("### 1. Privacy Policy\nIntelliMail adheres to the **Google Limited Use Policy**. No raw email data is stored.")
        
    else: # Focused Inbox
        col_list, col_view = st.columns([1, 1.5])
        
        with col_list:
            st.subheader("Business Communications")
            
            # Dummy Business Data (Filtered to ignore verifications)
            emails = [
                {"id": 1, "sender": "Alex Rivera", "subject": "Project Proposal - Q2", "body": "Hey, I've attached the proposal for the upcoming Phoenix project..."},
                {"id": 2, "sender": "Finance Team", "subject": "Outstanding Invoice #991", "body": "Please review the attached invoice for last month's consultation fees..."},
            ]
            
            for m in emails:
                st.markdown(f"""
                <div class="email-card">
                    <div class="sender-name">👤 {m['sender']}</div>
                    <div class="subject-line">{m['subject']}</div>
                    <div class="snippet">{m['body'][:80]}...</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Analyze Email {m['id']}", key=f"btn_{m['id']}", use_container_width=True):
                    st.session_state.selected_email = m

        with col_view:
            if 'selected_email' in st.session_state and st.session_state.selected_email:
                mail = st.session_state.selected_email
                st.title(mail['subject'])
                st.write(f"**From:** {mail['sender']}")
                
                with st.expander("✨ AI BUSINESS INSIGHTS", expanded=True):
                    st.write("AI analysis identifies this as a **Priority 1** business request. Action required: Approval of document.")
                
                st.text_area("Message Content", value=mail['body'], height=400, disabled=True)
            else:
                st.info("Select a business email to view the AI analysis.")

# --- 7. MAIN ROUTER ---
if not st.session_state.authenticated:
    show_login_page()
else:
    show_outlook_workspace()
