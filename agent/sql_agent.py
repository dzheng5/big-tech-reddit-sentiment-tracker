import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SCHEMA = """
Tables:
- posts: title, url, sentiment, score, datetime, company, is_layoff, is_product, is_earnings
- sentiment_by_company: company, sentiment, post_count
- sentiment_over_time: company, date, sentiment, post_count
- layoffs_by_company: company, total_posts, layoff_posts

Sentiment values are: positive, negative, neutral (lowercase)
Companies: Google, Apple, Microsoft, Meta, Amazon, Nvidia, Tesla, TSMC, Broadcom, Tencent
Date range: June 2023 to April 2025
"""

def generate_sql(question, route):
    prompt = f"""
You are a SQL expert working with a Reddit analytics database.

Schema:
{SCHEMA}

The question is about: {route}
Question: {question}

Rules:
- Write a single clean SELECT query
- Never use UNION or UNION ALL
- Only query one table at a time
- Use materialized views when possible for aggregated data
- Never use SELECT *

Return ONLY the SQL query, nothing else. No explanation, no markdown, no backticks.
"""

