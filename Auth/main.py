import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

# TODO: Add more Scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", 
          "https://www.googleapis.com/auth/gmail.compose", 
          "https://www.googleapis.com/auth/gmail.send",
        ]


def auth(user: str, port: int = 52088):
    """
    Docstring for auth
    
    :param user: User name to be used and saved, provided by caller
    :type user: str
    :param port: The localhost port OAuth will be running at, by default 52088 (aprooved redirect port in google client)
    :type port: int

    Returns:
    None : If any error occurs
    Gmail Service: If successfull
    """
    creds = None #Set creds to None

    # Check if credentials.json exists
    if not os.path.exists("credentials.json"):
        print("credentials.json doesn't exist!")
        return None

    #Check if the user exists
    if os.path.exists(f"tokens/{user}_token.json"):
        creds = Credentials.from_authorized_user_file(f"tokens/{user}_token.json", SCOPES)
    
    #Do this if user doesnt exist or user is not valid
    if not creds or not creds.valid:

        # If user's token has expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) #Refresh

        # User doesnt exist -> Create new user
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=port) 
        
        # Makes/ Updates the user
        with open(f"tokens/{user}_token.json", "w") as token:
            token.write(creds.to_json())

    # Build the Gmail Service to return
    try:
        service = build("gmail", "v1", credentials=creds)
        return service # Success
    except HttpError as e:
        print(f"Exception raised: {type(e).__name__}: {e}")
        return None
    # TODO: Make proper exception handling 
    except Exception as e:
        print(f"Exception raised: {type(e).__name__}: {e}")
        return None
