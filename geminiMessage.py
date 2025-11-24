from google import genai
from dotenv import load_dotenv
import os

# Global persistent client and chat
client = None
chat = None

def start_gemini():
    global client, chat

    load_dotenv()

    # Create persistent client ONLY ONCE
    client = genai.Client()

    # Create persistent chat session ONLY ONCE
    chat = client.chats.create(model="gemini-2.5-flash")

    return client, chat


def gemini_response(userquestion, initialmessage=None):
    """
    Sends a message to an EXISTING persistent chat session.
    Keeps history. Does NOT recreate the chat.
    """

    global chat

    if chat is None:
        raise RuntimeError("Chat has not been initialized. Call start_gemini() first.")

    # Optional system/initial message
    if initialmessage:
        chat.send_message(initialmessage)

    # User message
    response = chat.send_message(userquestion)

    return response.text
