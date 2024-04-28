# app/controllers.py
from app.models.models import convo_collection, user_collection
import logging

logger = logging.getLogger(__name__)  # get a logger instance


def create_conversation_helper(user_phone, source):
    convo_collection.update_many(
        {"user_phone": user_phone, "latest": True},  # Query to find documents
        {"$set": {"latest": False}}  # Update action
    )
    conversation = convo_collection.insert_one({"user_phone": user_phone, "latest" : True, "source" : source})
    return conversation

