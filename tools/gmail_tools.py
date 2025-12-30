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
        print(f"Got error {e}")
        return []

