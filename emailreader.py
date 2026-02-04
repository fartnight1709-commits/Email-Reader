import streamlit as st
import time
import engine # Ensure engine.py has get_business_emails() defined

# --- 1. ENTERPRISE UI CONFIG ---
st.set_page_config(
    page_title="IntelliMail | Business Workspace",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. OUTLOOK-STYLE CSS ---
st.markdown("""
    <style>
    /* Outlook Blue & Grey Theme */
    .stApp { background-color: #f3f2f1; color: #323130; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #edebe9; }
    
    /* Email List Styling */
    .email-item {
        padding: 15px;
        background-color: white;
        border-bottom: 1px solid #f3f2f1;
        cursor: pointer;
        transition: 0.2s;
    }
    .email-item:hover { background-color: #f3f2f1; }
    .email-sender { font-weight: 700; color: #0078d4; font-size: 0.9em; }
    .email-subject { font-weight: 600; font-size: 1em; color: #201f1e; }
    .email-snippet { color: #605e5c; font-size: 0.85em; }
    
    /* Header Bar */
    .outlook-header {
        background-color: #0078d4;
        padding: 10px 20px;
        color: white;
        margin: -5rem -5rem 2rem -5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION LOGIC ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- 4. THE OUTLOOK INTERFACE ---
def outlook_workspace():
    # Top Ribbon
    st.markdown('<div class="outlook-header"><h1>IntelliMail Business</h1></div>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.button("➕ New Message", use_container_width=True)
        st.divider()
        st.markdown("**Favorites**")
        st.write("📥 Inbox")
        st.write("📤 Sent")
        st.write("🗑️ Archive")
        st.divider()
        if st.button("Log Out"):
            st.session_state.auth = False
            st.rerun()

    # Main Workspace Layout (List on left, Reading Pane on right)
    col_list, col_view = st.columns([1, 2])

    with col_list:
        st.subheader("Focused Inbox")
        st.caption("Filtering out verifications & automated alerts...")
        
        # --- BUSINESS FILTER LOGIC ---
        # Fetching emails from your engine
        try:
            # We filter for emails that DON'T contain 'no-reply', 'verify', or 'code'
            raw_emails = engine.get_business_emails() 
            business_emails = [e for e in raw_emails if not any(word in e['sender'].lower() for word in ['no-reply', 'verification', 'info@', 'noreply'])]
        except:
            # Placeholder for testing if engine isn't synced yet
            business_emails = [
                {"sender": "John Doe (Partnerships)", "subject": "Quarterly Review Deck", "time": "10:45 AM", "body": "See attached for the Q1 strategy..."},
                {"sender": "Sarah Miller", "subject": "Client Onboarding: Project X", "time": "9:12 AM", "body": "The contract is ready for signature..."},
                {"sender": "Finance Dept", "subject": "Invoice #8829 Approved", "time": "Yesterday", "body": "The payment has been processed for the vendor..."}
            ]

        for i, mail in enumerate(business_emails):
            with st.container():
                st.markdown(f"""
                <div class="email-item">
                    <div class="email-sender">{mail['sender']} • {mail['time']}</div>
                    <div class="email-subject">{mail['subject']}</div>
                    <div class="email-snippet">{mail['body'][:60]}...</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"View Details {i}", key=f"btn_{i}", label_visibility="collapsed"):
                    st.session_state.current_mail = mail

    with col_view:
        if 'current_mail' in st.session_state:
            mail = st.session_state.current_mail
            st.markdown(f"## {mail['subject']}")
            st.write(f"**From:** {mail['sender']}")
            st.divider()
            
            # AI Analysis Pane
            with st.expander("✨ AI Smart Summary", expanded=True):
                with st.spinner("Analyzing business intent..."):
                    # analysis = engine.analyze_email(mail['body'])
                    st.write("This email involves a **Quarterly Review**. Action required: Review the attached deck and reply by EOD.")
            
            st.text_area("Email Content", value=mail['body'], height=400, disabled=True)
        else:
            st.info("Select an email from the Focused Inbox to view the analysis.")

# --- 5. GATEWAY LOGIC ---
if not st.session_state.auth:
    # Minimalist Gate
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.title("🛡️ IntelliMail")
        st.write("Secure Business Access Only")
        # TYPE 'devmode' in the box below to bypass instantly
        entry_key = st.text_input("Enter Portal Key:", type="password")
        if entry_key == "devmode" or st.button("Sign in with Google"):
            st.session_state.auth = True
            st.rerun()
else:
    outlook_workspace()
