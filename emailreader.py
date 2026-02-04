import streamlit as st
import engine
import time

# --- 1. SETTINGS & ACCESS CONTROL ---
st.set_page_config(page_title="IntelliMail | Secure Access", layout="wide")

# Mock Database (In production, you'd link this to a CSV or Database)
if 'authorized_users' not in st.session_state:
    st.session_state.authorized_users = ["admin@example.com", "dev@example.com"]
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 2. AUTHENTICATION GATE ---
def check_auth():
    if not st.session_state.authenticated:
        st.title("🛡️ IntelliMail Secure Gateway")
        st.warning("Access Restricted. Please sign into your **Assigned Account** to proceed.")
        
        # Placeholder for your Google Auth Link from engine.py
        auth_url = engine.get_google_auth_url()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.link_button("🔑 Sign in with Google", auth_url, type="primary"):
                # Logic: After Google returns, you'd check if email in st.session_state.authorized_users
                pass
            
            # DEV OVERRIDE (For you to test right now)
            with st.expander("Dev Access"):
                email_test = st.text_input("Enter Email for testing:")
                if st.button("Simulate Login"):
                    if email_test in st.session_state.authorized_users:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email_test
                        if email_test == "admin@example.com":
                            st.session_state.is_admin = True
                        st.rerun()
                    else:
                        st.error("Account not assigned. Contact Administrator.")
        st.stop() # Stops the rest of the app from loading

check_auth()

# --- 3. THE PRIVATE APP (Only shown if authenticated) ---

# Sidebar Navigation
with st.sidebar:
    st.title("IntelliMail Pro")
    st.write(f"👤 {st.session_state.user_email}")
    
    pages = ["Intelligence Dashboard", "Security & Privacy"]
    if st.session_state.is_admin:
        pages.append("🛠️ ADMIN CONSOLE")
    
    selection = st.radio("Navigation", pages)
    
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

# --- 4. ADMIN CONSOLE PAGE ---
if selection == "🛠️ ADMIN CONSOLE":
    st.title("Admin Control Panel")
    st.subheader("Manage Assigned Accounts")
    
    new_user = st.text_input("Assign New User (Email):")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Add User"):
            if new_user and new_user not in st.session_state.authorized_users:
                st.session_state.authorized_users.append(new_user)
                st.success(f"Access granted to {new_user}")
    
    st.divider()
    st.write("### Currently Assigned Users")
    for user in st.session_state.authorized_users:
        st.code(user)

# --- 5. DASHBOARD PAGE ---
elif selection == "System Dashboard":
    st.title("🚀 Intelligence Dashboard")
    # ... your existing high-end dashboard code here ...
    st.info("System fully operational. Analyzing assigned account data.")

# --- 6. PRIVACY PAGE ---
elif selection == "Security & Privacy":
    st.title("🛡️ Compliance & Privacy")
    # ... your professional legal text here ...
