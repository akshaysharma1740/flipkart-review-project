from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    device=0  
)

def predict_sentiments(reviews):
    if not reviews:
        return []
    results = sentiment_pipeline(reviews)
    return [{"label": r["label"], "score": round(r["score"], 3)} for r in results]
