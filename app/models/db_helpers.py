from datetime import datetime
from app.models.models import conversation_collection, message_collection
from app.helpers.helpers import extract_user_chat_data

def insert_or_get_conversation(user_id, user_ph_number):
    existing_conversation = conversation_collection.find_one({'user_id': user_id})
    
    if existing_conversation:
        return str(existing_conversation['_id'])
    else:
        conversation = {
            'user_id': user_id,
            'time': datetime.now(),
            'user_ph_number': user_ph_number
        }
        try:
            result = conversation_collection.insert_one(conversation)
            return str(result.inserted_id)
        except Exception as e:
            return str(e)


def insert_chat_history(user_id, user_ph_number, chat_history):
    conv_id = insert_or_get_conversation(user_id, user_ph_number)
    extracted_data = extract_user_chat_data(chat_history)    
    
    for role, text, timestamp in extracted_data:
        existing_message = message_collection.find_one({
            'role': role,
            'text': text,
            'conv_id': conv_id,
            'user_id': user_id,
            'timestamp': timestamp
        })

        if not existing_message:
            message = {
                'role': role,
                'text': text,
                'conv_id': conv_id,
                'user_id': user_id,
                'timestamp': timestamp
            }
            try:
                result = message_collection.insert_one(message)
                print(f"Inserted message: {result.inserted_id}")
            except Exception as e:
                print(f"Error inserting message: {str(e)}")

def get_chat_history(user_id):
    messages = message_collection.find({'user_id': user_id}).sort('timestamp', 1)
    chat_history = [(msg['role'], msg['text'], msg['timestamp']) for msg in messages]
    return chat_history