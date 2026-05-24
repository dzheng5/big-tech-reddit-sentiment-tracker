import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from agent.router_agent import route_question
from agent.sql_agent import generate_sql
from agent.explainer_agent import explain_results

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

def run(question):
    route = route_question(question)
    sql = generate_sql(question, route)
    
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = list(result.keys())
    
    explanation = explain_results(question, sql, columns, rows)
    
    return {
        "route": route,
        "sql": sql,
        "columns": columns,
        "rows": rows,
        "explanation": explanation
    }