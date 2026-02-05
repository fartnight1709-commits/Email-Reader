import streamlit as st
import IntelliMail as engine
from models import Category

st.set_page_config(page_title="IntelliMail Pro", layout="wide", page_icon="🏦")

# Initialize Engine
ai_engine = engine.IntelliMailEngine()

# Executive Styling
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .vault-card { background: #1E293B; padding: 20px; border-radius: 12px; border-left: 5px solid #38BDF8; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

if 'credentials' not in st.session_state:
    st.title("Garrison Financial Gateway")
    st.link_button("🔐 Connect Gmail", ai_engine.get_google_auth_url(), type="primary")
else:
    # 1. Fetch & Batch Analyze (One-time process)
    if 'inbox' not in st.session_state:
        with st.spinner("Gemini is analyzing your vaults..."):
            raw = ai_engine.fetch_live_emails(st.session_state.credentials)
            # Process everything immediately
            st.session_state.inbox = [
                {**e, "ai": ai_engine.generate_briefing(e['body'], e['sender'])} for e in raw
            ]

    # 2. Separate Vault Tabs
    tab_fin, tab_cli, tab_reg = st.tabs(["💰 Financial Vault", "🤝 Client Relations", "📬 News/Regular"])

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
                    st.info(f"**Briefing:** {e['ai'].summary_executive}")
                with col2:
                    st.text_area("Suggested Reply:", value=e['ai'].suggested_reply, height=100, key=f"t_{e['id']}")
                    if st.button("Copy Draft", key=f"b_{e['id']}"):
                        st.toast("Copied!")
                st.divider()

    with tab_fin: show_vault(Category.FINANCIAL)
    with tab_cli: show_vault(Category.CLIENTS)
    with tab_reg: 
        # Show Regular and News together
        for e in [x for x in st.session_state.inbox if x['ai'].category in [Category.REGULAR, Category.NEWS]]:
            with st.expander(f"{e['sender']}: {e['subject']}"):
                st.write(e['ai'].summary_executive)
