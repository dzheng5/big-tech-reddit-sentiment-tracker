import pandas as pd

class IngestBlock:
    def run(self):
        df = pd.read_csv("data/data.csv")
        return df