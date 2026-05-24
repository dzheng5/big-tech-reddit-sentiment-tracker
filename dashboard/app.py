import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import base64
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.orchestrator import run

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

engine = create_engine(os.getenv("DATABASE_URL"))

COMPANIES = {
    "Google": "assets/google.png",
    "Apple": "assets/apple.png",
    "Microsoft": "assets/microsoft.png",
    "Meta": "assets/meta.png",
    "Amazon": "assets/amazon.png",
    "Nvidia": "assets/nvidia.png",
    "Tesla": "assets/tesla.png",
    "TSMC": "assets/tsmc.png",
    "Broadcom": "assets/broadcom.png",
    "Tencent": "assets/tencent.png"
}

st.set_page_config(page_title="Big Tech Reddit Sentiment Tracker", layout="wide")


st.title("Big Tech Reddit Sentiment Tracker")
st.caption("What is Reddit saying about Big Tech Companies?")
st.caption("Data spans June 2023 to April 2025 · Source: r/technology")

st.subheader("Companies")

cols = st.columns(5)

for i, (company, logo) in enumerate(COMPANIES.items()):
    with cols[i % 5]:
        if st.button(company, key=company, use_container_width=True):
            st.session_state.selected = company
        st.markdown(f"""
            <div style="
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 16px;
                text-align: center;
                background: white;
                height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-top: -50px;
                pointer-events: none;
            ">
                <img src="data:image/png;base64,{get_image_base64(logo)}" width="50" style="margin-bottom:8px;">
                <div style="font-weight:600; font-size:14px; color:#333;">{company}</div>
            </div>
        """, unsafe_allow_html=True)

if "selected" in st.session_state:
    company = st.session_state.selected

    st.divider()

    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        st.image(COMPANIES[company], width=50)
    with col_title:
        st.subheader(company)

    layoff_df = pd.read_sql(f"""
        SELECT total_posts, layoff_posts
        FROM layoffs_by_company
        WHERE company = '{company}'
    """, engine)

    total = layoff_df["total_posts"].values[0]
    layoffs = layoff_df["layoff_posts"].values[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Posts", total)
    col2.metric("Layoff Mentions", layoffs)
    col3.metric("Layoff %", f"{round(layoffs/total*100, 1)}%")

    st.subheader("Sentiment analysis")
    chart_col1, chart_col2 = st.columns([2, 1])

    sentiment_time_df = pd.read_sql(f"""
        SELECT date, sentiment, post_count
        FROM sentiment_over_time
        WHERE company = '{company}'
        ORDER BY date
    """, engine)

    pivot_df = sentiment_time_df.pivot(index="date", columns="sentiment", values="post_count").fillna(0)

    with chart_col1:
        st.caption("Sentiment over time")
        st.line_chart(pivot_df, color=["#FF4444", "#888888", "#22CC66"])

    with chart_col2:
        st.caption("Sentiment breakdown")
        sentiment_df = pd.read_sql(f"""
            SELECT INITCAP(sentiment) as sentiment, post_count
            FROM sentiment_by_company
            WHERE company = '{company}'
        """, engine)
        fig_data = sentiment_df.set_index("sentiment")
        import plotly.express as px
        fig = px.pie(sentiment_df, values="post_count", names="sentiment",
             color="sentiment",
             color_discrete_map={"Negative": "#FF4444", "Neutral": "#888888", "Positive": "#22CC66"},
             height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top posts")
    df = pd.read_sql(f"""
        SELECT title, url, INITCAP(sentiment) as sentiment, score, DATE(datetime) as datetime
        FROM posts
        WHERE company = '{company}'
        ORDER BY score DESC
        LIMIT 50
    """, engine)
    df.columns = ["Title", "URL", "Sentiment", "Upvotes", "Date"]
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "URL": st.column_config.LinkColumn("URL"),
        }
    )

st.divider()
st.subheader("Ask a question")
st.caption("Ask anything about the data in plain English")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sql" in message:
            with st.expander("See SQL query"):
                st.code(message["sql"], language="sql")
        if "data" in message:
            st.dataframe(pd.DataFrame(message["data"]["rows"], columns=message["data"]["columns"]), use_container_width=True)

if question := st.chat_input("e.g. Which company had the most negative posts?"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = run(question)
        st.markdown(result["explanation"])
        with st.expander("See SQL query"):
            st.code(result["sql"], language="sql")
        if result["rows"]:
            st.dataframe(pd.DataFrame(result["rows"], columns=result["columns"]), use_container_width=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["explanation"],
        "sql": result["sql"],
        "data": {"rows": [list(r) for r in result["rows"]], "columns": result["columns"]}
    })