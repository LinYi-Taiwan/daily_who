import os
import openai
import pandas as pd
from openai.embeddings_utils import get_embedding, cosine_similarity
from dotenv import load_dotenv
import requests

env_path = '.env'
load_dotenv(dotenv_path=env_path)
openai.api_key = os.environ['OPENAI_KEY']
model = os.environ['OPENAI_MODEL']
vector_github_gist = os.environ['VECTOR_GITHUB_GIST']


class ChatGPT:
    def __init__(self, pkl_path = ''):
        self.max_tokens = 500,
        self.temperature = 0.3,
        self.model = model
        self.messages = []
        self.database = pkl_path

    def get_text_embedding(self, text):
        embedding = get_embedding(text, engine="text-embedding-ada-002")
        return embedding

    def get_similarity(self, search_text):
        search_text_embedding = self.get_text_embedding(search_text)
        response = requests.get(vector_github_gist)
        res = response.json()
        gist = pd.DataFrame(res)

        gist['similarity'] = gist['summary_vector'].apply(
            lambda x: cosine_similarity(x, search_text_embedding))
        gist = gist.sort_values(
            by='similarity', ascending=False)
        result = gist.head(1)['summary'].values[0]
        return result


    def get_response(self, msg):
        response = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=500,
            temperature=0.7,
            messages=[
                {"role": "system", "content": "你是一個摘要高手，摘要以下內容"},
                {"role": "user", "content": msg},
            ]
        )
        result = response.choices[0].message.content
        return result