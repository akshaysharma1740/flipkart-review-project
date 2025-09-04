import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_flipkart_product(driver, product_url, max_pages=3, max_reviews=100):
    data = {
        "product_name": "N/A",
        "price": "N/A",
        "num_reviews": 0,
        "reviews": []
    }

    driver.get(product_url)
    time.sleep(3)

    # Get product name
    try:
        data["product_name"] = driver.find_element(By.XPATH, "//span[@class='VU-ZEz']").text.strip()
    except:
        pass

    # Get price
    try:
        data["price"] = driver.find_element(By.XPATH, "//div[@class='Nx9bqj CxhGGd']").text.strip()
    except:
        pass

    # Click "All reviews"
    try:
        all_reviews_link = driver.find_element(By.XPATH, "//div[@class='_23J90q RcXBOT']/span")
        driver.execute_script("arguments[0].click();", all_reviews_link)
        time.sleep(2)
    except:
        pass

    reviews = []
    page = 1

    while page <= max_pages and len(reviews) < max_reviews:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ZmyHeo"))
            )
        except:
            break

        elements = driver.find_elements(By.CSS_SELECTOR, "div.ZmyHeo")
        print(f"Found {len(elements)} reviews on page {page}")  # debug

        for el in elements:
            if len(reviews) < max_reviews:
                reviews.append(el.text.strip())

        # Click next page
        try:
            next_button = driver.find_element(By.XPATH, "//a[@class='_9QVEpD']")
            driver.execute_script("arguments[0].click();", next_button)
            page += 1
            time.sleep(2)
        except:
            break

    data["reviews"] = reviews
    data["num_reviews"] = len(reviews)
    print(f"Total reviews scraped: {len(reviews)}")
    return data

def scrape_all_products(file_path="data/flipkartproducts.xlsx"):
    # Read product URLs
    df_products = pd.read_excel(file_path)
    urls = df_products["url"].dropna().tolist()

    # Create reviews Excel if not exists
    os.makedirs("data", exist_ok=True)
    reviews_file = os.path.join("data", "reviews.xlsx")
    if not os.path.exists(reviews_file):
        pd.DataFrame(columns=["product_name", "price", "review_text"]).to_excel(reviews_file, index=False)

    driver = init_driver(headless=False)

    for idx, url in enumerate(urls, start=1):
        print(f"\nScraping product {idx}/{len(urls)}: {url}")
        product_data = scrape_flipkart_product(driver, url)
        reviews = product_data["reviews"]

        if reviews:
            df = pd.DataFrame({
                "product_name": [product_data["product_name"]] * len(reviews),
                "price": [product_data["price"]] * len(reviews),
                "review_text": reviews
            })

            # Append to existing Excel
            if os.path.exists(reviews_file):
                existing_df = pd.read_excel(reviews_file)
                df = pd.concat([existing_df, df], ignore_index=True)

            df.to_excel(reviews_file, index=False)
            print(f"✅ Saved {len(reviews)} reviews for this product to {reviews_file}")

    driver.quit()
    print("\nAll products scraped successfully!")

if __name__ == "__main__":
    scrape_all_products()
