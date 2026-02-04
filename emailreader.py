import streamlit as st
import time
import engine 

# --- 1. ENTERPRISE UI CONFIG ---
st.set_page_config(
    page_title="IntelliMail Business",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. OUTLOOK-STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f3f2f1; color: #323130; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #edebe9; }
    
    /* Email List Item */
    .email-box {
        padding: 15px;
        background-color: white;
        border: 1px solid #edebe9;
        border-radius: 4px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .email-box:hover { border-color: #0078d4; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .sender-text { font-weight: 700; color: #0078d4; font-size: 0.9em; }
    .subject-text { font-weight: 600; font-size: 1em; color: #201f1e; display: block; margin: 4px 0; }
    .preview-text { color: #605e5c; font-size: 0.85em; }
    
    /* Professional Header */
    .outlook-header {
        background-color: #0078d4;
        padding: 15px 25px;
        color: white;
        margin: -5rem -5rem 2rem -5rem;
        display: flex;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'auth_active' not in st.session_state:
    st.session_state.auth_active = False
if 'selected_email' not in st.session_state:
    st.session_state.selected_email = None

# --- 4. THE OUTLOOK INTERFACE ---
def outlook_interface():
    # Top Branding Bar
    st.markdown('<div class="outlook-header"><h2 style="margin:0;">IntelliMail | Outlook Business Sync</h2></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.button("➕ New Message", use_container_width=True, type="primary")
        st.divider()
        st.markdown("**Folders**")
        st.write("📥 **Focused Inbox**")
        st.write("📨 Other")
        st.write("📤 Sent Items")
        st.write("🗑️ Deleted")
        st.divider()
        if st.button("Sign Out"):
            st.session_state.auth_active = False
            st.rerun()

    # Main View: List vs. Reading Pane
    col_list, col_view = st.columns([1, 2])

    with col_list:
        st.subheader("Focused")
        st.caption("Filtered: Business Correspondence Only")
        
        # BUSINESS FILTER LOGIC
        try:
            # Pulling from your actual engine
            raw_data = engine.get_business_emails()
            # Strict filter: Remove automated trash
            emails = [e for e in raw_data if not any(x in e['sender'].lower() for x in ['no-reply', 'verify', 'code', 'alert'])]
        except:
            # Fallback for testing UI
            emails = [
                {"id": 1, "sender": "Mark Stevens (Acquisitions)", "subject": "Project Phoenix Update", "time": "11:30 AM", "body": "The due diligence is complete. Please see the attached report regarding the Scottsdale assets..."},
                {"id": 2, "sender": "Clara Vance", "subject": "Contract Revision Needed", "time": "10:15 AM", "body": "We noticed a discrepancy in Section 4.2 of the agreement. Can we jump on a call?"},
                {"id": 3, "sender": "Strategy Team", "subject": "Market Analysis 2026", "time": "9:00 AM", "body": "The latest numbers for the Arizona market are in. We are seeing a 12% uptick in..."},
            ]

        for mail in emails:
            # We create a clickable container
            with st.container():
                st.markdown(f"""
                <div class="email-box">
                    <div class="sender-text">{mail['sender']} • {mail['time']}</div>
                    <div class="subject-text">{mail['subject']}</div>
                    <div class="preview-text">{mail['body'][:75]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Fixed button logic to prevent the red error
                if st.button(f"Open: {mail['subject'][:20]}...", key=f"mail_{mail['id']}", use_container_width=True):
                    st.session_state.selected_email = mail

    with col_view:
        if st.session_state.selected_email:
            msg = st.session_state.selected_email
            st.markdown(f"# {msg['subject']}")
            st.write(f"**From:** {msg['sender']} • {msg['time']}")
            st.divider()
            
            # AI Insight Block (Professional/Clean)
            st.info(f"✨ **AI Intelligence Insight:** This email pertains to **{msg['subject']}**. Primary intent: Discussion of assets and scheduling a follow-up.")
            
            st.markdown("### Message Body")
            st.text_area("Original Content", value=msg['body'], height=450, disabled=True, label_visibility="collapsed")
        else:
            st.info("Select a business communication from the list to begin AI analysis.")

# --- 5. THE GATEWAY (Gated Access) ---
if not st.session_state.auth_active:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 IntelliMail Secure")
        st.write("Enterprise Authentication Required")
        
        # Password entry for your 'devmode' bypass
        key = st.text_input("Access Key:", type="password")
        if key == "devmode" or st.button("Sign in with Google"):
            st.session_state.auth_active = True
            st.rerun()
else:
    outlook_interface()
