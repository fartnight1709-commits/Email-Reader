import streamlit as st
import time
import features
import engine
st.set_page_config(page_title="EmailAI Pro", layout="centered")
st.title("EmailAI Pro")
st.caption("Commercial Grade Email Intelligence")

email_input = st.text_area("Paste the email content here:", height=200)

if st.button("Analyze with AI"):
    if email_input:
        with st.spinner("Analyzing"):
            analysis = engine.analyze_email(email_input)

            st.subheader("Results")
            st.json(analysis)

            if analysis["length"] > 10:
                st.success(f"Action: {analysis['suggestion']}")
    else:
        st.wraning("Please paste an email first.")

st.sidebar.title("System Status")
st.sidebar.write(f"Engine: {engine.get_api_status()}")

st.title("Email AI")
user_input = st.text_input("Enter Email Content")

if st.button("Send Email Content!"):
    response = features.process_email(user_input)
    st.write(response)

# --- Page Configuration ---
st.set_page_config(page_title="Email reader", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("PROJECT V1")
    if st.button("Home"):
        st.write("Welcome Home!")
    if st.button("Activity Logs"):
        st.write("Viewing Logs...")
    
    st.divider()
    theme = st.selectbox("Appearance Mode", ["Dark", "Light"])

# --- MAIN AREA ---
st.title("Status: Ready")

# Text Box (Output area)
output_container = st.empty()
output_text = "Welcome to the Web UI. Click 'Start AI Process' to begin..."
output_container.text_area("AI Output", value=output_text, height=300)

# Action Button
if st.button("Start AI Process"):
    st.write("Processing...")
    
    # Progress Bar (Loading Bar)
    progress_bar = st.progress(0)
    
    for i in range(1, 101):
        time.sleep(0.03)  # Simulating work
        progress_bar.progress(i)
        
        # Update text at certain milestones
        if i == 25:
            st.toast("Task 25% complete...")
        if i == 50:
            st.toast("Halfway there!")
            
    st.success("Process Finished!")
