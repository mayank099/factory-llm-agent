from datetime import datetime
from app.models.models import conversation_collection, message_collection
from app.helpers.helpers import extract_chat_history
from vertexai.generative_models._generative_models import Content
from vertexai.generative_models._generative_models import Part

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
    extracted_history = extract_chat_history(chat_history, conv_id, user_id)        
    try:
        message_collection.insert_many(extracted_history)
    except Exception as e:
        print(f"Error inserting message: {str(e)}")
            

def get_chat_history(chat, user_id):
    chat_history = []
    messages = message_collection.find({'user_id': user_id}).sort('timestamp', 1)
    for message in messages:
        print(f"Message -1 {message['parts']}")
        sys_instruction = None

        parts = message.get('parts', {})
        if 'text' in parts and parts['text'] is not None:
            sys_instruction = Part.from_text(parts['text'])
        elif 'function_response' in parts and parts['function_response'] is not None:
            sys_instruction = Part.from_function_response(name=parts['function_response']['name'], response=parts['function_response']['response'])
        elif 'function_call' in parts and parts['function_call'] is not None:
            sys_instruction = Part.from_dict({"function_call": parts['function_call']})

        if sys_instruction is not None:
            common_msg = Content(role=message['role'], parts=[sys_instruction])
            chat_history.append(common_msg)
        else:
            print(f"Skipping message due to missing valid parts.")
    return chat_history
