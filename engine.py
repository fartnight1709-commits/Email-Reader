import os

def analyze_email(email_content):
    """
    This function handles the logic. 
    In a production app, this is where your OpenAI/Anthropic API calls live.
    """
    if not email_content:
        return "No content provided."
    

    word_count = len(email_content.split())
    
    result = {
        "status": "Processed",
        "length": word_count,
        "suggestion": "Draft a follow-up" if word_count < 50 else "Summarize this thread"
    }
    
    return result

def get_api_status():
    return "Operational"
