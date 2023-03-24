''' 
Having a knowledge database of prompts, completions and embeddings of prompts.
a query and a number (n) of most similar prompts (with the query) from the knowledge database, 
create  new acc_prompt made of the similar (prompt, completion) pairs and the query. 
Retun the acc_prompt from the acc_prompt function to be fed to the ai model to generate the answer.

Ioan Sapariuc
Feb 2023
''' 
import tiktoken
import pickle5 as pickle
import openai
import pandas as pd
import numpy as np

#embedding_engine = "text-similarity-davinci-001"
embedding_engine = "text-embedding-ada-002" 

def text_embed(text: str) -> str:
    response = openai.Embedding.create(input=text,engine=embedding_engine)
    curated_response = response.data[0]["embedding"]
    return curated_response

def cosine_similarity(A,B):
    return np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

#df = pd.read_pickle('/data/blueprint-primer-general-and-specific-embeddings-with-tokens.pkl')
df = pd.read_pickle('data/blueprint-primer-embeddings-with-tokens-mac.pkl')

#print(df.head(3))
#print(type(df['prompt_embedding'][0]))
#query = "What is blueprint?"
#query = '''Using the blueprint tools, write steps to create an e-shopping ai, 
#with collections of users,
#products, shopping events and users balance, and with relations between these.'''
def enrich_query(query, max_tokens, MAX_ALLOWED_TOKENS):
    query_embed = text_embed(query)

    df['query_similarity']=df.apply(lambda x: cosine_similarity(x['prompt_embedding'], query_embed), axis=1)

    dfs = df.sort_values(by='query_similarity',ascending=False)

    task = '''Learn about blueprint: '''
    actual_prompt = []
    tokens = num_tokens_from_string(task+query, encoding_name="p50k_base")
    #for i in range(n):
    #    actual_prompt += 'input: '+ dfs['prompt'][i]+ ' output: ' + dfs['completion'][i]+' '
    # actual_prompt += 'input: ' + query + ' output: '

    #print(len(actual_prompt))
    n = 0

    while True: 
        if (tokens +dfs.iloc[n]['prompt_and_completion_tokens'] < MAX_ALLOWED_TOKENS - 100 - max_tokens):
            actual_prompt.append({"role": "user", "content": df.iloc[n]['prompt']})
            actual_prompt.append({"role" : "assistant", "content": df.iloc[n]['completion']})
            tokens += dfs.iloc[n]['prompt_and_completion_tokens']
            n += 1
        else:
            break

    print('add_spec_training_data: enrich_query: we added ', n, ' (prompts, completions), \
           where prompts are the most similar to the actual prompt')
    print('add_spec_training_data: enrich_query: the number of tokens in the actual prompt is: ', tokens)

    actual_prompt.append({"role": "user", "content": query})
    actual_prompt.append({"role": "assistant", "content": ""})

    print('add_spec_training_data: enrich_query: The first 200 characters of the actual prompt are: \n')
    print(actual_prompt[:6])
    print('add_spec_training_data: enrich_query: The last 100 characters of the actual prompt are: \n')
    print(actual_prompt[-6:])
    
    return actual_prompt

