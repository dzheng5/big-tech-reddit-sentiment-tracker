import pandas as pd

class ValidateBlock:
    def run(self, df):
        df = df.dropna(subset=["title", "company", "sentiment"])
        df = df.drop_duplicates(subset=["title"])
        print(f"Rows after validation: {len(df)}")
        return df