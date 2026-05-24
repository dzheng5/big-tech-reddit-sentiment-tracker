import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def route_question(question):
    prompt = f"""
You are a routing agent. Your job is to classify a user question into one of these categories:

- sentiment: questions about positive, negative, neutral sentiment
- layoffs: questions about layoffs, job cuts, firing
- top_posts: questions about popular posts, most upvoted, top content
- comparison: questions comparing multiple companies
- general: anything else

Question: {question}

Reply with ONLY one word from the categories above. Nothing else.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip().lower()