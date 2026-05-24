import pandas as pd
from transformers import pipeline

COMPANIES = {
    "Nvidia": ["nvidia", "nvda"],
    "Google": ["google", "alphabet", "googl"],
    "Microsoft": ["microsoft", "msft", "azure"],
    "Apple": ["apple", "aapl", "iphone"],
    "Amazon": ["amazon", "amzn", "aws"],
    "TSMC": ["tsmc", "taiwan semiconductor"],
    "Broadcom": ["broadcom", "avgo"],
    "Meta": ["meta", "facebook", "instagram"],
    "Tesla": ["tesla", "tsla"],
    "Tencent": ["tencent", "tcehy"]
}

sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def detect_company(text):
    if not isinstance(text, str):
        return None
    text = text.lower()
    for company, keywords in COMPANIES.items():
        for keyword in keywords:
            if keyword in text:
                return company
    return None

def detect_sentiment(text):
    if not isinstance(text, str) or len(text) == 0:
        return "neutral"
    try:
        result = sentiment_analyzer(text[:512])
        return result[0]["label"]
    except:
        return "neutral"
    
def detect_topics(text):
    if not isinstance(text, str):
        return False, False, False
    text = text.lower()
    is_layoff = any(word in text for word in ["layoff", "laid off", "job cuts", "firing", "redundancies"])
    is_product = any(word in text for word in ["launch", "release", "product", "feature", "update", "announced"])
    is_earnings = any(word in text for word in ["earnings", "revenue", "profit", "quarterly", "results", "beat"])
    return is_layoff, is_product, is_earnings

class EnrichBlock:
    def run(self, df):
        df["company"] = df["title"].apply(detect_company)
        df = df[df["company"].notna()]
        df["sentiment"] = df["title"].apply(detect_sentiment)
        df[["is_layoff", "is_product", "is_earnings"]] = df["title"].apply(
            lambda x: pd.Series(detect_topics(x))
        )
        return df