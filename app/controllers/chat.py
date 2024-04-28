from app.tools import cancel_order, view_product_details, search_products, recommend_orders, add_to_cart
from app.prompts.prompttemplate import main_qa_prompt
from app.models.db_helpers import insert_or_get_conversation, insert_message
from app.helpers.helpers import extract_user_chat_data
from vertexai.generative_models import Tool, GenerativeModel, GenerationConfig, Part

retail_tool = Tool(
    function_declarations=[
        cancel_order,
        add_to_cart,
        view_product_details,
        search_products,
        recommend_orders,
    ],
)

model = GenerativeModel(
    "gemini-1.0-pro-001",
    generation_config=GenerationConfig(temperature=0),
    tools=[retail_tool]
)

chat = model.start_chat()

def handle_function_calling(api_response):
    try:
        function_name = api_response.function_call.name
        params = {key: value for key, value in api_response.function_call.args.items()}

        print(f"Function called: {function_name}")
        print(f"Parameters: {params}")

        api_response_new = None

        if function_name == "search_products":
            api_response_new = {
                "sku": "GA04834-US",
                "in_stock": "yes",
                "details": "The price of PS5 is 73 dollars"
            }
        elif function_name == "add_to_cart":
            api_response_new = {"status": "Success", "message": "The order was added successfully to your cart"}

        if api_response_new:
            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"content": api_response_new},
                ),
            )
            api_response = response.candidates[0].content.parts[0]
            
        if hasattr(api_response, "text"):
            print("Final Response")
            return api_response, False
        else:
            print("Additional function call required")
            return api_response, True

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, False
        
def chat_agent(params):
    user_id = "1234"
    user_phone = "555-1234"
    conv_id = insert_or_get_conversation(user_id, user_phone)
    # message_id = insert_message('user', 'Hello, this is a test message.', conv_id, user_id)
    print(f"Conversation ID: {conv_id}")
    
    prompt = params["input"]
    response = chat.send_message(prompt)
    api_response = response.candidates[0].content.parts[0]
    resp = ""

    if hasattr(api_response, "text"):
        print(f"Response: {api_response.text}")
        resp = api_response.text
    else:
        while True:
            api_response, is_function_call = handle_function_calling(api_response)
            if api_response:
                resp = api_response.text
            if not is_function_call:
                break

    print(f"Chat history: {extract_user_chat_data(chat_history=chat.history)}")
    
    return resp