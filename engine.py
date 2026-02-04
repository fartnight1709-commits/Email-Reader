import streamlit as st
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, PriorityLevel

LLM_MODEL = "gemini-1.5-pro"
TEMPERATURE = 0.2

class IntelliMailEngine:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=TEMPERATURE)
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def get_api_status(self):
        return "Operational - Cluster Alpha-1"
    
    def analyze_email(self, content: str, sender_info: str = "Unknown") -> EmailAnalysis:
        """
        Principal-grade analysis pipeline. 
        Analyzes content, determines priority, and generates a draft.
        """

        system_prompt = """
        You are the CEO for a company called Garrison Financial in scottsdale arizona. 
        Your task is to process incoming emails with 100% accuracy.
        
        RULES:
        1. CRITICAL Priority: Legal threats, financial transactions >$100k, direct board member requests.
        2. HIGH Priority: Active client requests, internal management blockers.
        3. TONE: Match the sender's professionalism. If they are brief, you be brief.
        4. PRIVACY: Do not mention internal PII in the suggested reply.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("systemn", system_prompt),
            ("user", "Sender Context: {context}\n\nEmail Content:\n{content}")
        ])

        chain = prompt | self.structured_llm
        return chain.invoke({"context": sender_info, "content": content})

def get_api_status():
    """Returns the current status of the AI engine."""
    return "Operational - Ready for OAuth"

def get_google_auth_url():
    """Generates the professional 'Sign in with Google' link."""
    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    # This must match exactly what you put in Google Cloud Console
    redirect_uri = "https://intellimail.streamlit.app/" 
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
