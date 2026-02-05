import streamlit as st
import os
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, Category # Ensure Category is in models.py

LLM_MODEL = "gemini-1.5-pro"
TEMPERATURE = 0.2

class IntelliMailEngine:
    def __init__(self):
        """Initializes engine using Streamlit secrets."""
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY missing from secrets.")

        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL, 
            temperature=TEMPERATURE,
            google_api_key=self.api_key
        )
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def fetch_live_emails(self, credentials):
        """Fetches real messages from Gmail API."""
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(userId='me', maxResults=15).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = m['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            email_data.append({
                "id": msg['id'],
                "sender": sender,
                "subject": subject,
                "body": m['snippet']
            })
        return email_data

    def analyze_email(self, content: str, sender_info: str = "Unknown") -> EmailAnalysis:
        """Categorizes and analyzes email for Garrison Financial."""
        system_prompt = """
        You are the CEO of Garrison Financial (Scottsdale, AZ). 
        Categorize into: FINANCIAL, CLIENTS, REGULAR, or NEWS.
        Rules:
        1. FINANCIAL: Legal, transfers >$100k, escrow.
        2. CLIENTS: Existing client requests.
        3. NEWS/REGULAR: Everything else.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Sender: {context}\n\nContent:\n{content}")
        ])
        return (prompt | self.structured_llm).invoke({"context": sender_info, "content": content})
