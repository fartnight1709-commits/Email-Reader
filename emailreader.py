import streamlit as st
import IntelliMail as engine

st.set_page_config(page_title="IntelliMail Pro", layout="wide")

# Custom CSS for the Premium Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .email-box { background: #1E293B; padding: 20px; border-radius: 10px; border-left: 5px solid #38BDF8; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

if 'credentials' not in st.session_state:
    st.markdown("<h1 style='text-align:center;'>Garrison Financial Gateway</h1>", unsafe_allow_html=True)
    auth_url = engine.IntelliMailEngine().get_google_auth_url()
    st.link_button("🔐 Connect Your Gmail", auth_url, type="primary", use_container_width=True)
else:
    # This runs once you are logged in
    ai_engine = engine.IntelliMailEngine()
    emails = ai_engine.fetch_real_emails(st.session_state.credentials)
    
    col_list, col_view = st.columns([1, 1])
    with col_list:
        st.subheader("Your Real Inbox")
        for e in emails:
            with st.container():
                st.markdown(f"<div class='email-box'><b>{e['sender']}</b><br>{e['subject']}</div>", unsafe_allow_html=True)
                if st.button(f"Analyze: {e['id'][:5]}"):
                    st.session_state.active_email = e

    with col_view:
        if 'active_email' in st.session_state:
            st.write("### AI Analysis")
            st.write(st.session_state.active_email['body'])
