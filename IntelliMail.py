import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, Category 

class IntelliMailEngine:
    def __init__(self):
        """Initializes the engine using secure secrets."""
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        self.client_id = st.secrets.get("GOOGLE_CLIENT_ID")
        self.client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = "https://intellimail.streamlit.app/" 
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY missing from secrets.")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", 
            temperature=0.2,
            google_api_key=self.api_key
        )
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def get_google_auth_url(self):
        """Now properly contained within the class to fix AttributeErrors."""
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
        """Fetches real messages from the Gmail API."""
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = m['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            email_data.append({"id": msg['id'], "sender": sender, "subject": subject, "body": m['snippet']})
        return email_data

    def analyze_email(self, content: str, sender_info: str) -> EmailAnalysis:
        """Categorizes email into high-stake vaults: FINANCIAL, CLIENTS, or REGULAR."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are the CEO of Garrison Financial. Categorize this email into FINANCIAL, CLIENTS, or REGULAR."),
            ("user", "Sender: {context}\nContent: {content}")
        ])
        return (prompt | self.structured_llm).invoke({"context": sender_info, "content": content})
