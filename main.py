from Auth.main import auth
from tools.gmail_tools import search_messages

if __name__ == "__main__":
    service = auth("Test")
    print(search_messages(service, query="Quora" ,max_results = 1))
