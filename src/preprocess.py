import os
import re
import unicodedata
import pandas as pd

def clean_text(text: str) -> str:
    """Normalize text and remove HTML tags and extra spaces."""
    text = unicodedata.normalize("NFKC", text)  # normalize unicode
    text = re.sub(r"<.*?>", " ", text)          # remove HTML tags
    text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
    return text

def preprocess_reviews(input_file="data/reviews.xlsx", output_file="data/processed.csv"):
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Read Excel file
    df = pd.read_excel(input_file)

    # Check if review_text column exists
    if "review_text" not in df.columns:
        raise ValueError("Excel file must contain a 'review_text' column")

    # Clean reviews
    df["processed_review"] = df["review_text"].astype(str).apply(clean_text)

    # Save processed data to CSV
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"✅ Processed {len(df)} reviews and saved to {output_file}")
    return df

if __name__ == "__main__":
    preprocess_reviews()
