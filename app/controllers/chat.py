from app.tools import cancel_order, view_product_details, search_products, add_to_cart
from app.prompts.prompttemplate import main_qa_prompt
from app.models.db_helpers import insert_chat_history, get_chat_history
from vertexai.generative_models import Tool, GenerativeModel, GenerationConfig, Part
import logging.config

logger = logging.getLogger(__name__)  # get a logger instance

retail_tool = Tool(
    function_declarations=[
        search_products,
        view_product_details,
        add_to_cart,
        cancel_order
    ],
)

model = GenerativeModel(
    "gemini-1.0-pro-001",
    generation_config=GenerationConfig(temperature=0),
    tools=[retail_tool]
)


def handle_function_calling(api_response, chat):
    try:
        function_name = api_response.function_call.name
        
        # TODO: Use when params is dynamic
        params = {key: value for key, value in api_response.function_call.args.items()}

        api_response_new = None

        if function_name == "search_products":
            api_response_new = {"sku": "GA04855-AU","in_stock": "yes","details": "The price of PS5 is 73 dollars"}
        elif function_name == "add_to_cart":
            api_response_new = {"status": "Success", "message": "The order was added successfully to your cart"}
        elif function_name == "view_product_details":
            api_response_new = [{"sku": "GA04855-AU", "in_stock": "yes", "details" : "The price of PS5 is 73 dollars"},{"sku": "GA04834-US", "in_stock": "yes", "details" : "The price of Shiny Leather Boots is 80 dollars"}]
        elif function_name == "cancel_order":
            api_response_new = {"status": "Success", "message": "The order has been successfully cancelled"}

        if api_response_new:
            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"content": api_response_new},
                ),
            )
            api_response = response.candidates[0].content.parts[0]
         
        if hasattr(api_response, "text"):
            return api_response, False
        else:
            return api_response, True

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, False
        
def chat_agent(params):
    chat = model.start_chat()
    resp = None
    prompt = params["input"]
    user_id = params["user_id"]
    user_phone = params["user_phone"]

    chat_history = get_chat_history(chat, user_id)    
    
    # Append chat_history to chat.history if is not empty
    if len(chat_history) > 0:
        chat.history.extend(chat_history)
    chat_history_len = len(chat.history)

    response = chat.send_message(prompt)
    api_response = response.candidates[0].content.parts[0]
    
    if hasattr(api_response, "text"):
        print(f"Response: {api_response.text}")
        resp = api_response.text
    else:
        while True:
            api_response, is_function_call = handle_function_calling(api_response, chat)
            if api_response:
                resp = api_response.text
            if not is_function_call:
                break
    
    recent_chat_history = chat.history[chat_history_len:]
    insert_chat_history(user_id, user_phone, recent_chat_history)
    return {
        "response": resp,
        "chat_history": [type(content).to_dict(content) for content in chat.history],
    }