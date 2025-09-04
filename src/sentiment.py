from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import os

def load_model(model_name="roberta-base"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

def get_review_sentiment_hf(review, tokenizer, model):
    inputs = tokenizer(str(review), return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    return pred

def predict_product_sentiments_hf(input_file="data/processed.csv",
                                  output_file="output/flipkartsentiment.xlsx",
                                  model_name="roberta-base"):

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)

    if not all(col in df.columns for col in ["product_name", "price", "processed_review"]):
        raise ValueError("Input must have 'product_name', 'price', and 'processed_review' columns")

    tokenizer, model = load_model(model_name)

    df["sentiment_score"] = df["processed_review"].apply(lambda x: get_review_sentiment_hf(x, tokenizer, model))

    product_sentiments = []
    for product, group in df.groupby(["product_name", "price"]):
        pos_count = sum(group["sentiment_score"] == 1)
        neg_count = sum(group["sentiment_score"] == 0)

        if pos_count > neg_count:
            overall_sentiment = "buy product"
        elif neg_count > pos_count:
            overall_sentiment = "don't buy product"
        else:
            overall_sentiment = "customer's choice"

        product_sentiments.append({
            "product_name": product[0],
            "price": product[1],
            "sentiment": overall_sentiment
        })

    result_df = pd.DataFrame(product_sentiments)

    os.makedirs("output", exist_ok=True)
    result_df.to_excel(output_file, index=False)
    print(f"✅ Sentiment results saved to {output_file}")

    return result_df

if __name__ == "__main__":
    predict_product_sentiments_hf()
