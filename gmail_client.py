from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

def get_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)

def fetch_inbox(creds, max_results=10):
    service = get_gmail_service(creds)
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = data["payload"]["headers"]
        body = ""

        for part in data["payload"].get("parts", []):
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8")

        email = {
            "id": msg["id"],
            "sender": next(h["value"] for h in headers if h["name"] == "From"),
            "subject": next(h["value"] for h in headers if h["name"] == "Subject"),
            "body": body
        }
        emails.append(email)

    return emails
