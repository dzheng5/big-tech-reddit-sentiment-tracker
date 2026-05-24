import pandas as pd

class TransformBlock:
    def run(self, df):
        df = df.drop(columns=["tag"])
        df = df.drop_duplicates()
        df = df.dropna(subset=["title", "text"])
        return df