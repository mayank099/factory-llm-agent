from app import app
from app.controllers.controllers import create_conversation_helper
from flask import request, jsonify, render_template
import logging
import os
from app.controllers.chat import chat_agent

logger = logging.getLogger(__name__)  # get a logger instance


@app.route('/health-check', methods=['GET'])
def health_check():
    logger.info("Health check")
    return jsonify(success=True, message="Server working fine (-_-)")

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/create_message', methods=['POST'])
def create_message():
    print("Request Received!!")
    input = request.json.get("input")
    # conversation_id = request.json.get("conversation_id")
    # user_id = request.json.get("user_id")
    
    params = {
        "input": input, 
        # "conversation_id": conversation_id,
        # "user_id": user_id
    }
    
    # Print Params with equals to sign
    print("="*80)
    print(params)
    print("="*80)

    
    agent_response = chat_agent(params=params)
    return agent_response

@app.route('/create_conversation', methods=['POST'])
def create_conversation():
    # Extract the data from the request
    data = request.json

    # Retrieve the necessary fields from the POST data
    user_phone = data.get('user_phone')
    source = data.get('source')
    try:
        #conversation = create_conversation_helper(user_phone, source)
        #return jsonify({"convo_id": str(conversation.inserted_id)}), 200
        print("somethingh")
    except Exception as e:
        print(f"Invalid {e}")
        return jsonify({"message": "User saved successfully"}), 200
    
