from dataclasses import dataclass

@dataclass
class MessageRequestDTO:
    question: str 

    @staticmethod
    def new_instance_from_flask_body(data: dict) -> 'MessageRequestDTO':
        if 'question' not in data:
            raise Exception('question attribute not found in chat_gpt_model.py: MessageRequestDTO.new_instance_from_flask_body')
        
        return MessageRequestDTO(question = data['question'])
