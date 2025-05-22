# prompt_engineering.py
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


_api_key = os.getenv("GROQ_API_KEY")
if not _api_key:
    raise RuntimeError("GROQ_API_KEY is not set")
_client = Groq(api_key=_api_key)

def generate_responses(query: str):
    casual_prompt = f"Explain this like you're talking to a friend: {query}"
    formal_prompt = f"Write a formal and academic explanation of: {query}"

    casual_resp = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": casual_prompt},
            {"role": "user",   "content": query},
        ],
        temperature=0.7,
        max_completion_tokens=256,
    )
    formal_resp = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": formal_prompt},
            {"role": "user",   "content": query},
        ],
        temperature=0.7,
        max_completion_tokens=256,
    )

    return (
        casual_resp.choices[0].message.content,
        formal_resp.choices[0].message.content,
    )
