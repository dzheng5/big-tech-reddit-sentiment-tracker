import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_results(question, sql, columns, rows):
    rows_text = "\n".join([str(dict(zip(columns, row))) for row in rows])
    
    prompt = f"""
You are a data analyst explaining query results to a non-technical user.

The user asked: {question}
The SQL query run was: {sql}
The results were:
{rows_text}

Write a clear, concise 2-3 sentence explanation of what the results mean.
Focus on the insight, not the technical details.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()