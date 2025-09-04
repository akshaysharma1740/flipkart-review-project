# Flipkart Review Sentiment Analyzer

This project scrapes product reviews from **Flipkart**, performs **sentiment analysis**, and generates **summaries** of customer feedback.  

---

Features
- Scrapes product details (name, price, reviews) from Flipkart  
- Collects multiple pages of reviews  
- Performs sentiment analysis (positive / negative / neutral)  
- Summarizes large sets of reviews  
- Saves results into Excel for easy use  

---

Tech Stack
- Python  
- Selenium  
- Pandas  
- NLTK / Transformers  

---

 ⚙️ How It Works

1. **Input**: Add Flipkart product URLs into `data/flipkartproducts.xlsx`.  
2. **Scraping**: `flipkartscraper.py` fetches all reviews from the given product URLs.  
3. **Preprocessing**: `preprocess.py` cleans and prepares text data.  
4. **Sentiment Analysis**: `sentiment.py` analyzes each review → Positive, Negative, or Neutral.  
5. **Output**: The results (reviews, sentiments, and summaries) are saved into `output/flipkartsentiment.xlsx`.  

---

 🚀 Getting Started

 1. Clone the Repository
```bash
git clone https://github.com/akshaysharma1740/review_sentiment_project.git
cd review_sentiment_project
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
pip install -r requirements.txt
put flipkartproducts.xlsx in data folder(with products url)
python src/flipkartscarper.py
python src/preprocess.py
python src/sentiment.py

📊 Example Output
The final Excel file contains:
1.Reviews
2.Sentiment
3.Summarized Review

📌 Tech Stack
1.Python 3.10+
2.Selenium + WebDriver Manager (scraping)
3.SpaCy (text preprocessing)
4.Transformers (Hugging Face) (sentiment model)
5.Pandas + OpenPyXL (Excel handling)

👨‍💻 Author
Developed by Akshay Sharma.