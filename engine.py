import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from models import EmailAnalysis

class IntelliMailEngine:
    def __init__(self):
        # Fetching credentials from st.secrets to avoid FileNotFoundError
        self.api_key = st.secrets["GOOGLE_API_KEY"]
        self.client_id = st.secrets["GOOGLE_CLIENT_ID"]
        self.client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
        self.redirect_uri = "https://intellimail.streamlit.app/"

    def get_google_auth_url(self):
        """Generates the secure login link for the UI."""
        client_config = {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        flow = Flow.from_client_config(
            client_config,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri=self.redirect_uri
        )
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        return auth_url

    def fetch_live_emails(self, credentials):
        """Connects to Gmail API and retrieves the latest messages."""
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Parsing headers for Subject and Sender
            headers = m['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            email_data.append({
                "id": msg['id'],
                "sender": sender,
                "subject": subject,
                "body": m['snippet'] # The real email content
            })
        return email_data
