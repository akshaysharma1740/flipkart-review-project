import os
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text_nlp(text: str) -> str:
    doc = nlp(str(text))
    tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_space:
            tokens.append(token.lemma_.lower())
    return " ".join(tokens) 

def preprocess_reviews_nlp(input_file="data/reviews.xlsx", output_file="data/processed.csv"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_excel(input_file)

    if "review_text" not in df.columns:
        raise ValueError("Excel file must contain a 'review_text' column")

    df["processed_review"] = df["review_text"].astype(str).apply(clean_text_nlp)

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"✅ Processed {len(df)} reviews with NLP and saved to {output_file}")
    return df

if __name__ == "__main__":
    preprocess_reviews_nlp()
