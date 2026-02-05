import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, Category

class IntelliMailEngine:
    def __init__(self):
        # Fetching credentials from Streamlit Secrets
        self.api_key = st.secrets["GOOGLE_API_KEY"]
        self.client_id = st.secrets["GOOGLE_CLIENT_ID"]
        self.client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
        # Ensure this matches your Authorized Redirect URI in Google Console
        self.redirect_uri = "https://intellimail.streamlit.app/" 

        # Initialize Gemini 1.5 Pro
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview", 
            temperature=0.2,
            google_api_key=self.api_key
        )
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def get_google_auth_url(self):
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
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        email_list = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = m['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            email_list.append({
                "id": msg['id'],
                "sender": sender,
                "subject": subject,
                "body": m['snippet']
            })
        return email_list

    def generate_briefing(self, content: str, sender: str) -> EmailAnalysis:
        system_prompt = """
        You are the Elite Executive Assistant for Garrison Financial. 
        Analyze the email and provide:
        1. CATEGORY: FINANCIAL (legal/money), CLIENTS (direct leads), or REGULAR.
        2. SUMMARY: A 1-sentence BLUF summary.
        3. DRAFT: A professional Scottsdale-executive style reply.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Sender: {sender}\nContent: {content}")
        ])
        return (prompt | self.structured_llm).invoke({"sender": sender, "content": content})
