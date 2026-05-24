import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

class LoadBlock:
    def run(self, df):
        engine = create_engine(os.getenv("DATABASE_URL"))
        df.to_sql("posts", engine, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into posts table")