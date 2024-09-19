import openai
from config import OPENAI_API_KEY, GPT_MODEL

openai.api_key = OPENAI_API_KEY

async def ask_question(question, role):


    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": question}
        ]
    )
    return(response['choices'][0]['message']['content'])
