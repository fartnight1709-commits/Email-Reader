import os
import google_auth_oauthlib.flow
import google.oauth2.credentials

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email"
]

def get_auth_url():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri="https://intellimail.streamlit.app/"
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    return auth_url, state

def exchange_code(code, state):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        state=state,
        redirect_uri="https://intellimail.streamlit.app/"
    )
    flow.fetch_token(code=code)
    return flow.credentials
