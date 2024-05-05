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
    input = request.json.get("input")
    user_id = request.json.get("user_id")
    user_phone = request.json.get("user_phone")

    params = {
        "input": input,
        "user_id": user_id,
        "user_phone" : user_phone
    }
        
    agent_response = chat_agent(params=params)
    return agent_response
    