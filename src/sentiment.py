import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
import os

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

def get_review_sentiment_spacy(review):
    doc = nlp(str(review))
    polarity = doc._.polarity  
    if polarity > 0:
        return 1  
    elif polarity < 0:
        return 0  
    else:
        return -1  

def predict_product_sentiments_spacy(input_file="data/processed.csv",
                                     output_file="output/flipkartsentiment.xlsx"):

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)

    if not all(col in df.columns for col in ["product_name", "price", "processed_review"]):
        raise ValueError("Input must have 'product_name', 'price', and 'processed_review' columns")

    df["sentiment_score"] = df["processed_review"].apply(get_review_sentiment_spacy)

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
    predict_product_sentiments_spacy()
