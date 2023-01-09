from flask import Blueprint, jsonify
from flask import request
from chat_gpt.chat_gpt_service import ChatGptService
from chat_gpt.chat_gpt_model import MessageRequestDTO

chat_gpt_route_path ='chat-gpt-ai'
chat_gpt_route=Blueprint('chat_gpt_route_path',__name__)

@chat_gpt_route.route('/message',methods=['POST','GET'])

def get_ai_model_answer():
    body = request.form['message']
    return jsonify({ 'result':
        ChatGptService.get_ai_response(MessageRequestDTO.new_instance_from_flask_body(body))})