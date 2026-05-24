# Big Tech Reddit Sentiment Tracker

A full end-to-end data engineering and AI project that tracks what Reddit is saying about the 10 biggest tech companies in real time.

## What it does

- Ingests Reddit posts from r/technology spanning June 2023 to April 2025
- Runs local AI sentiment analysis (positive, negative, neutral) on each post using HuggingFace
- Detects which company each post is about and flags topic categories (layoffs, product news, earnings)
- Loads enriched data into a cloud PostgreSQL database (Neon)
- Exposes insights through an interactive Streamlit dashboard
- Includes a multi-agent AI query layer that answers plain English questions about the data

## Architecture
CSV Data → IngestBlock → TransformBlock → EnrichBlock → ValidateBlock → LoadBlock → PostgreSQL
↓
Materialized Views
↓
Streamlit Dashboard + AI Agent

## Pipeline blocks

- **IngestBlock** — reads raw data from CSV
- **TransformBlock** — cleans nulls, duplicates, drops unused columns
- **EnrichBlock** — detects company mentions, runs sentiment analysis, flags topics
- **ValidateBlock** — ensures data quality before loading
- **LoadBlock** — writes enriched data to PostgreSQL

## AI agent layer

A multi-agent system built with Groq:
- **Router agent** — classifies the question type
- **SQL agent** — generates a PostgreSQL query from natural language
- **Explainer agent** — explains the results in plain English

## Tech stack

- Python
- PostgreSQL (Neon)
- HuggingFace Transformers
- Streamlit
- Groq (LLM API)
- SQLAlchemy
- Pandas

## Companies tracked

Google, Apple, Microsoft, Meta, Amazon, Nvidia, Tesla, TSMC, Broadcom, Tencent

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies

pip install -r requirements.txt
3. Add your credentials to a `.env` file
DATABASE_URL=your_neon_connection_string
GROQ_API_KEY=your_groq_key
4. Run the pipeline
python pipeline.py
5. Launch the dashboard
streamlit run dashboard/app.py