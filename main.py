from Auth.main import auth
from tools.gmail_tools import search_messages, get_message

if __name__ == "__main__":
    service = auth("Test")
    msg = search_messages(service, query="Test" ,max_results = 1)
    print(get_message(service=service, message_id=msg[0].get('id')))
