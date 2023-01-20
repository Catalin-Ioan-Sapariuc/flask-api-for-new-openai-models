import os, openai
from chat_gpt.chat_gpt_model import MessageRequestDTO 

openai.organization =os.getenv('ORGANIZATION_ID')
openai.api_key=os.getenv('OPENAI_API_KEY')

# defaullt davinci model
DEFAULT_MODEL = "text-davinci-003"
DEFAULT_TEMPERATURE =0.2
DEFAULT_MAX_TOKENS = 512

class ChatGptService:
    @classmethod
    def get_ai_response(cls, data:MessageRequestDTO):
        return openai.Completion.create(prompt=data.question, model=DEFAULT_MODEL,
                        temperature=DEFAULT_TEMPERATURE, max_tokens=DEFAULT_MAX_TOKENS)