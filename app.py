import os
import pandas as pd
from src.flipkartscraper import scrape_flipkart_product, init_driver
from src.preprocess import preprocess_reviews
from src.sentiment import predict_sentiments

# --- Paths ---
input_file = "data/flipkartproducts.xlsx"
output_file = "output/flipkart_products_result.xlsx"
os.makedirs("output", exist_ok=True)

# --- Load products ---
df_products = pd.read_excel(input_file)
if "url" not in df_products.columns:
    raise ValueError("Excel must contain a 'url' column.")

# --- Init driver ---
driver = init_driver()
all_data = []

# --- Process each product ---
for idx, row in df_products.iterrows():
    url = row["url"]
    print(f"Processing product {idx+1}: {url}")

    product_info = scrape_flipkart_product(driver, url, max_pages=3)

    if product_info["num_reviews"] > 0:
        clean_reviews = preprocess_reviews(product_info["reviews"])
        sentiments = predict_sentiments(clean_reviews)  

        pos = sentiments.count("positive")
        neg = sentiments.count("negative")
        neu = sentiments.count("neutral")

        # --- Improved summary logic ---
        if pos > (neg + neu):
            summary = "Mostly positive feedback, recommended."
        elif neg > (pos + neu):
            summary = "Mostly negative feedback, not recommended."
        elif neu > (pos + neg):
            summary = "Reviews are mostly neutral."
        else:
            summary = "Mixed reviews, depends on preferences."
    else:
        summary = "No reviews available"

    result = {
        "product_name": product_info["product_name"],
        "price": product_info["price"],
        "num_reviews": product_info["num_reviews"],
        "summary": summary
    }

    all_data.append(result)

# --- Close driver ---
driver.quit()

# --- Save output ---
df_result = pd.DataFrame(all_data)
df_result.to_excel(output_file, index=False)
print(f"✅ Done! Results saved to {output_file}")
