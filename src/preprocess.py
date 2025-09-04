import os
import re
import unicodedata
import pandas as pd

def clean_text(text: str) -> str:
    """Normalize text and remove HTML tags and extra spaces."""
    text = unicodedata.normalize("NFKC", text)  
    text = re.sub(r"<.*?>", " ", text)          
    text = re.sub(r"\s+", " ", text).strip()    
    return text

def preprocess_reviews(input_file="data/reviews.xlsx", output_file="data/processed.csv"):
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_excel(input_file)

    if "review_text" not in df.columns:
        raise ValueError("Excel file must contain a 'review_text' column")

    df["processed_review"] = df["review_text"].astype(str).apply(clean_text)

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"✅ Processed {len(df)} reviews and saved to {output_file}")
    return df

if __name__ == "__main__":
    preprocess_reviews()
