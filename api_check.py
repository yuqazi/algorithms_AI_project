import google.genai as genai
from google.genai.errors import APIError

def check_api_key_validity(api_key: str) -> bool:
    try:
        # Initialize the client with the provided API key
        client = genai.Client(api_key=api_key)
        # Make a simple, low-cost call (List Models)
        client.models.list()
        return True
    
    except APIError as e:
        # Handle specific API errors

        # error_message = str(e).lower()
    
        # if "unauthenticated" in error_message or "invalid api key" in error_message:
        #     print("   -> Reason: The key is likely **invalid, expired, or malformed**.")
        # elif "insufficient permission" in error_message or "billing" in error_message:
        #     print("   -> Reason: The key is valid but the linked project may have **insufficient permissions or billing is not enabled**.")
        # else:
        #     print(f"   -> Reason: Unidentified API error: {e}")
        return False
    
    except Exception as e:
        # Handle general exceptions (e.g., network issues)
        return False