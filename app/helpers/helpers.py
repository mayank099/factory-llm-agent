# app/helpers.py
import logging

logger = logging.getLogger(__name__)  # get a logger instance

def handle_response(data, status_code=200):
    """Handle standard responses for the application."""
    return {
        "data": data,
        "status": status_code
    }
