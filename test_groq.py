import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
try:
    print('Testing...')
    response = client.chat.completions.create(
        model='openai/gpt-oss-120b',
        messages=[{'role':'user', 'content':'Output strictly as a JSON object matching this schema: {"type":"object"}'}],
        response_format={'type': 'json_object'}
    )
    print(response.choices[0].message.content)
except Exception as e:
    print('Exact Error:', type(e), e)
