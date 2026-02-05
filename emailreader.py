import streamlit as st
import IntelliMail as engine
from models import Category
from google_auth_oauthlib.flow import Flow

st.set_page_config(page_title="IntelliMail Pro", layout="wide", page_icon="🏦")

# 1. Initialize Engine
ai_engine = engine.IntelliMailEngine()

# 2. Handle Google OAuth Callback (The part that was missing)
query_params = st.query_params
if "code" in query_params and 'credentials' not in st.session_state:
    client_config = {
        "web": {
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        redirect_uri="https://intellimail.streamlit.app/"
    )
    flow.fetch_token(code=query_params["code"])
    st.session_state.credentials = flow.credentials
    st.query_params.clear() 
    st.rerun()

# Executive Styling
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .vault-card { background: #1E293B; padding: 20px; border-radius: 12px; border-left: 5px solid #38BDF8; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. UI Logic
if 'credentials' not in st.session_state:
    st.title("Garrison Financial Gateway")
    st.subheader("Connect your Scottsdale Executive Account")
    auth_url = ai_engine.get_google_auth_url()
    st.link_button("🔐 Connect Gmail", auth_url, type="primary")
else:
    st.title("Executive Intelligence Hub")
    
    # Fetch & Batch Analyze
    if 'inbox' not in st.session_state:
        with st.spinner("Gemini is analyzing your vaults..."):
            raw = ai_engine.fetch_live_emails(st.session_state.credentials)
            st.session_state.inbox = [
                {**e, "ai": ai_engine.generate_briefing(e['body'], e['sender'])} for e in raw
            ]

    # Tabs for separate inboxes
    tab_fin, tab_cli, tab_reg = st.tabs(["💰 Financial Vault", "🤝 Client Relations", "📬 Regular Stream"])

    def show_vault(cat_type):
        items = [e for e in st.session_state.inbox if e['ai'].category == cat_type]
        if not items:
            st.caption("No intelligence in this vault.")
            return

        for e in items:
            with st.container():
                st.markdown(f"### {e['subject']}")
                st.caption(f"From: {e['sender']}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("**Executive Briefing**")
                    st.info(e['ai'].summary_executive)
                with col2:
                    st.markdown("**Suggested Reply**")
                    st.text_area("Draft:", value=e['ai'].suggested_reply, height=120, key=f"t_{e['id']}")
                    if st.button("Copy Draft", key=f"b_{e['id']}"):
                        st.toast("Copied to clipboard!")
                st.divider()

    with tab_fin:
        show_vault(Category.FINANCIAL)
    with tab_cli:
        show_vault(Category.CLIENTS)
    with tab_reg:
        # Show both Regular and News in this tab
        reg_items = [x for x in st.session_state.inbox if x['ai'].category in [Category.REGULAR, Category.NEWS]]
        for e in reg_items:
            with st.expander(f"{e['sender']}: {e['subject']}"):
                st.write(e['ai'].summary_executive)
                st.text_area("Draft:", value=e['ai'].suggested_reply, key=f"reg_{e['id']}")
