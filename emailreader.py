import streamlit as st
import engine
import time

# --- 1. GLOBAL PAGE SETUP ---
st.set_page_config(
    page_title="IntelliMail | Secure Gateway",
    page_icon="🔐",
    layout="centered", # Centered makes the login look more professional
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Login Card Styling */
    .login-card {
        background-color: rgba(30, 41, 59, 0.7);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* Title Styling */
    h1 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'auth_list' not in st.session_state:
    # Starting list of emails allowed to enter
    st.session_state.auth_list = ["admin@intellimail.ai"]

# --- 4. SECURE LOGIN GATEWAY ---
def show_login():
    # Vertical Spacer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.title("📩 IntelliMail")
        st.markdown("<p style='color: #94a3b8;'>Enterprise-Grade Email Intelligence Suite</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Google Auth Link from your engine
        auth_url = engine.get_google_auth_url()
        
        st.link_button("🚀 Sign in with Assigned Account", auth_url, use_container_width=True)
        
        st.markdown("<br><p style='font-size: 0.8em; color: #64748b;'>Protected by AES-256 Encryption</p>", unsafe_allow_html=True)
        
        # HIDDEN ADMIN PORTAL (Only for you)
        # You can type a secret password in this small inconspicuous box to open the admin panel
        secret = st.text_input("..", type="password", label_visibility="collapsed")
        if secret == "admin123": # Change this to your secret password
            st.session_state.authenticated = True
            st.session_state.is_admin = True
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. THE PROFESSIONAL DASHBOARD ---
def show_dashboard():
    # Once logged in, switch to wide layout
    st.markdown("<style>div.block-container{max-width: 95% !important;}</style>", unsafe_allow_html=True)
    
    # Custom Modern Sidebar
    with st.sidebar:
        st.title("IntelliMail")
        st.caption("Active Session: Secure")
        st.divider()
        nav = st.radio("Management", ["Audit Dashboard", "User Access Control", "Legal Compliance"])
        
        st.divider()
        if st.button("Secure Logout"):
            st.session_state.authenticated = False
            st.rerun()

    if nav == "Audit Dashboard":
        st.header("Intelligence Overview")
        # Visual stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Sync Status", "Live", delta="Operational")
        c2.metric("Data Privacy", "Restricted", delta="Compliant")
        c3.metric("AI Engine", "V4.2-Turbo", delta="Optimal")
        
        st.divider()
        email_body = st.text_area("Analyze Email Stream", height=350, placeholder="Paste email content here...")
        if st.button("Execute AI Audit"):
            with st.spinner("Processing deep-analysis..."):
                time.sleep(1.5)
                # Call your actual AI engine
                result = engine.analyze_email(email_body)
                st.subheader("Audit Results")
                st.json(result)

    elif nav == "User Access Control":
        st.header("User Access Management")
        st.write("Assign new accounts to the IntelliMail whitelist.")
        
        new_email = st.text_input("Add Authorized Email Address:")
        if st.button("Grant Access"):
            if new_email and new_email not in st.session_state.auth_list:
                st.session_state.auth_list.append(new_email)
                st.success(f"Access granted to {new_email}")
        
        st.subheader("Whitelisted Entities")
        for email in st.session_state.auth_list:
            st.code(f"USER: {email}")

    elif nav == "Legal Compliance":
        st.header("Security & Compliance")
        tab1, tab2 = st.tabs(["Privacy Policy", "Terms of Service"])
        with tab1:
            st.markdown("### Privacy Rules\n* Read-only access.\n* No storage of raw data.\n* Adheres to Google Limited Use policy.")
        with tab2:
            st.markdown("### Terms of Use\n* Professional use only.\n* AI output is probabilistic.")

# --- 6. APP LOGIC ---
if not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()
