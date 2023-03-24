from flask import Flask, json, request, render_template
import openai, os
#from flask_cors import CORS, cross_origin
from add_specific_train_data_to_query import enrich_query

openai.api_key = os.getenv('OPENAI_API_KEY')

MODELS = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301"]
TEMPERATURES =["0.","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1."]
TOKENS = ["100", "200", "400", "600", "800", "1000"]
#MODEL_TYPE = ["old_model","new_model"]

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html', models = MODELS, temperatures = TEMPERATURES, 
                           tokens=TOKENS)
        #return redirect(url_for('/chat-gpt-ai/message/'))

@app.route('/answer',methods=['GET','POST'])
def get_ai_model_answer(): 
    if request.method == "POST": 
        prompt = request.form.get("prompt")
        model = request.form.get("model")
        temperature = float(request.form.get("temperature"))
        max_tokens = int(request.form.get("token"))

        MAX_ALLOWED_TOKENS = 4000

        print("prompt = \n", prompt)
        #op_p = 1.
        #presence_penalty = 1.
        actual_prompt = enrich_query(prompt, max_tokens, MAX_ALLOWED_TOKENS)
        response =openai.ChatCompletion.create(model = model, messages = actual_prompt, max_tokens=max_tokens,
                                           temperature=temperature) 
        # n=1, stop=['\n\ninput:'])
        hresponse=response['choices'][0]['message']['content']
        print("hresponse = \n", hresponse)
        return render_template('answer.html', prompt=prompt, response=hresponse)
    else:
        return render_template("index.html")        
