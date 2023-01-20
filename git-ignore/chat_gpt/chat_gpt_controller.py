from flask import Blueprint, jsonify
from flask import Flask, json, request
import requests
from chat_gpt.chat_gpt_service import ChatGptService
from chat_gpt.chat_gpt_model import MessageRequestDTO

#chat_gpt_route_path ='chat-gpt-ai'
#chat_gpt_route=Blueprint('chat-gpt-ai',__name__)
app = Flask(__name__)

@app.route('/chat-gpt-ai/message',methods=['POST','GET'])
def get_ai_model_answer():
    body = request.json()
    #data = {"question": "Hello! What is your name?"}
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #body =requests.post('http://localhost:3000/chat-gpt-ai/message', headers = headers, json={})
    #json = {"question": "Hello! What is your name?"}
    #body = json
    return jsonify({ 'result':
        ChatGptService.get_ai_response(MessageRequestDTO.new_instance_from_flask_body(body))})