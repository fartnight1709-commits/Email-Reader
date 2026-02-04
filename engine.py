import streamlit as st
import os
import json
import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, PriorityLevel

# Garrison Financial - Scottsdale Intelligence Config
LLM_MODEL = "gemini-1.5-pro"
TEMPERATURE = 0.2

class IntelliMailEngine:
    def __init__(self):
        """
        Initializes the Gemini Pro engine and Google API Connectors.
        """
        self.api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client_id = st.secrets.get("GOOGLE_CLIENT_ID")
        self.client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = "https://intellimail.streamlit.app/" 

        if not self.api_key:
            st.error("Engine Critical Error: GOOGLE_API_KEY missing.")
            return

        # AI Initialization
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL, 
            temperature=TEMPERATURE,
            google_api_key=self.api_key
        )
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def get_api_status(self):
        return "Operational - Cluster Alpha-1 (Garrison Financial)"

    # --- GOOGLE OAUTH & GMAIL LOGIC ---

    def get_google_auth_url(self):
        """Generates the OAuth2 URL for the CEO to sign in."""
        scope = ["https://www.googleapis.com/auth/gmail.readonly"]
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=scope,
            redirect_uri=self.redirect_uri
        )
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        return auth_url

    def fetch_emails(self, credentials):
        """Fetches the latest 10 emails from the authenticated Gmail account."""
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Basic parsing of snippet and headers
            headers = m['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            email_data.append({
                "id": msg['id'],
                "sender": sender,
                "subject": subject,
                "body": m['snippet']
            })
        return email_data

    # --- AI ANALYSIS LOGIC ---

    def analyze_email(self, content: str, sender_info: str = "Unknown") -> EmailAnalysis:
        """
        Principal-grade analysis pipeline for Garrison Financial.
        """
        system_prompt = """
        You are the CEO of Garrison Financial based in Scottsdale, Arizona. 
        You are highly professional, decisive, and focused on client trust.
        
        RULES:
        1. CRITICAL: Legal threats, transactions >$100k, direct board member requests.
        2. HIGH: Active client requests, internal management blockers.
        3. TONE: Professional, executive, and brief.
        4. PRIVACY: Do not mention internal PII (SSNs, Account IDs) in replies.
        5. CONTEXT: Scottsdale, AZ location.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Sender Context: {context}\n\nEmail Content:\n{content}")
        ])

        chain = prompt | self.structured_llm
        return chain.invoke({"context": sender_info, "content": content})

# --- UI Helper Functions ---

def get_api_status():
    return "Operational - Ready for OAuth"

def get_google_auth_url():
    """Standalone wrapper for the initial UI login button."""
    engine = IntelliMailEngine()
    return engine.get_google_auth_url()
