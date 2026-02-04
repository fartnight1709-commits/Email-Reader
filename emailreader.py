import streamlit as st
import engine
from models import PriorityLevel

# Premium Page Config
st.set_page_config(page_title="IntelliMail Pro", layout="wide", page_icon="📩")

# Executive-Grade CSS
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #1E293B; border-right: 1px solid #334155; }
    .email-card { border-left: 4px solid #38BDF8; padding: 15px; margin-bottom: 10px; background: #1E293B; border-radius: 4px; }
    .priority-critical { border-left-color: #EF4444; }
    .priority-high { border-left-color: #F59E0B; }
    </style>
""", unsafe_allow_html=True)

# Session State Init
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_mail' not in st.session_state: st.session_state.current_mail = None

def show_gateway():
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>INTELLIMAIL<span style='color:#38BDF8'>PRO</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94A3B8;'>Enterprise Intelligence for Garrison Financial</p>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if st.button("Sign in with Google", type="primary", use_container_width=True):
            # In production, this redirects to the auth_url
            st.session_state.auth = True
            st.rerun()

def main_dashboard():
    with st.sidebar:
        st.title("INTELLIMAIL")
        st.status(engine.get_api_status())
        st.write("👤 **Executive Account**")
        st.caption("ceo@garrisonfinancial.com")
        if st.button("Terminate Session"):
            st.session_state.auth = False
            st.rerun()

    col_list, col_view = st.columns([1, 2])

    with col_list:
        st.subheader("Intelligence Stream")
        mock_emails = [
            {"sender": "J. Wells (Legal)", "org": "Garrison Legal", "subject": "Urgent: Escrow $250k", "body": "Need approval for the Scottsdale land acquisition funds transfer.", "priority": "CRITICAL"},
            {"sender": "Sarah Miller", "org": "Client Relations", "subject": "Quarterly Update", "body": "Clients are requesting the Q4 performance reports by EOD.", "priority": "HIGH"}
        ]
        
        for i, m in enumerate(mock_emails):
            p_class = f"priority-{m['priority'].lower()}"
            with st.container():
                st.markdown(f"""<div class='email-card {p_class}'>
                    <small style='color:#38BDF8'>{m['priority']}</small><br>
                    <b>{m['sender']}</b><br>{m['subject']}</div>""", unsafe_allow_html=True)
                if st.button("View Analysis", key=f"v_{i}"):
                    st.session_state.current_mail = m

    with col_view:
        if st.session_state.current_mail:
            m = st.session_state.current_mail
            ai = engine.IntelliMailEngine()
            with st.spinner("Generating Intelligence..."):
                res = ai.analyze_email(m['body'], m['sender'])
                
                st.title(m['subject'])
                st.info(f"**AI Executive Summary:** {res.summary_executive}")
                
                c1, c2 = st.columns(2)
                c1.metric("Priority", res.priority, delta=res.priority_reasoning, delta_color="inverse")
                c2.metric("AI Confidence", f"{res.confidence_score}%")
                
                st.subheader("Actionable Intelligence")
                st.write(res.summary_bullets)
                
                st.subheader("Suggested Reply")
                st.text_area("CEO Draft", res.suggested_reply, height=200)
                st.button("Approve & Send")
        else:
            st.info("Select a high-signal communication to begin.")

if not st.session_state.auth: show_gateway()
else: main_dashboard()
