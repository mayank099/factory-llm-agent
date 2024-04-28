from datetime import datetime
from app.models.models import conversation_collection, message_collection

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


def insert_message(role, text, conv_id, user_id):
    message = {
        'role': role,
        'text': text,
        'conv_id': conv_id,
        'user_id': user_id
    }
    try:
        result = message_collection.insert_one(message)
        return str(result.inserted_id)
    except Exception as e:
        return str(e)
