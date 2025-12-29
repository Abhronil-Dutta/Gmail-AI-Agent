import os
import json
from main import auth
from googleapiclient.errors import HttpError

class TestAuth():

    def __init__(self):
        self.test_user = "test_user"
        self.path_to_tokens = f"tokens/{self.test_user}_token.json"
        self.test_user_service = None
    
    def NormalAuthTest(self):
        print("\n--- Testing Normal Auth ---")
        service = auth(self.test_user)
        if not service:
            print("Failed! No service generated")
        if os.path.exists(self.path_to_tokens):
            with open(self.path_to_tokens, "r") as file:
                if file.readline() == "":
                    print("Failed! File is empty")
                    return
                else:
                    print(f"Success! {self.path_to_tokens} found! Auth successfull")
                    self.test_user_service = service
        else:
            print("Failed! File not found")
    
    def ExpiredTokenTest(self):
        print("\n--- Testing Expired Token ---")
        # TODO: Need to figure out how to automatically expire a token for testing
        # To expire a token right now, go to the token file and change the date of expiry
        if os.path.exists(self.path_to_tokens):
            service = auth(self.test_user)
            if service:
                print("Success! Expired token was refreshed and service was generated")
            else:
                print("Failed! Service not generated for expired token")
        else:
            print("Failed! Token file does not exist for expiry test")
    
    def InvalidTokenTest(self):
        print("\n--- Testing Invalid Token ---")
        invalid_user = "invalid_user_12345"
        invalid_path = f"tokens/{invalid_user}_token.json"
        
        service = auth(invalid_user)
        
        if service:
            if os.path.exists(invalid_path):
                print("Success! Invalid token triggered new auth flow and created new token")
            else:
                print("Failed! Service created but token file not saved")
        else:
            print("Failed! No service generated for invalid token scenario")
    
    def HttpErrorTest(self):
        print("\n--- Testing HttpError Handling ---")
        try:
            service = auth(self.test_user)
            if service is None:
                print("Success! HttpError was caught and None returned")
            else:
                print("Note: Service returned (no HttpError occurred in this test)")
        except HttpError as e:
            print(f"Failed! HttpError not caught properly: {e}")
        except Exception as e:
            print(f"Failed! Unexpected error: {e}")
    
    def SomeOtherErrorTest(self):
        print("\n--- Testing Other Error Handling ---")
        # Try with invalid path/credentials
        bad_user = "bad_user"
        try:
            service = auth(bad_user)
            if service is None:
                print("Success! Error was handled and None returned")
            else:
                print("Note: Service returned (no error occurred in this test)")
        except Exception as e:
            print(f"Note: Exception raised: {type(e).__name__}: {e}")


if __name__ == "__main__":
    tester = TestAuth()
    tester.NormalAuthTest() # Passed
    tester.ExpiredTokenTest() # Passed 
    tester.HttpErrorTest() # Need to figure out how to raise a HttpError to test
    tester.InvalidTokenTest() # Passed
    tester.SomeOtherErrorTest() # Failed need better error handling

    