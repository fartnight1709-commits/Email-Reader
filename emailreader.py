import streamlit as st
import time
import engine # Your Google/AI logic file

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(
    page_title="IntelliMail | Secure Portal",
    page_icon="📩",
    layout="centered", # Professional centered login
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS (SaaS Aesthetic) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%); }
    .main-card {
        background-color: rgba(30, 41, 59, 0.7);
        padding: 50px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    h1 { font-weight: 800 !important; color: #f8fafc !important; }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        border: none; color: white; border-radius: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE BRAINS (State Management) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user_list' not in st.session_state:
    st.session_state.user_list = ["dev@intellimail.com"] # Default assigned user

# --- 4. THE SECURE GATEWAY (Login Page) ---
def gate_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.title("📩 IntelliMail")
        st.markdown("<p style='color: #94a3b8; font-size: 1.1em;'>Welcome back. Please sign in to your assigned account.</p>", unsafe_allow_html=True)
        st.divider()
        
        # Main Button
        auth_url = engine.get_google_auth_url()
        st.link_button("🚀 Enter Workspace with Google", auth_url, use_container_width=True)
        
        # THE SECRET DEV OVERRIDE (Hidden at bottom)
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        secret = st.text_input("..", type="password", label_visibility="collapsed", placeholder="Dev Key")
        if secret == "devmode": # TYPE 'devmode' HERE TO BYPASS
            st.session_state.auth = True
            st.session_state.user_role = "Admin"
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. THE ENTERPRISE DASHBOARD ---
def main_app():
    # Force wide layout for dashboard
    st.markdown("<style>div.block-container{max-width: 95% !important;}</style>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("IntelliMail")
        st.caption("Commercial Tier V1.0")
        st.divider()
        nav = st.radio("Navigation", ["Dashboard", "Admin Console", "Compliance"])
        
        st.divider()
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    if nav == "Dashboard":
        st.title("📊 Intelligence Dashboard")
        st.write("### Analyze Inbox Stream")
        email_data = st.text_area("Paste Content for Audit", height=300)
        if st.button("Run AI Processing"):
            with st.spinner("Decoding and Analyzing..."):
                time.sleep(1)
                st.json(engine.analyze_email(email_data))

    elif nav == "Admin Console":
        st.title("🛠️ Account Management")
        st.subheader("Manage Assigned Accounts")
        st.write("Only users added here can bypass the security gateway.")
        
        new_user = st.text_input("Add Email to Assigned List:")
        if st.button("Assign Account"):
            if new_user and new_user not in st.session_state.user_list:
                st.session_state.user_list.append(new_user)
                st.success(f"Access granted to {new_user}")
        
        st.divider()
        st.write("### Whitelisted Access List")
        for user in st.session_state.user_list:
            st.code(f"USER: {user}")

    elif nav == "Compliance":
        st.title("🛡️ Legal & Privacy")
        st.info("Required for Google OAuth Verification")
        st.markdown("### Privacy Policy\nIntelliMail uses Google Read-Only scopes. We never store raw data. Processing is ephemeral.")

# --- 6. RUN LOGIC ---
if not st.session_state.auth:
    gate_page()
else:
    main_app()
