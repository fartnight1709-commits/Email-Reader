import streamlit as st
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import EmailAnalysis, PriorityLevel

# Configuration for Garrison Financial's High-Stake Environment
LLM_MODEL = "gemini-1.5-pro"
TEMPERATURE = 0.2

class IntelliMailEngine:
    def __init__(self):
        """
        Initializes the Gemini Pro engine with structured output capabilities.
        Ensure GOOGLE_API_KEY is set in your Streamlit secrets or environment.
        """
        api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in secrets or environment variables.")

        # Corrected: Using ChatGoogleGenerativeAI for Gemini models
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL, 
            temperature=TEMPERATURE,
            google_api_key=api_key
        )
        
        # Enforces the AI to follow the schema defined in models.py
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)

    def get_api_status(self):
        """Returns the internal status of the AI Engine."""
        return "Operational - Cluster Alpha-1 (Garrison Financial)"

    def analyze_email(self, content: str, sender_info: str = "Unknown") -> EmailAnalysis:
        """
        Principal-grade analysis pipeline. 
        Analyzes content, determines priority, and generates a draft.
        """

        system_prompt = """
        You are the CEO of Garrison Financial based in Scottsdale, Arizona. 
        You are highly professional, decisive, and focused on client trust.
        Your task is to process incoming emails with 100% accuracy.
        
        RULES:
        1. CRITICAL Priority: Legal threats, financial transactions >$100k, direct board member requests, or time-sensitive Scottsdale regulatory issues.
        2. HIGH Priority: Active client requests, internal management blockers, or requests from direct reports.
        3. TONE: Match the sender's professionalism. If they are brief, you be brief. Ensure the tone reflects Garrison Financial's prestige.
        4. PRIVACY: Do not mention internal PII (Social Security Numbers, specific account numbers) in the suggested reply.
        5. CONTEXT: You are in Scottsdale, AZ. Acknowledge local context if relevant to the sender.
        """

        # Fixed the typo "systemn" to "system"
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Sender Context: {context}\n\nEmail Content:\n{content}")
        ])

        # Execution Chain
        chain = prompt | self.structured_llm
        return chain.invoke({"context": sender_info, "content": content})

# --- Helper Functions for Streamlit UI ---

def get_api_status():
    """Top-level status check for the dashboard sidebar."""
    return "Operational - Ready for OAuth"

def get_google_auth_url():
    """
    Generates the professional 'Sign in with Google' link.
    Requires GOOGLE_CLIENT_ID to be set in .streamlit/secrets.toml
    """
    try:
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
    except KeyError:
        return "#error-missing-client-id"
