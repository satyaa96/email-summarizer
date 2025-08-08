import os.path
import base64
import json
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from summarize_emails import summarize_email  # Gemini function

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    emails = []

    if not messages:
        print("No unread messages.")
    else:
        print(f"Found {len(messages)} unread message(s):\n")

    for msg in messages[:10]:  # Limit to 10 for testing
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload'].get('headers', [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

        # Get body
        body = ""
        if 'data' in msg_data['payload'].get('body', {}):
            body = msg_data['payload']['body']['data']
        else:
            parts = msg_data['payload'].get('parts', [])
            for part in parts:
                if 'data' in part.get('body', {}):
                    body = part['body']['data']
                    break

        body = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8', errors='ignore')
        body_text = BeautifulSoup(body, "html.parser").get_text()

        emails.append({'from': sender, 'subject': subject, 'body': body_text})

    return emails

if __name__ == '__main__':
    service = authenticate_gmail()
    emails = get_unread_emails(service)

    for email in emails:
        print("=" * 60)
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print("\n📩 Summary:\n")
        summary = summarize_email(email['body'])
        print(summary)
        print("=" * 60)
