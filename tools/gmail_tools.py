import base64
import json
from email.message import EmailMessage
from googleapiclient.errors import HttpError

# --- Utility functions ---

def _b64url_encode_bytes(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").replace('=', '')

def _formatted_message(raw_bytes: bytes) -> dict:
    """
    Docstring for _formatted_message
    
    :param raw_bytes: Takes in email message as bytes
    :type raw_bytes: bytes
    :return: returns base64 encoded payload for Gmail sending or drafting
    :rtype: dict
    """
    return {"raw": _b64url_encode_bytes(raw_bytes)}

# ---- Tools ----

# --- Tool : Search Messages ---

def search_messages(service, query: str, max_results: int = 10) -> list:
    
    try:
        resp = service.users().messages().list(userId='me', q= query, maxResults= max_results).execute()
        return resp.get('messages', [])
    except HttpError as e:
        raise RuntimeError(f"Got search_message error: {e}") from e
    
# --- Tools : Get Message ---

def get_message(service, message_id: str, format : str = "full"):

    try: 
        msg = service.users().messages().get(userId='me', id=message_id, format = format).execute()
    except HttpError as e:
        raise RuntimeError(f"Got get_message error: {e}") from e


    wanted_headers = {'From', 'Delivered-To', 'Subject', 'Date', 'Cc', 'Bcc', 'Reply-To', 'Message-ID', 'Recieved'}
    #Extract the Headers
    headers = {
        h['name']: h['value']
        for h in msg.get('payload', {}).get('headers', [])
        if h['name'] in wanted_headers
    }

    # Body
    body_text = None
    if format in ("full","raw"):

        # parts because emails are MIME trees
        parts = msg.get('payload', {}).get('parts') or []

        for p in parts:
            # MIME Types 'text/plain' , 'text/html', 'multipart/*', 'application/pdf'
            mime = p.get('mimeType', '')
            #we wanna work with text/plain 
            if mime == 'text/plain' and 'body' in p and 'data' in p['body']:

                #Decoding
                body_text = base64.urlsafe_b64decode(p['body']['data'] + '==').decode('utf-8', errors='replace')
                break

            if not body_text:
                # Snippet = Gmail's safe preview.. always present
                body_text = msg.get('snippet')
        
        return {
            "id" : msg.get('id'),
            "threadId": msg.get('threadId'),
            "headers": headers,
            "body_text": body_text,
            "raw": msg.get('raw')  # may be present if requested
        }

# --- Tool : Create a Draft ---

def create_draft(service, to: str, subject: str, body: str, cc: list[str] | None = None, bcc: list[str] | None = None):
    em = EmailMessage()
    em['To'] = to
    em['Subject'] = subject

    if cc:
        em['Cc'] = ", ".join(cc)
    if bcc:
        em['Bcc'] = ", ".join(bcc)
    
    em.set_content(body)

    raw = _formatted_message(em.as_bytes())

    try: 
        draft = service.users().drafts().create(
            userId='me',
            body = {'message': raw}
        ).execute()
        return draft
    except HttpError as e:
        raise RuntimeError(f"Got create_draft error : {e}") from e

# --- Tool : Send Message ---


# This tool instantly sends a message 
# This should be gated behind an explicit confirmation step
# when used by an agent.
def send_message(service, to: str,subject: str, body: str, cc: list[str] | None = None, bcc: list[str] | None = None, in_reply_to: str = None):

    em = EmailMessage()
    em['To'] = to
    em['Subject'] = subject
    
    if cc:
        em['Cc'] = ", ".join(cc)
    if bcc:
        em["Bcc"] = ", ".join(bcc)
    
    if in_reply_to:
        em['In-Reply-To'] = in_reply_to
        em['References'] = in_reply_to
    
    em.set_content(body)

    raw = _formatted_message(em.as_bytes())

    try:
        sent = service.users().messages().send(userId='me', body=raw).execute()
        return sent
    except HttpError as e:
        raise RuntimeError(f"Got send_message error : {e}") from e
