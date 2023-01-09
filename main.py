from flask import Flask
import os
import openai
from chat_gpt.chat_gpt_controller import chat_gpt_route_path, chat_gpt_route
from dotenv import load_dotenv
load_dotenv() # load .env file

openai.api_key = os.getenv('OPENAI_API_KEY')

def bootstrap():
    # create and configure the app
    app = Flask(__name__)
    # register the modules / blueprints 
    app.register_blueprint(chat_gpt_route, url_prefix=f'/{chat_gpt_route_path}')
    # start the app
    app.run(port=3000, debug=True)

if __name__ == '__main__':
    bootstrap()