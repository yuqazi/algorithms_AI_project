from google import genai
from dotenv import load_dotenv
from logging_system import get_logger
import os

logger = get_logger(__name__)

import globalvalues as gv

# Global persistent client and chat
client = None
chat = None

def start_gemini():
    global client, chat

    if(gv.KEY != ""):
        client = genai.Client(api_key=gv.KEY)
        chat = client.chats.create(model="gemini-2.5-flash")
        logger.info("Gemini client and chat session initialized successfully.")
        return client, chat
    else:
        load_dotenv(override=True)
        client = genai.Client()
        chat = client.chats.create(model="gemini-2.5-flash")
        logger.info("Gemini client and chat session initialized successfully.")
        return client, chat


def gemini_response(userquestion, initialmessage=None):
    global chat

    if chat is None:
        raise RuntimeError("Chat has not been initialized. Call start_gemini() first.")

    # Optional system/initial message
    if initialmessage:
        chat.send_message(initialmessage)

    # User message
    response = chat.send_message(userquestion)

    logger.info("Received response from Gemini AI.")

    return response.text