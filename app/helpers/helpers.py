# app/helpers.py
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)  # get a logger instance

def handle_response(data, status_code=200):
    """Handle standard responses for the application."""
    return {
        "data": data,
        "status": status_code
    }

def extract_chat_history(chat_history, conv_id, user_id):
    print(f"Chat History: {chat_history}")
    history = []
    for content in chat_history:
        # print(content.role, "->", [type(part).to_dict(part) for part in content.parts])
        history.append({
            "role" : content.role,
            "parts" : type(content.parts[0]).to_dict(content.parts[0]),
            "user_id": user_id,
            "convo_id": conv_id,
            "timestamp": datetime.now()
        })
    return history