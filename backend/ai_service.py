import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_birthday_message(name):

    prompt = f"""
Write a warm and friendly birthday wish for {name}.

Requirements:
- Maximum 80 words
- Positive tone
- Professional but friendly
- End with:

GK-The-Coder
"""

    response = llm.invoke(prompt)

    return response.content