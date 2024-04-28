# app/helpers.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)  # get a logger instance

def handle_response(data, status_code=200):
    """Handle standard responses for the application."""
    return {
        "data": data,
        "status": status_code
    }

def extract_user_chat_data(chat_history):
    extracted_data = []
    for entry in chat_history:
        role = entry.role
        parts = entry.parts
        timestamp = datetime.now()
        for part in parts:
            if hasattr(part, 'text'):
                text = part.text
                extracted_data.append((role, text, timestamp))
    return extracted_data