from Auth.main import auth
from tools.gmail_tools import search_messages, get_message, create_draft, send_message

if __name__ == "__main__":
    service = auth("Test")
    # msg = search_messages(service, query="Test" ,max_results = 1)
    # print(get_message(service=service, message_id=msg[0].get('id')))
    # print(create_draft(service=service, to="example1@gmail.com", subject="This is a test draft subject", body= "This is a test draft body", cc=['example2@gmail.com']))
    print(send_message(service=service, to="example1@gmail.com", subject="This is a test subject", body= "This is a test body"))