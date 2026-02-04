import streamlit as st
import engine

# --- GLOBAL CONFIG ---
st.set_page_config(page_title="IntelliMail | Gateway", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .auth-card {
        background-color: #161b22;
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .stButton>button { background-color: #238636; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN UI ---
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("🔒 IntelliMail Secure")
        st.write("Authorize your workspace to begin.")
        
        # PROPER OAUTH LINKING
        auth_url = engine.get_google_auth_url()
        st.link_button("🔗 Link Authorized Google Account", auth_url)
        
        st.divider()
        # DEV BYPASS
        key = st.text_input("Admin Bypass Key:", type="password")
        if key == "devmode":
            st.session_state.authenticated = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.title("🚀 Business Workspace")
    st.success("Account Linked Successfully.")
    st.info("Select a page from the sidebar to manage accounts or view your inbox.")
