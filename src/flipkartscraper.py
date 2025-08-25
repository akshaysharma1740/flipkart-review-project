import time
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

    try:
        data["product_name"] = driver.find_element(By.XPATH, "//span[@class='VU-ZEz']").text.strip()
    except:
        pass

    try:
        data["price"] = driver.find_element(By.XPATH, "//div[@class='Nx9bqj CxhGGd']").text.strip()
    except:
        pass

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
        for el in elements:
            if len(reviews) < max_reviews:
                reviews.append(el.text.strip())

        try:
            next_button = driver.find_element(By.XPATH, "//a[@class='_9QVEpD']")
            driver.execute_script("arguments[0].click();", next_button)
            page += 1
            time.sleep(2)
        except:
            break

    data["reviews"] = reviews
    data["num_reviews"] = len(reviews)

    return data
