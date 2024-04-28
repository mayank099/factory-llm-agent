# app/models.py
from app import mongo

convo_collection = mongo.yaxis["convo_collection"]
user_collection = mongo.yaxis["users"]
messages_collection = mongo.yaxis["messages"]
conversation_collection = mongo.shoppingcart['conversation']
message_collection = mongo.shoppingcart['message']