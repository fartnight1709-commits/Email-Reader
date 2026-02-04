import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, PriorityLevel

LLM_MODEL = "gemini-1.5-pro"

class IntelliMailEngine:
    def __init__(self):
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        self.client_id = st.secrets.get("GOOGLE_CLIENT_ID")
        self.client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = "https://intellimail.streamlit.app/"

        if not self.api_key:
            st.error("Engine Critical Error: GOOGLE_API_KEY missing.")
            return

        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL, 
            temperature=0.2,
            google_api_key=self.api_key
        )
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def get_google_auth_url(self):
        """Generates the professional 'Sign in with Google' link."""
        flow = Flow.from_client_config(
            {"web": {"client_id": self.client_id, "client_secret": self.client_secret,
                     "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                     "token_uri": "https://oauth2.googleapis.com/token"}},
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri=self.redirect_uri
        )
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        return auth_url

    def analyze_email(self, content: str, sender_info: str = "Unknown") -> EmailAnalysis:
        system_prompt = """
        You are the CEO of Garrison Financial (Scottsdale, AZ). 
        Analyze with 100% precision for a high-net-worth environment.
        1. CRITICAL: Legal threats, transactions >$100k, board requests.
        2. HIGH: Client requests, management blockers.
        3. TONE: Executive, brief, prestigious.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Sender: {context}\n\nContent:\n{content}")
        ])
        return (prompt | self.structured_llm).invoke({"context": sender_info, "content": content})

def get_api_status():
    return "Operational - Cluster Alpha-1"
