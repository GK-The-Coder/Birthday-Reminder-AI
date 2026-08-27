import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY must be configured")

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

llm = ChatGroq(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY
)


def generate_birthday_message(name, sender_name=None):
    sender_name = sender_name or os.getenv("SENDER_NAME", "Your friend")

    prompt = f"""
Write a warm and personal birthday wish for {name}, from {sender_name}.

Requirements:
- Maximum 80 words
- Positive tone
- Friendly and heartfelt
- Mention the sender naturally when appropriate
- Include one short, natural mention of WishMate as the app helping send this wish
- Do not use sales language or make the message feel like an advertisement
- Sign the message exactly as:

With warm wishes,
{sender_name}
"""

    response = llm.invoke(prompt)

    return response.content