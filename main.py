from flask import Flask, json, request, jsonify, render_template, redirect, url_for
import openai, os
from dotenv import load_dotenv

load_dotenv() # load .env file

openai.api_key = os.getenv('OPENAI_API_KEY')


if __name__ == '__main__':
    #bootstrap()
    app = Flask(__name__)

    @app.route('/chat-gpt-ai/', methods = ['GET', 'POST'])
    def index():
        return render_template('mainpage.html')
        #return redirect(url_for('/chat-gpt-ai/message/'))
    @app.route('/chat-gpt-ai/message/',methods=['POST','GET'])
    def get_ai_model_answer():
        prompt = request.args.get("prompt")
        #prompt = request.json # this is the prompt from the user, this works in postman but not in the browser
        #prompt=prompt['prompt']
        #prompt='Who is the president of the United States?'
        print(prompt)
        engine="davinci"
        max_tokens=50
        temperature=0.
        top_p=0
        presence_penalty=1
        response =openai.Completion.create(engine=engine,prompt=prompt,max_tokens=max_tokens,
                                            temperature=temperature,top_p=top_p,
                                            presence_penalty=presence_penalty,n=1,
                                            stream=False)
        offset=0
        hresponse=response['choices'][0]['text'][offset:]
        #return render_template('answer.html')
        return jsonify({'text': hresponse})
        #else:
        #    return render_template_string('<h1> The request on this page should be GET. </h1>')
    #start the app  
    app.run(port=3000, debug=True)