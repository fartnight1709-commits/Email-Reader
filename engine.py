import streamlit as st

def get_api_status():
    """Returns the current status of the AI engine."""
    return "Operational - Ready for OAuth"

def get_google_auth_url():
    """Generates the professional 'Sign in with Google' link."""
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    # This must match exactly what you put in Google Cloud Console
    redirect_uri = "https://emailreads.streamlit.app" 
    scope = "https://www.googleapis.com/auth/gmail.readonly"
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"redirect_uri={redirect_uri}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return auth_url
