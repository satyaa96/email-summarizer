import os
import base64
import time
import cohere
from dotenv import load_dotenv
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from email import message_from_bytes

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_unread_emails(service):
    # Get 24 hours ago as epoch timestamp
    twenty_four_hours_ago = int(time.time()) - 86400
    query = f"is:unread after:{twenty_four_hours_ago}"

    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_content(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
    raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = message_from_bytes(raw_msg)

    subject = mime_msg['subject']
    sender = mime_msg['from']

    body = ""
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body += part.get_payload(decode=True).decode()
                except:
                    pass
    else:
        try:
            body = mime_msg.get_payload(decode=True).decode()
        except:
            pass

    return subject, sender, body

def summarize_email(text):
    try:
        response = co.chat(
            model="command-r-plus",
            message=f"Summarize this email clearly and briefly:\n\n{text}",
            temperature=0.3,
            max_tokens=150
        )
        return response.text.strip()
    except Exception as e:
        print("Cohere error:", str(e))
        return "Failed to summarize due to API error."

def main():
    try:
        service = authenticate_gmail()
        messages = fetch_unread_emails(service)

        if not messages:
            print("No unread emails in the last 24 hours.")
            return

        print(f"Found {len(messages)} unread emails in the last 24 hours.\n")

        for msg in messages:
            subject, sender, body = get_email_content(service, msg['id'])

            print(f"\nFrom: {sender}")
            print(f"Subject: {subject}")
            print("Summary:")
            summary = summarize_email(body)
            print(summary)
            print("-" * 50)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
