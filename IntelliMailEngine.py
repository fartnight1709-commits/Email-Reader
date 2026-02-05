import streamlit as st
import IntelliMail as engine
from models import Category

st.set_page_config(page_title="IntelliMail Pro", layout="wide")

# Executive Styling
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .email-card { 
        background: #1E293B; padding: 15px; border-radius: 8px; 
        border-left: 5px solid #64748B; margin-bottom: 10px; 
    }
    .fin-card { border-left-color: #EF4444; } /* Red for Financial */
    .cli-card { border-left-color: #38BDF8; } /* Blue for Clients */
    </style>
""", unsafe_allow_html=True)

if 'credentials' not in st.session_state:
    # (Insert your Google Login Button code here)
    st.title("Please Sign In")
else:
    ai = engine.IntelliMailEngine()
    
    # 1. Fetch Real Emails
    raw_emails = ai.fetch_live_emails(st.session_state.credentials)
    
    # 2. Run Gemini on the batch (This makes the AI "work")
    if 'processed_inbox' not in st.session_state:
        with st.spinner("Gemini is analyzing your vaults..."):
            st.session_state.processed_inbox = ai.batch_analyze(raw_emails)

    # 3. Create the Separate Inboxes
    tab_fin, tab_clients, tab_misc = st.tabs(["💰 Financial Vault", "🤝 Clients", "📬 Regular"])

    def render_list(category_type, css_class):
        items = [e for e in st.session_state.processed_inbox if e['ai'].category == category_type]
        if not items:
            st.caption(f"No {category_type.lower()} items detected.")
        for e in items:
            with st.container():
                st.markdown(f"<div class='email-card {css_class}'><b>{e['sender']}</b><br>{e['ai'].summary_executive}</div>", unsafe_allow_html=True)
                if st.button("Open Intelligence", key=e['id']):
                    st.session_state.active_mail = e

    with tab_fin:
        render_list(Category.FINANCIAL, "fin-card")

    with tab_clients:
        render_list(Category.CLIENTS, "cli-card")

    with tab_misc:
        # Show both Regular and News here
        items = [e for e in st.session_state.processed_inbox if e['ai'].category in [Category.REGULAR, Category.NEWS]]
        for e in items:
            st.write(f"**{e['sender']}**: {e['ai'].summary_executive}")
