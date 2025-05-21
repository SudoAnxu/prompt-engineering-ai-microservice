import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_responses(query: str):
    casual_prompt = f"Explain this like you're talking to a friend: {query}"
    formal_prompt = f"Write a formal and academic explanation of: {query}"
    casual_resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[
        {"role": "system", "content": casual_prompt},
        {"role": "user", "content": query}
        ],
        temperature=0.7,
        max_completion_tokens=256
    )
    formal_resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
        {"role": "system", "content": formal_prompt},
        {"role": "user", "content": query}
        ],
        temperature=0.7,
        max_completion_tokens=256
    )
    return casual_resp.choices[0].message.content, formal_resp.choices[0].message.content
