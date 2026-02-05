import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, Category

class IntelliMailEngine:
    def __init__(self):
        # Fetching credentials from st.secrets to avoid FileNotFoundError
        self.api_key = st.secrets["GOOGLE_API_KEY"]
        self.client_id = st.secrets["GOOGLE_CLIENT_ID"]
        self.client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", 
            temperature=0.2,
            google_api_key=self.api_key
        )
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def fetch_live_emails(self, credentials):
        """Connects to your real Gmail and pulls latest messages."""
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
        """Categorizes email into high-stake vaults for Garrison Financial."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are the CEO of Garrison Financial. Categorize this email into FINANCIAL, CLIENTS, or REGULAR."),
            ("user", "Sender: {context}\nContent: {content}")
        ])
        return (prompt | self.structured_llm).invoke({"context": sender_info, "content": content})
