import streamlit as st
import os

def get_google_auth_url():
    """
    Creates the URL that redirects users to the 'Sign in with Google' page.
    """
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    redirect_uri = "https://emailreads.streamlit.app"
    scope = "https://www.googleapis.com/auth/gmail.readonly"
    
    # Keyword: Authorization URL
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

def analyze_with_ai(email_text):
    # This is where your AI feature lives
    # For a $100k app, this returns high-value insights
    return f"AI Analysis: {email_text[:50]}... is high priority."
